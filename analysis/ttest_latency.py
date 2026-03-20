import json
import numpy as np
from scipy import stats


with open('snort_detection_times.json', 'r') as file:
    snort_data = json.load(file)

with open('ebpf_detection_times.json', 'r') as file:
    ebpf_data = json.load(file)


snort_array = np.array(snort_data)
ebpf_array = np.array(ebpf_data)


t_statistic, p_value = stats.ttest_ind(ebpf_array, snort_array)


print(f"T-Statistic: {t_statistic}")
print(f"P-Value: {p_value}")


