#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
UDP_echo program
Solution using scapy
Solution
"""
import time
import sys
import statistics
from scapy.all import *  # type: ignore

# https://scapy.readthedocs.io/en/latest/troubleshooting.html
conf.L3socket = L3RawSocket  # type: ignore
# sometimes needed for default gateway, and
# always for localhost, and
# sometimes not for remote.


def parse_args() -> tuple[str, int, int, int]:
    """
    parses the 4 args:
    server_hostname, server_port, num_pings, timeout
    """
    # server_hostname, server_port, num_pings, timeout = sys.argv[1:5]
    server_hostname = sys.argv[1]
    server_port = int(sys.argv[2])
    num_pings = int(sys.argv[3])
    timeout = int(sys.argv[4])
    return (server_hostname, server_port, num_pings, timeout)


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
    SERVER_IP = conf.route.route(SERVER_HOSTNAME)[1]  # type: ignore

    message = f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {0} {time.asctime()}"

    print(f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {len(message)} bytes of data.")

    rtt_hist = []
    total_time = 0  # = sum of rtt_hist
    for counter in range(NUM_PINGS):
        message = f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {counter+1} {time.asctime()}"
        package = IP(dst=SERVER_IP) / UDP(dport=SERVER_PORT, sport=SERVER_PORT + 1) / message  # type: ignore
        time_start = time.time()
        received = sr1(package, timeout=TIMEOUT, verbose=0)  # type: ignore
        time_stop = time.time()
        if received is not None:
            received = received[Raw].load  # type: ignore
            round_trip_time = round((time_stop - time_start - 0.02), 1) * 1000
            rtt_hist.append(round_trip_time)
            if received.decode()[:4] == "oops":
                print("Damaged packet")
            else:
                print(
                    f"{len(received)} bytes from {SERVER_HOSTNAME} ({SERVER_IP}): ping_seq={counter+1} time={int(round_trip_time)} ms"
                )
        else:
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
