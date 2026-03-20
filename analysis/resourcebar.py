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


cpu_means = [cpu_idle_ebpf.mean(), cpu_idle_snort.mean(), cpu_scan_ebpf.mean(), cpu_scan_snort.mean()]
cpu_mae = [np.mean(np.abs(cpu_idle_ebpf - cpu_idle_ebpf.mean())), 
           np.mean(np.abs(cpu_idle_snort - cpu_idle_snort.mean())), 
           np.mean(np.abs(cpu_scan_ebpf - cpu_scan_ebpf.mean())), 
           np.mean(np.abs(cpu_scan_snort - cpu_scan_snort.mean()))]

ram_means = [ram_idle_ebpf.mean(), ram_idle_snort.mean(), ram_scan_ebpf.mean(), ram_scan_snort.mean()]
ram_mae = [np.mean(np.abs(ram_idle_ebpf - ram_idle_ebpf.mean())), 
           np.mean(np.abs(ram_idle_snort - ram_idle_snort.mean())), 
           np.mean(np.abs(ram_scan_ebpf - ram_scan_ebpf.mean())), 
           np.mean(np.abs(ram_scan_snort - ram_scan_snort.mean()))]


print("CPU Averages:", cpu_means)
print("CPU MAE:", cpu_mae)
print("RAM Averages:", ram_means)
print("RAM MAE:", ram_mae)


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
x_labels = ['Idle ebpf', 'Idle snort', 'Scan ebpf', 'Scan snort']
x_positions = np.arange(len(cpu_means))
plt.bar(x_positions, cpu_means, yerr=cpu_mae, capsize=10, color=['blue', 'red', 'darkblue', 'darkred'], alpha=0.7)
plt.xticks(x_positions, x_labels)
plt.ylabel('CPU Usage (%)')
plt.title('Average CPU Usage with MAE')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('cpu_usage.pdf', format='pdf')



plt.figure(figsize=(12, 12))
plt.bar(x_positions, ram_means, yerr=ram_mae, capsize=10, color=['blue', 'red', 'darkblue', 'darkred'], alpha=0.7)
plt.xticks(x_positions, x_labels)
plt.ylabel('RAM Usage (%)')
plt.title('Average RAM Usage with MAE')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('ram_usage.pdf', format='pdf')
