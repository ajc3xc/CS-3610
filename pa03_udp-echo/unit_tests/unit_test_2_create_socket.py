#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Your code tests start here:
# To debug in pudb3
# Highlight the line of code below below
# Type 't' to jump 'to' it
# Type 's' to 'step' deeper
# Type 'n' to 'next' over
# Type 'f' or 'r' to finish/return a function call and go back to caller
import udp_echo_client

student_socket = udp_echo_client.create_socket(timeout=1)

# assert student_socket.family == udp_echo_client.socket.AddressFamily.AF_INET6
assert student_socket.family == udp_echo_client.socket.AddressFamily.AF_INET
assert student_socket.type == udp_echo_client.socket.SocketKind.SOCK_DGRAM
assert student_socket.timeout == 1.0
