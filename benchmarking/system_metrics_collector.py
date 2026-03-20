#!/home/bootless/snortebpf/bin/python3

import psutil
import json
import time
from datetime import datetime

# File to output data
OUTPUT_FILE = "system_metrics.json"

# Interval in seconds
INTERVAL = 10

# Duration in seconds (set to 0 for infinite loop)
DURATION = 60

# Initialize list to store metrics
metrics = []

def collect_metrics():
    """Collect system metrics and return as a dictionary."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # CPU utilization
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Memory utilization
    mem = psutil.virtual_memory()
    mem_usage = mem.percent
    
    # Disk utilization (root partition)
    disk_usage = psutil.disk_usage('/').percent
    
    # Create a dictionary with the collected metrics
    metric = {
        "timestamp": timestamp,
        "cpu_usage": cpu_usage,
        "mem_usage": mem_usage,
        "disk_usage": disk_usage
    }
    
    return metric

# Start monitoring
start_time = time.time()
while True:
    metrics.append(collect_metrics())
    time.sleep(INTERVAL)
    
    # Check if duration has been reached
    if DURATION > 0 and (time.time() - start_time) >= DURATION:
        break

# Write collected metrics to a JSON file
with open(OUTPUT_FILE, 'w') as f:
    json.dump(metrics, f, indent=4)

print(f"Monitoring finished. Data written to {OUTPUT_FILE}.")
