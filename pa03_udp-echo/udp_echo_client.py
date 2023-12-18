#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
UDP_echo program
Solution using python sockets
Student template
"""
import socket
import time
import sys
import statistics


def parse_args() -> tuple[str, int, int, int]:
    """
    parses the 4 args:
    server_hostname, server_port, num_pings, timeout
    """
    server_hostname = sys.argv[1]
    server_port = int(sys.argv[2])
    num_pings = int(sys.argv[3])
    timeout = int(sys.argv[4])
    return (server_hostname, server_port, num_pings, timeout)


def create_socket(timeout: int) -> socket.socket:
    """Create IPv4 UDP client socket"""
    pass  # delete this and write your code
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)
    return client_socket


def net_stats(
    num_pings: int, rtt_hist: list[float]
) -> tuple[float, float, float, float, float]:
    """
    Computes statistics for loss and timing.
    Mimicks the real ping's statistics.
    Check them out: `ping 127.0.0.1`
    See `man ping` for definitions.
    This is just a math function.
    Don't do any networking here.
    loss, rtt_min, rtt_avg, rtt_max, rtt_mdev
    """
    loss: float = round(((num_pings - len(rtt_hist)) / num_pings), 2) * 100

    rtt_min: float = min(rtt_hist)

    rtt_avg: float = sum(rtt_hist) / len(rtt_hist)

    rtt_max: float = max(rtt_hist)

    rtt_mdev: float = statistics.stdev(rtt_hist)

    return (loss, rtt_min, rtt_avg, rtt_max, rtt_mdev)


def main() -> None:
    SERVER_HOSTNAME, SERVER_PORT, NUM_PINGS, TIMEOUT = parse_args()
    # Get IP from hostname
    SERVER_IP = socket.gethostbyname(SERVER_HOSTNAME)
    # Create the socket
    client_socket = create_socket(timeout=TIMEOUT)

    message = f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {0} {time.asctime()}"

    print(f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {len(message)} bytes of data.")

    rtt_hist = []
    total_time = 0  # = sum of rtt_hist
    for counter in range(NUM_PINGS):
        try:
            message = (
                f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {counter+1} {time.asctime()}"
            )
            client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
            time_start = time.time()
            received = client_socket.recv(4096)
            time_stop = time.time()
            round_trip_time = round((time_stop - time_start), 2) * 1000
            rtt_hist.append(round_trip_time)
            if received.decode()[:4] == "oops":
                print("Damaged packet")
            else:
                print(
                    f"{len(received)} bytes from {SERVER_HOSTNAME} ({SERVER_IP}): ping_seq={counter+1} time={int(round_trip_time)} ms"
                )
        except TimeoutError:
            print("timed out")
    total_time = int(sum(rtt_hist))
    # ping stats
    loss, rtt_min, rtt_avg, rtt_max, rtt_mdev = net_stats(
        num_pings=NUM_PINGS, rtt_hist=rtt_hist
    )

    # print endLabel
    print(f"\n--- {SERVER_HOSTNAME} ping statistics ---")

    print(
        f"{NUM_PINGS} packets transmitted, {len(rtt_hist)} received, {int(loss)}% packet loss, time {int(total_time)}ms"
    )

    if (0.0, 0.0, 0.0, 0.0) != (rtt_min, rtt_avg, rtt_max, rtt_mdev):
        print(
            f"rtt min/avg/max/mdev = {int(rtt_min)}/{int(rtt_avg)}/{int(rtt_max)}/{int(round(rtt_mdev))} ms"
        )


if __name__ == "__main__":
    main()
