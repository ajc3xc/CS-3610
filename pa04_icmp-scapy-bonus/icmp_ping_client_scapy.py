#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Mimic ICMP ping with scapy
"""
import time
import sys
import statistics
import random
from scapy.all import *  # type: ignore
from socket import gethostbyname

# https://scapy.readthedocs.io/en/latest/troubleshooting.html
conf.L3socket = L3RawSocket  # type: ignore
# sometimes needed for default gateway, and
# always for localhost, and
# sometimes not for remote.


def parse_args() -> tuple[str, int, int]:
    """
    parses the 3 args:
    server_hostname, num_pings, timeout
    """
    print("Delete this and write your code")

def net_stats(
    num_pings: int, rtt_hist: list[float]
) -> tuple[float, float, float, float, float]:
    """
    Computes statistics for loss and timing.
    Mimicks the real ping's statistics.
    Check them out: `ping 127.0.0.1`
    See `man ping` for definitions.
    """
    print("Delete this and write your code")



def main() -> None:
    print("Delete this and write your code")

if __name__ == "__main__":
    main()
