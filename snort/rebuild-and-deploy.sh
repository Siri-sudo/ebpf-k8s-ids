#!/bin/sh
cd /home/bootless/snort || exit
kubectl delete ds snort
while kubectl get po | grep -q '^snort-'; do
  echo "Waiting for snort pod to terminate..."
  sleep 5
done
echo "ebpf pod terminated."
docker build -t sirisha1997/snort:latest . --progress=plain
docker push sirisha1997/snort:latest
kubectl apply -f snort-ds.yaml
