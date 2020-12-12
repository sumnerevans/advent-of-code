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

# Constants
INF = float('inf')
COMPASS_GRID_DIRS = [  # Tuples of (delta_row, delta_col)
    (-1, 0),  # above
    (1, 0),  # below
    (0, -1),  # left
    (0, 1),  # right
]
DIAG_GRID_DIRS = [  # Tuples of (delta_row, delta_col)
    (-1, -1),  # top-left
    (-1, 1),  # top-right
    (1, -1),  # bottom-left
    (1, 1),  # bottom-right
]
GRID_DIRS = COMPASS_GRID_DIRS + DIAG_GRID_DIRS


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


def grid_adjs(row, col, max_row, max_col, dirs=GRID_DIRS):
    # Iterate through all of the directions and return all of the (row, col) tuples
    # representing the adjacent cells.
    for dy, dx in dirs:
        if 0 <= row + dy < max_row and 0 <= col + dx < max_col:
            yield row + dy, col + dx


def rot(x, y, deg, origin=(0, 0)):
    theta = deg * math.pi / 180
    x2 = round((x - origin[0]) * math.cos(theta) - (y - origin[1]) * math.sin(theta))
    y2 = round((x - origin[0]) * math.sin(theta) + (y - origin[1]) * math.cos(theta))
    return (x2 + origin[0], y2 + origin[1])


# Crazy Machine
class OC(IntEnum):
    jmp = 0  # jump relative to PC+1
    acc = 1  # update accumulator
    nop = 2  # do nothing
    trm = 3  # terminate program


# Change if you add instructions
assert len(OC) == 4


def decode_tape(lines):
    ops = []
    for line in lines:
        opcode, *vals = line.split()
        ops.append((OC[opcode], tuple(int(v) for v in vals)))
    return ops


def run_machine(tape, return_acc_if_loop=True):
    a = 0
    pc = 0
    seen = set()
    while True:
        if pc in seen:
            return a if return_acc_if_loop else None

        seen.add(pc)

        oc, vs = tape[pc]
        if oc == OC.trm:
            return a
        elif oc == OC.jmp:
            pc += vs[0] - 1
        elif oc == OC.acc:
            a += vs[0]
        elif oc == OC.nop:
            pass

        pc += 1

    return a


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]
# tape = decode_tape(lines)
# seq = [int(x) for x in lines]
%HERE%
for line in lines:
    pass  # (<>)

# (<>)

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    pass  # (<>)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
# assert test or ans_part1 == (<>)

########################################################################################
print("\nPart 2:")


def part2():
    pass  # (<>)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
# assert test or ans_part2 == (<>)
