FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    clang \
    llvm \
    xz-utils \
    python3 \
    kmod \
    python3-pip \
    bpfcc-tools \
    linux-headers-$(uname -r) \
    iproute2 \
    tar \
    make \
    git \
    curl
RUN apt-get update && \
    apt-get install -y bpftrace
COPY xdp_prog.o /opt/xdp_prog.o
WORKDIR /opt
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
ENTRYPOINT ["/opt/entrypoint.sh"]
