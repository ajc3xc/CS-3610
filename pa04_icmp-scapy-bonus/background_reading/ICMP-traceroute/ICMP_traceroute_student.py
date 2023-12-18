#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Simplified ICMP-based traceroute
"""

import socket
import os
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise


def checksum(source_string: bytes) -> int:
    """
    Given the bytes array, it calculates the checksum and returns it.
    """
    # I'm not too confident that this is right but testing seems to
    # suggest that it gives the same answers as in_cksum in ping.c.
    # In this function we make the checksum of our packet
    # hint: see icmpPing lab


def build_packet() -> bytes:
    """
    Create a new echo request packet based on the given "id".
    """
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.
    # Don’t send the packet yet , just return the final packet in this function.
    # So the function ending should look like this
    # Header is type (8), code (8), checksum (16), sequence (16)
    packet = header + data
    return packet


def get_route(hostname: str) -> None:
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            dest_addr = socket.gethostbyname(hostname)
            # SOCK_RAW is a powerful socket type.
            # For more details:
            # http://sock-raw.org/papers/sock_raw
            # Fill in start
            # Make a raw socket named mySocket
            # Fill in end
            # setsockopt method is used to set the time-to-live field.
            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack("I", ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = time.time() - startedSelect
                # Timeout
                if whatReady[0] == []:
                    print("... Request timed out.")
                recvPacket, addr = mySocket.recvfrom(1024)
                time_received = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    print("... Request timed out.")
            except socket.timeout:
                continue
            else:
                # Fill in start
                # Fetch the ICMP type and code from the received packet
                # Fill in end
                if types == 11:
                    bytes = struct.calcsize("d")
                    time_sent = struct.unpack("d", recvPacket[28 : 28 + bytes])[0]
                    print(
                        " %d rtt=%.0f ms %s"
                        % (ttl, (time_received - t) * 1000, addr[0])
                    )
                elif types == 3:
                    bytes = struct.calcsize("d")
                    time_sent = struct.unpack("d", recvPacket[28 : 28 + bytes])[0]
                    print(
                        " %d rtt=%.0f ms %s"
                        % (ttl, (time_received - t) * 1000, addr[0])
                    )
                elif types == 0:
                    bytes = struct.calcsize("d")
                    time_sent = struct.unpack("d", recvPacket[28 : 28 + bytes])[0]
                    print(
                        " %d rtt=%.0f ms %s"
                        % (ttl, (time_received - time_sent) * 1000, addr[0])
                    )
                    return
                else:
                    print("error")
                break
            finally:
                mySocket.close()

if __name__ == "__main__":
    get_route("mst.edu")
    # get_route("127.0.0.1")
