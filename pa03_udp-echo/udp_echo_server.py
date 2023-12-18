#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Given server code (already works)
"""
import random
import socket
import time

# for auto-grading...
random.seed(a=42)

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Assign IP address and port number to socket
server_socket.bind(("", 12000))

try:
    while True:
        # Receive the client packet along with the address it is coming from
        message, address = server_socket.recvfrom(1024)
        dur = random.choice(range(100, 500, 10)) / 1000  # time in seconds (100-500ms)
        goal = time.time() + dur

        message_str = message.decode()
        # Generate random number in the range of 0 to 10
        rand = random.randint(0, 10)
        # If rand is less is than 4, we consider the packet lost and do not respond
        if rand < 4:
            # simulates lost packet
            continue
        # Otherwise, the server responds
        elif rand == 4:
            # simulates packet error
            message = b"oops" + message[4:]
        while time.time() < goal:
            pass
        server_socket.sendto(message, address)
except Exception as e:
    print("Exception occured: ")
    print(e)
except:
    print("An un-caught exception occured (maybe you killed the server)")
finally:
    server_socket.close()
