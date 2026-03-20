import json
import numpy as np
import matplotlib.pyplot as plt


with open('snort_detection_times.json', 'r') as file:
    snort_detection_times = json.load(file)

with open('ebpf_detection_times.json', 'r') as file:
    ebpf_detection_times = json.load(file)


snort_mean = np.mean(snort_detection_times)
ebpf_mean = np.mean(ebpf_detection_times)


snort_mae = np.mean(np.abs(np.array(snort_detection_times) - snort_mean))
ebpf_mae = np.mean(np.abs(np.array(ebpf_detection_times) - ebpf_mean))


labels = ['Snort', 'eBPF']
means = [snort_mean, ebpf_mean]
errors = [snort_mae, ebpf_mae]


plt.figure(figsize=(8, 8))
plt.rcParams.update({
    'font.size': 25,
    'axes.titlesize': 25,
    'axes.labelsize': 25,
    'xtick.labelsize': 25,
    'ytick.labelsize': 25,
    'legend.fontsize': 20,
    'figure.titlesize': 28
})
plt.bar(labels, means, yerr=errors, capsize=5, color=['#1f77b4', '#ff7f0e'], alpha=0.7)
plt.ylabel('Average Detection Time (ms)')

plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('barlatency.pdf', format="pdf", bbox_inches="tight")

