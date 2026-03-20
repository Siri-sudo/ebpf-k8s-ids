import subprocess
import time
import re
import threading
import argparse
import queue
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitor Snort container logs for port scan detection.')
    parser.add_argument('--container-name', type=str, required=True, help='Name of the container running Snort')
    parser.add_argument('--target-ip', type=str, required=True, help='Target IP for nmap scan')
    parser.add_argument('--output-file', type=str, default='snort_detection_times.json', help='Output file for detection times')
    parser.add_argument('--num-scans', type=int, default=1000, help='Number of scans to perform')
    return parser.parse_args()

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def run_nmap_scan(target_ip):
    NMAP_SCAN_COMMAND = ["nmap", "-sS", "-p-", target_ip]
    kubectl_nmap_command = ["kubectl", "exec", "nmap", "--"] + NMAP_SCAN_COMMAND
    run_command(kubectl_nmap_command)

def monitor_logs(container_name, start_time_ns, detection_queue):
    log_pattern = re.compile(r"TCP SCAN DETECTED")  # Adjusted to match 'Port scan detected from IP: 201f40a'

    # Start kubectl logs with --follow to continuously read logs
    kubectl_logs_command = [
        "kubectl", "logs", container_name, "--follow"
    ]

    with subprocess.Popen(kubectl_logs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            # Check if the logs contain the detection message
            if log_pattern.search(line):
                detection_time_ns = time.perf_counter_ns()
                latency_ms = (detection_time_ns - start_time_ns) / 1_000_000  # Convert nanoseconds to milliseconds
                detection_queue.put(latency_ms)  # Put latency in milliseconds in the queue
                break

def main():
    # Parse arguments
    args = parse_arguments()
    container_name = args.container_name
    target_ip = args.target_ip
    output_file = args.output_file
    num_scans = args.num_scans

    detection_times = []  # List to store detection times

    for i in range(num_scans):
        print(f"Starting nmap scan {i+1}/{num_scans} and monitoring logs...")

        # Start Timer for this scan
        start_time_ns = time.perf_counter_ns()

        # Queue to communicate detection latency between threads
        detection_queue = queue.Queue()

        # Start nmap scan in a separate thread
        nmap_thread = threading.Thread(target=run_nmap_scan, args=(target_ip,))
        nmap_thread.start()

        # Monitor logs for detection concurrently
        monitor_thread = threading.Thread(target=monitor_logs, args=(container_name, start_time_ns, detection_queue))
        monitor_thread.start()

        # Wait for detection or nmap to finish
        while nmap_thread.is_alive() and monitor_thread.is_alive():
            try:
                latency_ms = detection_queue.get(timeout=0.1)
                print(f"Port scan detected! Latency: {latency_ms:.2f} milliseconds")
                detection_times.append(latency_ms)
                break
            except queue.Empty:
                continue

        # Ensure both threads finish before moving to the next scan
        nmap_thread.join()
        monitor_thread.join()

    # Output the detection times to a JSON file
    with open(output_file, 'w') as f:
        json.dump(detection_times, f)

    print(f"Detection times written to {output_file}")

if __name__ == "__main__":
    main()
