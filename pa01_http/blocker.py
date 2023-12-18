#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Blocks connections between client and server.
"""

import socket

server_port = 6789
try:
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client_socket.connect(("", server_port))
    while True:
        pass
except:
    print("Blocker stopped")
finally:
    client_socket.close()
