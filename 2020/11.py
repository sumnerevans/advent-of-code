#! /usr/bin/env python3

import copy
import itertools as it
import math
import os
import re
import sys
from collections import defaultdict
from enum import IntEnum
from functools import partial, lru_cache
from typing import Dict, List, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Constants
INF = float("inf")


# Input parsing
A = [[x for x in l.strip()] for l in sys.stdin.readlines()]
lines = copy.deepcopy(A)

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def adjs(r, c):
    if r > 0:
        yield r - 1, c
        if c > 0:
            yield r - 1, c - 1
        if c < len(lines[0]) - 1:
            yield r - 1, c + 1
    if c > 0:
        yield r, c - 1
        if r > 0:
            yield r - 1, c - 1
        if r < len(lines) - 1:
            yield r + 1, c - 1

    if r < len(lines) - 1:
        yield r + 1, c
        if c > 0:
            yield r + 1, c - 1
        if c < len(lines[0]) - 1:
            yield r + 1, c + 1

    if c < len(lines[0]) - 1:
        yield r, c + 1
        if r < len(lines) - 1:
            yield r + 1, c + 1
        if r > 0:
            yield r - 1, c + 1


def part1():
    prev = copy.deepcopy(lines)
    i = 0
    while True:
        new = copy.deepcopy(prev)
        for r in range(len(lines)):
            for c in range(len(lines[0])):
                if prev[r][c] in "L#":
                    num_o = 0
                    for a_r, a_c in set(adjs(r, c)):
                        assert a_r >= 0 and a_c >= 0
                        if prev[a_r][a_c] == "#":
                            num_o += 1

                    if num_o == 0:
                        new[r][c] = "#"
                    if num_o >= 4:
                        new[r][c] = "L"

        neq = False
        for x, y in zip(prev, new):
            for a, b in zip(x, y):
                if a != b:
                    neq = True
                    break
            if neq:
                break

        if not neq:
            # Return the count of all of the occupied seats (marked with '#')
            return "".join("".join(p) for p in prev).count("#")

        i += 1
        prev = new


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 2424

########################################################################################
print("\nPart 2:")


def rays(r, c):
    C = len(lines[0])
    R = len(lines)

    # right
    if c < C:
        yield [(r, x) for x in range(c + 1, C)]

    # left
    if c > 0:
        yield [(r, x) for x in range(c - 1, -1, -1)]

    # down
    if r > 0:
        yield [(x, c) for x in range(r - 1, -1, -1)]

    # up
    if r < R:
        yield [(x, c) for x in range(r + 1, R)]

    # diags
    def diag(dx, dy):
        a = r + dy
        b = c + dx
        x = []
        while a >= 0 and b >= 0 and a < R and b < C:
            x.append((a, b))
            a += dy
            b += dx
        return x

    yield diag(1, 1)
    yield diag(1, -1)
    yield diag(-1, -1)
    yield diag(-1, 1)
    # print(diag(-1, 1))
    # ohea


# print("\n".join(map(str, rays(0, 9))))
# ohea


def part2():
    prev = copy.deepcopy(lines)
    i = 0
    while True:
        # print()
        # print('\n'.join(["".join(p) for p in prev]))
        # if i > 2:
        #     break
        new = copy.deepcopy(prev)
        for r in range(len(lines)):
            for c in range(len(lines[0])):
                if prev[r][c] in "L#":
                    num_o = 0
                    # if (r, c) == (1, 9):
                    #     print(r, c, list(rays(r, c)))
                    for ray in rays(r, c):
                        # print(ray)
                        for r_r, r_c in ray:
                            if prev[r_r][r_c] in "L#":
                                if prev[r_r][r_c] == "#":
                                    num_o += 1
                                break

                    # print(num_o)
                    if num_o == 0:
                        new[r][c] = "#"
                    if num_o >= 5:
                        new[r][c] = "L"

        neq = False
        for x, y in zip(prev, new):
            for a, b in zip(x, y):
                if a != b:
                    neq = True
                    break
            if neq:
                break

        if not neq:
            return "".join("".join(p) for p in prev).count("#")

        i += 1
        prev = new


ans_part2 = part2()
print("ohea", ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
# assert test or ans_part2 == (<>)
