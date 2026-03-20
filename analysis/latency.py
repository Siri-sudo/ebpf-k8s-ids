import json
import numpy as np
import matplotlib.pyplot as plt


with open('snort_detection_times.json', 'r') as file:
    snort_data = json.load(file)

with open('ebpf_detection_times.json', 'r') as file:
    ebpf_data = json.load(file)


snort_array = np.array(snort_data)
ebpf_array = np.array(ebpf_data)


iterations = np.arange(1, len(snort_array) + 1)


snort_cumulative_avg = np.cumsum(snort_array) / iterations
ebpf_cumulative_avg = np.cumsum(ebpf_array) / iterations


snort_std = np.std(snort_array)
ebpf_std = np.std(ebpf_array)


plt.figure(figsize=(10, 10))
plt.rcParams.update({
    'font.size': 25,
    'axes.titlesize': 25,
    'axes.labelsize': 25,
    'xtick.labelsize': 25,
    'ytick.labelsize': 25,
    'legend.fontsize': 20,
    'figure.titlesize': 28})
plt.errorbar(iterations, snort_array, yerr=snort_std, label='Snort', fmt='-')
plt.errorbar(iterations, ebpf_array, yerr=ebpf_std, label='eBPF', fmt='-')
plt.xlabel('Iterations')
plt.ylabel('Latency (ms)')

plt.legend()
plt.grid(True)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.savefig('latency.pdf',format="pdf", bbox_inches="tight")



plt.figure(figsize=(10, 10))
plt.rcParams.update({
    'font.size': 25,
    'axes.titlesize': 25,
    'axes.labelsize': 25,
    'xtick.labelsize': 25,
    'ytick.labelsize': 25,
    'legend.fontsize': 20,
    'figure.titlesize': 28})
plt.errorbar(iterations, snort_cumulative_avg, yerr=snort_std/np.sqrt(iterations), label='Snort', fmt='-')
plt.errorbar(iterations, ebpf_cumulative_avg, yerr=ebpf_std/np.sqrt(iterations), label='eBPF', fmt='-')
plt.xlabel('Iterations')
plt.ylabel('Cumulative Average Latency (ms)')

plt.legend()
plt.grid(True)
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.savefig('cumuavg.pdf',format="pdf", bbox_inches="tight")