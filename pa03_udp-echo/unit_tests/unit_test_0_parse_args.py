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
import random

# Create a pirate arrrgv, to take over real argv.
arrrgv = []
for _ in range(5):
    arrrgv.append(random.randint(0, 255))
arrrgv[0] = chr(int(arrrgv[0]))
arrrgv[1] = chr(int(arrrgv[1]))

# save real argv
temp = sys.argv

# overwrite real argv with pirate arrrgv
sys.argv = arrrgv

# Run your code
arglist = udp_echo_client.parse_args()

# Put argv back where it should be.
sys.argv = temp

# test your inputs
assert tuple(arrrgv[1:]) == arglist
