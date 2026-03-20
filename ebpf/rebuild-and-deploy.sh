#!/bin/sh
cd /home/bootless/xdp || exit
kubectl delete ds ebpf-monitor
while kubectl get po | grep -q '^ebpf-'; do
  echo "Waiting for ebpf pod to terminate..."
  sleep 5
done
echo "ebpf pod terminated."
docker build -t sirisha1997/ebpf-xdp:latest . --progress=plain
docker push sirisha1997/ebpf-xdp:latest
kubectl apply -f ebpf-xdp.yaml
