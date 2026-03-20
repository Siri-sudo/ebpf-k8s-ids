# ebpf-k8s-ids

Kernel-space port scan detection for Kubernetes using eBPF/XDP, benchmarked 
against Snort. MSc Cyber Security dissertation; Lancaster University, 2024.

---

## What this is

An XDP (eXpress Data Path) program that attaches to the network driver on each 
Kubernetes worker node and detects TCP SYN port scans entirely in kernel space. 
When a source IP exceeds 20 SYN packets within a 10-second window, the event is 
logged via `bpf_printk` to the kernel trace pipe. No userspace agent. No packet 
copying. Detection happens before packets reach the kernel networking stack.

Benchmarked against Snort 2.9 deployed as a Kubernetes DaemonSet on the same 
interface, under identical conditions, across 1000 nmap TCP SYN scans.

---

## Results

Statistical significance tested with Welch's two-sample t-test (α = 0.05).

**Detection latency**

| | Mean | MAE |
|---|---|---|
| Snort | 69.41 ms | ±4.45 ms |
| eBPF/XDP | 72.01 ms | ±6.07 ms |

p-value: 5.4×10⁻¹⁶. Statistically significant difference. Snort was marginally 
faster on raw latency; eBPF showed higher variance. The measurement method 
(polling kubectl logs) introduces noise that partially offsets the XDP advantage.

**RAM usage**

| | Idle | Under scan |
|---|---|---|
| eBPF/XDP | 44.55 ±0.22% | 44.54 ±0.13% |
| Snort | 48.95 ±0.14% | 49.03 ±0.18% |

p-value ≈ 0. Statistically significant. eBPF uses approximately 5% less RAM across 
both idle and scan conditions.

**CPU usage**

Both systems used approximately 4% at idle and 17.5% under active scans.
p-value: 0.614 (idle), 0.894 (scan). No statistically significant difference.

---

## How it works

`xdp_prog.c` attaches to `eth0` in XDP mode. For each inbound TCP packet:

1. Checks for SYN without ACK (new connection attempt, no handshake)
2. Looks up the source IP in a BPF hash map (max 1024 entries)
3. If within the 10-second time window, increments the SYN counter
4. At threshold (20 SYNs), logs a detection via `bpf_printk`
5. Resets the counter on window expiry
6. Returns XDP_PASS; all packets are forwarded regardless

Detection events are read from `/sys/kernel/debug/tracing/trace_pipe` via:
```sh
cat /sys/kernel/debug/tracing/trace_pipe
```

or through `kubectl logs` on the DaemonSet pod.

---

## Repo structure
```
ebpf-k8s-ids/
│
├── ebpf/
│   ├── xdp_prog.c              XDP program source
│   ├── xdp_prog.o              compiled eBPF object
│   ├── Dockerfile              container image for the DaemonSet
│   ├── entrypoint.sh           loads XDP program, tails trace_pipe
│   ├── monitor-daemonset.yaml  Kubernetes DaemonSet manifest
│   ├── rebuild-and-deploy.sh   build, push, redeploy (waits for termination)
│   ├── build-and-push.sh       build and push without waiting
│   └── stream-logs.sh          tail logs from the running eBPF pod
│
├── snort/
│   ├── Dockerfile
│   ├── snort.conf
│   ├── local.rules
│   ├── snort-daemonset.yaml
│   └── rebuild-and-deploy.sh
│
├── k8s-nmap/
│   └── attacker-pod.yaml       nmap pod used to trigger scans
│
├── benchmarking/
│   ├── measure_ebpf_latency.py      runs nmap, monitors trace_pipe, records ms
│   ├── measure_ebpf_latency_v1.py   single-run prototype
│   ├── measure_snort_latency.py     monitors kubectl logs, records ms
│   ├── measure_snort_latency_v2.py  structured logging variant
│   ├── bpftrace_monitor.py          bpftrace-based monitor (exploratory)
│   ├── scan_ebpf_resources.py       CPU/RAM during scans, eBPF running
│   ├── scan_snort_resources.py      CPU/RAM during scans, Snort running
│   ├── idle_ebpf_resources.py       CPU/RAM at idle, eBPF running
│   ├── idle_snort_resources.py      CPU/RAM at idle, Snort running
│   ├── pod_resource_monitor.py      pod-level resource monitor via kubectl top
│   └── system_metrics_collector.py  general system metrics
│
├── analysis/
│   ├── plot_latency_bar.py          mean detection time bar chart with MAE
│   ├── plot_latency_raw.py          raw and cumulative average latency
│   ├── plot_latency_smoothed.py     smoothed latency with rolling window
│   ├── plot_resources_bar.py        average resource bar charts with MAE
│   ├── plot_resources_cumulative.py cumulative average CPU and RAM
│   ├── plot_resources_raw.py        raw CPU and RAM over time
│   ├── plot_resources_smoothed.py   smoothed CPU/RAM with standard error
│   ├── ttest_latency.py             Welch's t-test on detection latency
│   └── ttest_resources.py           Welch's t-test on CPU and RAM
│
└── .gitignore
```

---

## Running the benchmark

Update the Docker Hub username in `rebuild-and-deploy.sh` and `build-and-push.sh` 
before building.

**Deploy both DaemonSets:**
```sh
cd ebpf && ./rebuild-and-deploy.sh
cd snort && ./rebuild-and-deploy.sh
```

**Measure detection latency (1000 scans each):**
```sh
python benchmarking/measure_ebpf_latency.py \
  --container-name <ebpf-pod> \
  --target-ip <node-ip> \
  --num-scans 1000 \
  --output-file ebpf_detection_times.json

python benchmarking/measure_snort_latency.py \
  --container-name <snort-pod> \
  --target-ip <node-ip> \
  --num-scans 1000 \
  --output-file snort_detection_times.json
```

**Measure resource usage (run while scans are active):**
```sh
python benchmarking/scan_ebpf_resources.py --target-ip <node-ip>
python benchmarking/scan_snort_resources.py --target-ip <node-ip>
python benchmarking/idle_ebpf_resources.py
python benchmarking/idle_snort_resources.py
```

**Run analysis (JSON files must be in the working directory):**
```sh
cd analysis
python ttest_latency.py
python ttest_resources.py
python plot_latency_bar.py
python plot_latency_raw.py
python plot_latency_smoothed.py
python plot_resources_bar.py
python plot_resources_cumulative.py
python plot_resources_raw.py
python plot_resources_smoothed.py
```

---

## Environment

- Kubernetes 1.30, minikube (docker driver), kindnet CNI
- Ubuntu 22.04, kernel 6.8.0-41
- XDP minimum kernel requirement: 4.18
- Python 3.10; numpy, pandas, matplotlib, scipy, psutil
- Snort 2.9 containerised via Docker

---

## Security notes

Both DaemonSets run `privileged: true` with `hostNetwork: true`. This is required 
for the benchmark. Snort needs raw socket access; eBPF needs `/sys/fs/bpf`, 
`/lib/modules`, and `/sys/kernel/debug`. Neither manifest is appropriate for 
production without scoping down capabilities.

For production eBPF deployment: use `CAP_BPF` (kernel 5.8+) rather than 
`CAP_SYS_ADMIN`, restrict the BPF syscall via seccomp, and review verifier output 
before loading programs. The eBPF verifier itself has had exploitable bugs 
(CVE-2024-41003); keep the kernel patched.