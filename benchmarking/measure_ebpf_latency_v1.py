import subprocess
import time
import re
import threading
import argparse
import queue

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Monitor eBPF container logs for port scan detection.')
    parser.add_argument('--container-name', type=str, required=True, help='Name of the container running eBPF')
    parser.add_argument('--target-ip', type=str, required=True, help='Target IP for nmap scan')
    return parser.parse_args()

def run_command(command):
    """Run a shell command and return its output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')

def run_nmap_scan(target_ip):
    """Run the nmap scan using kubectl exec."""
    NMAP_SCAN_COMMAND = ["nmap", "-sS", "-p", "1-20", target_ip]
    kubectl_nmap_command = ["kubectl", "exec", "nmap", "--"] + NMAP_SCAN_COMMAND
    run_command(kubectl_nmap_command)

def monitor_logs(container_name, start_time, detection_queue):
    """Monitor the eBPF container logs for port scan detection."""
    log_pattern = re.compile(r"Port scan detected from IP: [0-9a-f]+")  # Adjusted to match 'Port scan detected from IP: 201f40a'

    # Start kubectl logs with --follow to continuously read logs
    kubectl_logs_command = [
        "kubectl", "logs", container_name, "--follow"
    ]
    
    with subprocess.Popen(kubectl_logs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            # Check if the logs contain the detection message
            if log_pattern.search(line):
                detection_time = time.time()
                latency = detection_time - start_time
                detection_queue.put(latency)  # Put latency in the queue
                break

def main():
    # Parse arguments
    args = parse_arguments()
    container_name = args.container_name
    target_ip = args.target_ip

    # Step 1: Start Timer
    start_time = time.time()

    print("Starting nmap scan and monitoring logs...")

    # Step 2: Start nmap scan in a separate thread
    nmap_thread = threading.Thread(target=run_nmap_scan, args=(target_ip,))
    nmap_thread.start()

    # Queue to communicate detection latency between threads
    detection_queue = queue.Queue()

    # Step 3: Monitor logs for detection concurrently
    monitor_thread = threading.Thread(target=monitor_logs, args=(container_name, start_time, detection_queue))
    monitor_thread.start()

    # Wait for detection or nmap to finish
    while nmap_thread.is_alive() and monitor_thread.is_alive():
        try:
            latency = detection_queue.get(timeout=0.1)
            print(f"Port scan detected! Latency: {latency:.2f} seconds")
            break
        except queue.Empty:
            continue

    # Ensure both threads finish before exiting the script
    nmap_thread.join()
    monitor_thread.join()

if __name__ == "__main__":
    main()
