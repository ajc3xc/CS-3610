#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Simplified ICMP-based ping
"""

import socket
import os
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    csum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        thisVal = ord(source_string[count + 1]) * 256 + ord(source_string[count])
        csum = csum + thisVal
        csum = csum & 0xFFFFFFFF
        count = count + 2
    if count_to < len(source_string):
        csum = csum + ord(source_string[len(source_string) - 1])
        csum = csum & 0xFFFFFFFF
    csum = (csum >> 16) + (csum & 0xFFFF)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xFFFF
    # Swap bytes.
    answer = answer >> 8 | (answer << 8 & 0xFF00)
    return answer


def receive_one_ping(my_socket, ID, timeout, dest_addr):
    """
    receive the ping from the socket.
    """
    timeLeft = timeout
    while True:
        startedSelect = time.time()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = time.time() - startedSelect
        # Timeout
        if whatReady[0] == []:
            return "Request timed out."
        timeReceived = time.time()
        rec_packet, addr = my_socket.recvfrom(1024)
        # Fetch the ICMPHeader from the IP
        icmpHeader = rec_packet[20:28]
        raw_ttl = struct.unpack("s", rec_packet[8])[0]
        # binascii -- Convert between binary and ASCII
        TTL = int(binascii.hexlify(str(raw_ttl)), 16)

        icmp_type, code, checksum, packet_ID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
        if packet_ID == ID:
            byte = struct.calcsize("d")
            time_sent = struct.unpack("d", rec_packet[28 : 28 + byte])[0]
            return "Reply from %s: bytes=%d time=%f5ms TTL=%d" % (
                dest_addr,
                len(rec_packet),
                (timeReceived - time_sent) * 1000,
                TTL,
            )
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def send_one_ping(my_socket, dest_addr, ID):
    """
    Send one ping to the given >dest_addr<.
    """
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)
    # Get the checksum, and put in the header
    my_checksum = socket.htons(my_checksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    packet = header + data
    # AF_INET address must be tuple, not str
    my_socket.sendto(packet, (dest_addr, 1))
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def do_one_ping(dest_addr, timeout):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    icmp = socket.getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type.
    # For more details:
    # http://sock-raw.org/papers/sock_raw
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    # Return the current process i
    my_ID = os.getpid() & 0xFFFF
    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, my_ID, timeout, dest_addr)
    my_socket.close()
    return delay


def ping(host, timeout=1):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    # timeout=1 means: If one second goes by without a reply from the server,
    # client assumes that either client's ping or the server's pong is lost
    dest = socket.gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Send ping requests to a server separated by approximately one second
    while True:
        delay = do_one_ping(dest, timeout)
        print(delay)
        # one second
        time.sleep(1)
    return delay


if __name__ == "__main__":
    # ping("mst.edu")
    ping("127.0.0.1")
