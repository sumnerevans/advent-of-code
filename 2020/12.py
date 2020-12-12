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
def rot(x, y, deg, origin=(0, 0)):
    theta = deg * math.pi / 180
    x2 = round((x - origin[0]) * math.cos(theta) - (y - origin[1]) * math.sin(theta))
    y2 = round((x - origin[0]) * math.sin(theta) + (y - origin[1]) * math.cos(theta))
    return (x2 + origin[0], y2 + origin[1])


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]
actions = []
for line in lines:
    actions.append((line[0], int(line[1:])))


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    pos = (0, 0)
    facing = (1, 0)
    for c, v in actions:
        if c == "N":
            # Action N means to move north by the given value.
            pos = (pos[0], pos[1] + v)
        if c == "S":
            # Action S means to move south by the given value.
            pos = (pos[0], pos[1] - v)
        if c == "E":
            # Action E means to move east by the given value.
            pos = (pos[0] + v, pos[1])
        if c == "W":
            # Action W means to move west by the given value.
            pos = (pos[0] - v, pos[1])
        if c == "F":
            # Action F means to move forward by the given value in the direction the
            # ship is currently facing.
            pos = (pos[0] + v * facing[0], pos[1] + v * facing[1])
        if c == "L":
            # Action L means to turn left the given number of degrees.
            facing = dirs[(dirs.index(facing) + v // 90) % 4]
        if c == "R":
            # Action R means to turn right the given number of degrees.
            facing = dirs[(dirs.index(facing) - v // 90) % 4]

    return abs(pos[0]) + abs(pos[1])


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 1186

########################################################################################
print("\nPart 2:")


def part2():
    pos = (0, 0)
    wp = (10, 1)
    for c, v in actions:
        if c == "N":
            wp = (wp[0], wp[1] + v)
        if c == "S":
            wp = (wp[0], wp[1] - v)
        if c == "E":
            wp = (wp[0] + v, wp[1])
        if c == "W":
            wp = (wp[0] - v, wp[1])
        if c == "F":
            pos = (pos[0] + v * wp[0], pos[1] + v * wp[1])
        if c == "L":
            wp = rot(*wp, v)
        if c == "R":
            wp = rot(*wp, -v)
    return abs(pos[0]) + abs(pos[1])


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 47806
