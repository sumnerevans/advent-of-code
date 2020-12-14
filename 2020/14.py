#! /usr/bin/env python3

import functools as ft
import itertools as it
import math
import os
import re
import sys
from copy import deepcopy
from collections import defaultdict
from enum import IntEnum
from typing import Dict, List, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


def pbits(num, pad=32):
    return bin(num)[2:].zfill(pad)


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    mem = {}
    andmask = 1
    ormask = 0
    for line in lines:
        if rematch("mask.*", line):
            andmask = 1
            ormask = 0
            for x in rematch("mask = (.*)", line).group(1):
                andmask = andmask << 1
                ormask = ormask << 1
                if x != "0":
                    andmask |= 1
                if x == "1":
                    ormask |= 1
        else:
            loc, val = map(int, rematch(r"mem\[(\d+)\] = (\d+)", line).groups())
            mem[loc] = (val & andmask) | ormask

    return sum(mem.values())


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = [16073107098]
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 6386593869035

########################################################################################
print("\nPart 2:")


def part2():
    mem = {}
    curmask = ""

    for line in lines:
        if rematch("mask.*", line):
            curmask = rematch("mask = (.*)", line).group(1)
        else:
            loc, val = map(int, rematch(r"mem\[(\d+)\] = (\d+)", line).groups())

            result_bits = ""
            access = pbits(loc, len(curmask))
            for cl, cm in zip(access, curmask):
                if cm == "0":
                    result_bits += cl
                elif cm == "1":
                    result_bits += "1"
                else:
                    result_bits += "X"

            for bit_combo in it.product("01", repeat=result_bits.count("X")):
                real_loc = ""
                combo_idx = 0
                for b in result_bits:
                    if b in "01":
                        real_loc += b
                    else:
                        real_loc += bit_combo[combo_idx]
                        combo_idx += 1

                mem[int(real_loc, 2)] = val

    return sum(mem.values())


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 4288986482164
