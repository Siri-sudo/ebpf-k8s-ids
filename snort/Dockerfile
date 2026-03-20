FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    snort \
    libpcap-dev \
    iproute2 \
    iputils-ping \
    net-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY snort.conf /etc/snort/snort.conf
COPY local.rules /etc/snort/rules/local.rules
RUN mkdir -p /var/log/snort
