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


def float_eq(f1: float, f2: float) -> bool:
    if abs(f1 - f2) < 0.0001:
        return True
    return False


# test 1
result = udp_echo_client.net_stats(5, [20, 30, 40, 50])
goal = (20.0, 20, 35.0, 50, 12.909944487358056)
for f1, f2 in zip(result, goal):
    assert float_eq(f1=f1, f2=f2)

# test 2
result = udp_echo_client.net_stats(10, [30, 40, 60, 60])
goal = (60.0, 30, 47.5, 60, 15.0)
for f1, f2 in zip(result, goal):
    assert float_eq(f1=f1, f2=f2)
