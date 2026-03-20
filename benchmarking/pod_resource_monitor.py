#!/home/bootless/snortebpf/bin/python3
import subprocess
import time
import threading
import argparse
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run nmap scans for 5 minutes and record Kubernetes pod resource utilization.')
    parser.add_argument('--target-ip', type=str, required=True, help='Target IP for nmap scan')
    parser.add_argument('--namespace', type=str, required=True, help='Kubernetes namespace of the pod to monitor')
    parser.add_argument('--pod-name', type=str, required=True, help='Specific pod name to monitor')
    parser.add_argument('--output-file', type=str, default='scan_k8s_resources.json', help='Output file for resource utilization')
    parser.add_argument('--interval', type=float, default=10, help='Interval in seconds to record resource utilization')
    return parser.parse_args()

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def run_nmap_scan(target_ip):
    NMAP_SCAN_COMMAND = ["nmap", "-sS", "-p-", target_ip]
    run_command(NMAP_SCAN_COMMAND)

def record_pod_resource_utilization(namespace, pod_name, interval, utilization_data, end_time):
    while time.time() < end_time:
        command = ["kubectl", "top", "pod", pod_name, "--namespace", namespace, "--no-headers"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            line = result.stdout.strip()
            if line:
                parts = line.split()
                pod_data = {
                    "time": time.time(),
                    "namespace": namespace,
                    "pod": parts[0],
                    "cpu": parts[1],
                    "memory": parts[2]
                }
                utilization_data.append(pod_data)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running kubectl: {e}")
        # Wait for the next interval
        time.sleep(interval)

def main():
    # Parse arguments
    args = parse_arguments()
    target_ip = args.target_ip
    namespace = args.namespace
    pod_name = args.pod_name
    output_file = args.output_file
    interval = args.interval

    utilization_data = []  # List to store resource utilization data

    # Calculate end time for 5 minutes from now
    end_time = time.time() + 300

    # Start a thread to record pod resource utilization
    monitoring_thread = threading.Thread(
        target=record_pod_resource_utilization, 
        args=(namespace, pod_name, interval, utilization_data, end_time)
    )
    monitoring_thread.daemon = True  # Allows thread to exit when main program exits
    monitoring_thread.start()

    # Run nmap scans until the 5-minute duration has passed
    while time.time() < end_time:
        # Run nmap scan
        run_nmap_scan(target_ip)

    # Ensure monitoring thread has finished
    monitoring_thread.join()

    # Output the resource utilization data to a JSON file
    with open(output_file, 'w') as f:
        json.dump(utilization_data, f, indent=4)

    print(f"Resource utilization data written to {output_file}")

if __name__ == "__main__":
    main()
