#!/bin/bash
pod_info=$(kubectl get pods --no-headers -o custom-columns=":metadata.name,:status.phase" | grep '^ebpf-')
if [ -z "$pod_info" ]; then
  echo "No pod found with the prefix 'ebpf-'"
  exit 1
fi
pod_name=$(echo "$pod_info" | awk '{print $1}')
pod_status=$(echo "$pod_info" | awk '{print $2}')
if [[ "$pod_status" == "Running" || "$pod_status" == "Terminating" || "$pod_status" == "ContainerCreating" ]]; then
  kubectl logs "$pod_name" -f
else
  kubectl logs "$pod_name"
fi
