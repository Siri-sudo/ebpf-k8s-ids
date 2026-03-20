#!/bin/bash
ip link set dev eth0 xdp obj /opt/xdp_prog.o sec xdp
cat /sys/kernel/debug/tracing/trace_pipe
