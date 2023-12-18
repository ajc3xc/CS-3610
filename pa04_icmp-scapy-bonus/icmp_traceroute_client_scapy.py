#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Mimic ICMP traceroute with scapy
"""
import time
import sys
from scapy.all import *  # type: ignore
from socket import gethostbyname, gethostbyaddr

# https://scapy.readthedocs.io/en/latest/troubleshooting.html
conf.L3socket = L3RawSocket  # type: ignore
# sometimes needed for default gateway, and
# always for localhost, and
# sometimes not for remote.


def main() -> None:
    print("Delete this and write your code")



if __name__ == "__main__":
    main()
