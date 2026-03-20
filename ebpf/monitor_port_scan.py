import subprocess

def monitor_bpftrace():
    process = subprocess.Popen(
        ['bpftrace', 'port_scan_detected.bt'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        for line in iter(process.stdout.readline, ''):
            print(line.strip())
    except KeyboardInterrupt:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    monitor_bpftrace()
