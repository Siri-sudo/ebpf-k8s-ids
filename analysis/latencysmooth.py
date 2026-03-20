import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


with open('snort_detection_times.json') as f:
    snort_data = json.load(f)

with open('ebpf_detection_times.json') as f:
    ebpf_data = json.load(f)


snort_series = pd.Series(snort_data)
ebpf_series = pd.Series(ebpf_data)


window_size = 10


snort_moving_avg = snort_series.rolling(window=window_size).mean()
ebpf_moving_avg = ebpf_series.rolling(window=window_size).mean()


snort_std = snort_series.rolling(window=window_size).std()
ebpf_std = ebpf_series.rolling(window=window_size).std()
plt.rcParams.update({
    'font.size': 25,
    'axes.titlesize': 25,
    'axes.labelsize': 25,
    'xtick.labelsize': 25,
    'ytick.labelsize': 25,
    'legend.fontsize': 20,
    'figure.titlesize': 28})

plt.figure(figsize=(10, 10))


plt.plot(snort_moving_avg, label='Snort Moving Average', linestyle='-', linewidth=2)
plt.fill_between(snort_series.index, snort_moving_avg - snort_std, snort_moving_avg + snort_std, alpha=0.2)

plt.plot(ebpf_moving_avg, label='eBPF Moving Average', linestyle='-', linewidth=2)
plt.fill_between(ebpf_series.index, ebpf_moving_avg - ebpf_std, ebpf_moving_avg + ebpf_std, alpha=0.2)


plt.xlabel('Iterations')
plt.ylabel('Latency (ms)')

plt.legend()


plt.xlim(left=0)
plt.ylim(bottom=0)


plt.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.7)


plt.tight_layout()
plt.savefig('smoothedlatency.pdf',format="pdf", bbox_inches="tight")
