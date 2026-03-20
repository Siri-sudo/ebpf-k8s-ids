#!/home/bootless/snortebpf/bin/python3
import subprocess
import time
import threading
import argparse
import json
import psutil

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run nmap scans for 5 minutes and record system resource utilization.')
    parser.add_argument('--output-file', type=str, default='data/idle_snort_resources.json', help='Output file for resource utilization')
    parser.add_argument('--interval', type=float, default=0.5, help='Interval in seconds to record resource utilization')
    return parser.parse_args()

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def record_resource_utilization(interval, utilization_data, end_time):
    while time.time() < end_time:
        # Record CPU and memory utilization
        cpu_percent = psutil.cpu_percent(interval=interval)
        memory_info = psutil.virtual_memory()
        utilization_data.append({
            "time": time.time(),
            "cpu_percent": cpu_percent,
            "memory_percent": memory_info.percent
        })

def main():
    # Parse arguments
    args = parse_arguments()
    output_file = args.output_file
    interval = args.interval

    utilization_data = []  # List to store resource utilization data

    # Calculate end time for 5 minutes from now
    end_time = time.time() + 300

    record_resource_utilization(interval, utilization_data, end_time)
    # Output the resource utilization data to a JSON file
    with open(output_file, 'w') as f:
        json.dump(utilization_data, f, indent=4)

    print(f"Resource utilization data written to {output_file}")

if __name__ == "__main__":
    main()
