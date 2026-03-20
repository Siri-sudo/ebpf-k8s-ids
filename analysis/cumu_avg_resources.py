import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np


with open('idle_snort_resources.json', 'r') as file:
    idle_snort = json.load(file)

with open('scan_ebpf_resources.json', 'r') as file:
    scan_ebpf = json.load(file)

with open('scan_snort_resources.json', 'r') as file:
    scan_snort = json.load(file)

with open('idle_ebpf_resources.json', 'r') as file:
    idle_ebpf = json.load(file)


df_idle_snort = pd.DataFrame(idle_snort)
df_scan_ebpf = pd.DataFrame(scan_ebpf)
df_scan_snort = pd.DataFrame(scan_snort)
df_idle_ebpf = pd.DataFrame(idle_ebpf)


cpu_idle_snort = df_idle_snort['cpu_percent']
cpu_idle_ebpf = df_idle_ebpf['cpu_percent']
cpu_scan_snort = df_scan_snort['cpu_percent']
cpu_scan_ebpf = df_scan_ebpf['cpu_percent']

ram_idle_snort = df_idle_snort['memory_percent']
ram_idle_ebpf = df_idle_ebpf['memory_percent']
ram_scan_snort = df_scan_snort['memory_percent']
ram_scan_ebpf = df_scan_ebpf['memory_percent']


cpu_idle_ebpf_cumavg = cpu_idle_ebpf.expanding().mean()
cpu_idle_snort_cumavg = cpu_idle_snort.expanding().mean()
cpu_scan_ebpf_cumavg = cpu_scan_ebpf.expanding().mean()
cpu_scan_snort_cumavg = cpu_scan_snort.expanding().mean()

ram_idle_ebpf_cumavg = ram_idle_ebpf.expanding().mean()
ram_idle_snort_cumavg = ram_idle_snort.expanding().mean()
ram_scan_ebpf_cumavg = ram_scan_ebpf.expanding().mean()
ram_scan_snort_cumavg = ram_scan_snort.expanding().mean()


plt.rcParams.update({
    'font.size': 25,
    'axes.titlesize': 25,
    'axes.labelsize': 25,
    'xtick.labelsize': 25,
    'ytick.labelsize': 25,
    'legend.fontsize': 20,
    'figure.titlesize': 28
})


plt.figure(figsize=(12, 12))
plt.plot(cpu_idle_ebpf_cumavg, label='Idle ebpf')
plt.plot(cpu_idle_snort_cumavg, label='Idle snort')
plt.plot(cpu_scan_ebpf_cumavg, label='Scan ebpf')
plt.plot(cpu_scan_snort_cumavg, label='Scan snort')
plt.xlabel('Iterations')
plt.ylabel('Cumulative Average CPU Usage (%)')
plt.ylim(0)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('cumulative_cpu_usage.pdf', format='pdf')
plt.close()


plt.figure(figsize=(12, 12))
plt.plot(ram_idle_ebpf_cumavg, label='Idle ebpf')
plt.plot(ram_idle_snort_cumavg, label='Idle snort')
plt.plot(ram_scan_ebpf_cumavg, label='Scan ebpf')
plt.plot(ram_scan_snort_cumavg, label='Scan snort')
plt.xlabel('Iterations')
plt.ylabel('Cumulative Average RAM Usage (%)')
plt.ylim(0)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('cumulative_ram_usage.pdf', format='pdf')
