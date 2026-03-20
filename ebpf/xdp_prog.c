#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/in.h>
#include <linux/if_ether.h>

#define SCAN_THRESHOLD 20
#define TIME_WINDOW 10 * 1000000000ULL

struct syn_data {
    __u32 count;
    __u64 timestamp;
};

struct bpf_map_def SEC("maps") syn_map = {
    .type = BPF_MAP_TYPE_HASH,
    .key_size = sizeof(__u32),
    .value_size = sizeof(struct syn_data),
    .max_entries = 1024,
};

SEC("xdp")
int xdp_prog(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    struct ethhdr *eth = data;

    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;

    if (eth->h_proto != bpf_htons(ETH_P_IP))
        return XDP_PASS;

    struct iphdr *ip = data + sizeof(*eth);
    if ((void *)(ip + 1) > data_end)
        return XDP_PASS;

    if (ip->protocol != IPPROTO_TCP)
        return XDP_PASS;

    struct tcphdr *tcp = (struct tcphdr *)((__u8 *)ip + (ip->ihl * 4));
    if ((void *)(tcp + 1) > data_end)
        return XDP_PASS;

    if (tcp->syn && !tcp->ack) {
        __u32 src_ip = ip->saddr;
        struct syn_data *data;
        __u64 now = bpf_ktime_get_ns();

        data = bpf_map_lookup_elem(&syn_map, &src_ip);
        if (data) {
            if (now - data->timestamp < TIME_WINDOW) {
                data->count += 1;
                if (data->count >= SCAN_THRESHOLD) {
                    bpf_printk("Port scan detected from IP: %x\n", src_ip); //CHANGE THIS TO SNORT
                }
            } else {
                data->count = 1;
                data->timestamp = now;
            }
        } else {
            struct syn_data new_data = {1, now};
            bpf_map_update_elem(&syn_map, &src_ip, &new_data, BPF_ANY);
        }
    }


    return XDP_PASS;
}

char _license[] SEC("license")="GPL";

