import pandas as pd
import json
from scipy.stats import ttest_ind


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


cpu_idle_test = ttest_ind(cpu_idle_ebpf, cpu_idle_snort, equal_var=False)
cpu_scan_test = ttest_ind(cpu_scan_ebpf, cpu_scan_snort, equal_var=False)
ram_idle_test = ttest_ind(ram_idle_ebpf, ram_idle_snort, equal_var=False)
ram_scan_test = ttest_ind(ram_scan_ebpf, ram_scan_snort, equal_var=False)


print("CPU Usage (ebpf idle vs snort idle):")
print(f"t-statistic: {cpu_idle_test.statistic:.3e}, p-value: {cpu_idle_test.pvalue:.3e}\n")

print("CPU Usage (ebpf scan vs snort scan):")
print(f"t-statistic: {cpu_scan_test.statistic:.3e}, p-value: {cpu_scan_test.pvalue:.3e}\n")

print("RAM Usage (ebpf idle vs snort idle):")
print(f"t-statistic: {ram_idle_test.statistic:.3e}, p-value: {ram_idle_test.pvalue:.3e}\n")

print("RAM Usage (ebpf scan vs snort scan):")
print(f"t-statistic: {ram_scan_test.statistic:.3e}, p-value: {ram_scan_test.pvalue:.3e}")
