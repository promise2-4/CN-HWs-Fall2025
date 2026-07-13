#!/usr/bin/env python3
"""Small ICMP Echo Request experiment using Scapy."""

import time

from scapy.all import ICMP, IP, sr1


def my_custom_ping(dest_ip: str) -> None:
    packet = IP(dst=dest_ip) / ICMP(id=555, seq=1)

    print(f"Sending echo request to: {dest_ip}")
    start_time = time.time()
    answer = sr1(packet, timeout=2, verbose=False)
    end_time = time.time()

    if answer:
        rtt_ms = (end_time - start_time) * 1000
        print(f"Got reply from {answer.src}")
        print(f"Round Trip Time: {rtt_ms:.2f} ms")
        answer.show()
    else:
        print("No response (timeout or unreachable)")


if __name__ == "__main__":
    print("--- Test 1: Google DNS ---")
    my_custom_ping("8.8.8.8")

    print("\n--- Test 2: Unreachable Host ---")
    my_custom_ping("192.168.1.222")
