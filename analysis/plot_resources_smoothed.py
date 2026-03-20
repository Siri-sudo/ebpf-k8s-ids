import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


with open('scan_ebpf_resources.json', 'r') as f:
    scan_ebpf_data = json.load(f)

with open('scan_snort_resources.json', 'r') as f:
    scan_snort_data = json.load(f)

with open('idle_ebpf_resources.json', 'r') as f:
    idle_ebpf_data = json.load(f)

with open('idle_snort_resources.json', 'r') as f:
    idle_snort_data = json.load(f)


scan_ebpf_df = pd.DataFrame(scan_ebpf_data)
scan_snort_df = pd.DataFrame(scan_snort_data)
idle_ebpf_df = pd.DataFrame(idle_ebpf_data)
idle_snort_df = pd.DataFrame(idle_snort_data)


def convert_time(df):
    start_time = df['time'].min()
    df['relative_time'] = df['time'] - start_time
    return df

scan_ebpf_df = convert_time(scan_ebpf_df)
scan_snort_df = convert_time(scan_snort_df)
idle_ebpf_df = convert_time(idle_ebpf_df)
idle_snort_df = convert_time(idle_snort_df)


def calc_stats(df, window=50):
    df['cpu_mean'] = df['cpu_percent'].rolling(window=window).mean()
    df['cpu_se'] = df['cpu_percent'].rolling(window=window).std() / np.sqrt(window)
    df['mem_mean'] = df['memory_percent'].rolling(window=window).mean()
    df['mem_se'] = df['memory_percent'].rolling(window=window).std() / np.sqrt(window)
    return df


scan_ebpf_df = calc_stats(scan_ebpf_df)
scan_snort_df = calc_stats(scan_snort_df)
idle_ebpf_df = calc_stats(idle_ebpf_df)
idle_snort_df = calc_stats(idle_snort_df)


plt.rcParams.update({
    'font.size': 25,
    'axes.titlesize': 25,
    'axes.labelsize': 25,
    'xtick.labelsize': 25,
    'ytick.labelsize': 25,
    'legend.fontsize': 20,
    'figure.titlesize': 28
})


plt.figure(figsize=(8, 8))

plt.errorbar(idle_ebpf_df['relative_time'], idle_ebpf_df['cpu_mean'], yerr=idle_ebpf_df['cpu_se'], 
             label='eBPF Idle', color='blue', ecolor='lightblue', capsize=3)

plt.errorbar(scan_ebpf_df['relative_time'], scan_ebpf_df['cpu_mean'], yerr=scan_ebpf_df['cpu_se'], 
             label='eBPF Scan', color='darkblue', ecolor='lightblue', capsize=3)

plt.errorbar(idle_snort_df['relative_time'], idle_snort_df['cpu_mean'], yerr=idle_snort_df['cpu_se'], 
             label='Snort Idle', color='red', ecolor='lightcoral', capsize=3)

plt.errorbar(scan_snort_df['relative_time'], scan_snort_df['cpu_mean'], yerr=scan_snort_df['cpu_se'], 
             label='Snort Scan', color='darkred', ecolor='lightcoral', capsize=3)

plt.xlabel('Time (seconds)')
plt.ylabel('CPU Percent (%)')
plt.xlim(0, plt.xlim()[1])
plt.ylim(0, plt.ylim()[1])
plt.legend()
plt.grid(True)
plt.savefig('cpu_consumptionsmooth.pdf', format='pdf')


plt.figure(figsize=(8, 8))

plt.errorbar(idle_ebpf_df['relative_time'], idle_ebpf_df['mem_mean'], yerr=idle_ebpf_df['mem_se'], 
             label='eBPF Idle', color='blue', ecolor='lightblue', capsize=3)

plt.errorbar(scan_ebpf_df['relative_time'], scan_ebpf_df['mem_mean'], yerr=scan_ebpf_df['mem_se'], 
             label='eBPF Scan', color='darkblue', ecolor='lightblue', capsize=3)

plt.errorbar(idle_snort_df['relative_time'], idle_snort_df['mem_mean'], yerr=idle_snort_df['mem_se'], 
             label='Snort Idle', color='red', ecolor='lightcoral', capsize=3)

plt.errorbar(scan_snort_df['relative_time'], scan_snort_df['mem_mean'], yerr=scan_snort_df['mem_se'], 
             label='Snort Scan', color='darkred', ecolor='lightcoral', capsize=3)

plt.xlabel('Time (seconds)')
plt.ylabel('Memory Percent (%)')
plt.xlim(0, plt.xlim()[1])
plt.ylim(0, plt.ylim()[1])
plt.legend()
plt.grid(True)
plt.savefig('memory_consumptionsmooth.pdf', format='pdf')
