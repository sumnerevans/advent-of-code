#! /usr/bin/env python3

import functools as ft
import itertools as it
import heapq
import math
import operator
import os
import re
import string
import sys
import time
from copy import deepcopy
from collections import defaultdict
from enum import IntEnum
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Match,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

test = False
debug = False
stdin = False
INFILENAME = "inputs/03.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/03.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


# Type variables
K = TypeVar("K")
V = TypeVar("V")


# Utilities
def bitstrtoint(s: Union[str, List]) -> int:
    if isinstance(s, list):
        s = "".join(map(str, s))
    return int(s, 2)


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines()]

# seq = [int(x) for x in lines]


input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    # Calculate frequencies of the lines
    freq0 = [0] * len(lines[0])
    freq1 = [0] * len(lines[0])

    for line in lines:
        for i, c in enumerate(line):
            if c == "0":
                freq0[i] += 1
            else:
                freq1[i] += 1

    # Store the bitmap as a list of integers
    gamma = [0 if zeros > ones else 1 for (zeros, ones) in zip(freq0, freq1)]

    # Epsilon is just the complement of gamma
    epsilon = [1 if x == 0 else 0 for x in gamma]
    return bitstrtoint(gamma) * bitstrtoint(epsilon)


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 1092896
if expected is not None:
    assert test or ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    xs = deepcopy(lines)
    ys = deepcopy(lines)

    I = 0

    while I < 100:
        print("===================" * 2)
        print("===================" * 2)
        print(I)
        print("===================" * 2)
        print("===================" * 2)
        print("===================" * 2)
        print(xs)
        print(ys)
        freq0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        freq1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        freq0y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        freq1y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for line in xs:
            for i, c in enumerate(line):
                if c == "0":
                    freq0[i] += 1
                else:
                    freq1[i] += 1

        for line in ys:
            for i, c in enumerate(line):
                if c == "0":
                    freq0y[i] += 1
                else:
                    freq1y[i] += 1

        def x(y, i):
            new_y = []

            if freq0[i] <= freq1[i]:  # 1
                for w in y:
                    if w[i] == "1":
                        new_y.append(w)
            else:
                for w in y:
                    if w[i] == "0":
                        new_y.append(w)
            return new_y

        def y(y, i):
            print("i", i)
            new_y = []
            if freq0y[i] <= freq1y[i]:  # 1
                print("USE 1")
                for w in y:
                    if w[i] == "0":
                        new_y.append(w)
            else:
                for w in y:
                    if w[i] == "1":
                        new_y.append(w)
            return new_y

        if len(xs) > 1:
            xs = x(xs, I)

        if len(ys) > 1:
            ys = y(ys, I)
        I += 1

        if len(xs) == 1 == len(ys):
            print(int("".join(map(str, xs[0])), 2))
            print(int("".join(map(str, ys[0])), 2))
            return (int("".join(map(str, xs[0])), 2)) * (
                int("".join(map(str, ys[0])), 2)
            )


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 4672151
if expected is not None:
    assert test or ans_part2 == expected

if debug:
    input_parsing = input_end - input_start
    shared = shared_end - shared_start
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Shared: {shared * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + shared + part1_time + part2_time) * 1000}ms")
