#!/bin/sh
cd /home/bootless/xdp || exit
kubectl delete ds ebpf-monitor
docker build -t sirisha1997/ebpf-xdp:latest . --progress=plain
docker push sirisha1997/ebpf-xdp:latest
kubectl apply -f ebpf-xdp.yaml
