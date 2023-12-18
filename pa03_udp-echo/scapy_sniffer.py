#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from scapy.layers.inet import UDP  # type: ignore
from scapy.layers.l2 import Ether  # type: ignore
from scapy.sendrecv import sniff  # type: ignore

server_dst_port = 12000


def handle_packet(packet: Ether) -> None:
    message = packet[UDP].load.decode()

    time_str = message[-24:]
    time_float = time.mktime(time.strptime(time_str))

    diff = time.time() - time_float
    if abs(diff) > 10:
        print(f"Received '{time_str}'; Time differed by {diff:.2f} seconds")
    else:
        print("Time match")


sniff(
    filter=f"udp and dst port {server_dst_port}",
    prn=handle_packet,
    count=26,
    store=False,
    iface="lo",
)
