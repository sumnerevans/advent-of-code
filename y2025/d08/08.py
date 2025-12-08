#! /usr/bin/env python3

import functools as ft
import heapq
import itertools as it
import math
import operator
import os
import re
import string
import sys
import time
from collections import defaultdict
from copy import deepcopy
from enum import Enum, IntEnum
from fractions import Fraction
from typing import (Callable, Dict, Generator, Iterable, Iterator, List, Match, Optional, Set,
                    Tuple, TypeVar, Union)

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "08.txt"
TESTFILENAME = "08.test.01.txt"
for arg in sys.argv:
    if arg == "--notest":
        TEST = False
    if arg == "--debug":
        DEBUG = True
    if arg == "--stdin":
        STDIN = True


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Utilities
def allints(s: str) -> Iterator[int]:
    """
    Returns a list of all of the integers in the string.
    """
    return map(lambda m: int(m.group(0)), re.finditer(r"-?\d+", s))


def prod(it: Iterable):
    return ft.reduce(operator.mul, it, 1)


print(f"\n{'=' * 30}\n")

# Read the input
if STDIN:
    input_lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        input_lines: List[str] = [l.strip() for l in f.readlines()]

# Try and read in the test file.
try:
    with open(TESTFILENAME) as f:
        test_lines: List[str] = [l.strip() for l in f.readlines()]
except Exception:
    test_lines = []


# Shared
########################################################################################


def dist(c1, c2):
    return abs((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2 + (c2[2] - c1[2]) ** 2)


@ft.cache
def construct_graph(lines):
    coords = [tuple(allints(line)) for line in lines]

    G = defaultdict(lambda: defaultdict(lambda: float("inf")))
    for i, c1 in enumerate(coords):
        for j, c2 in enumerate(coords):
            if i <= j:
                continue
            d = dist(c1, c2)
            G[i][j] = min(G[i][j], d)

    edges = sorted([(d, a, b) for a, x in G.items() for b, d in x.items()])

    return coords, G, edges


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    coords, G, edges = construct_graph(tuple(lines))
    parents = [i for i in range(len(coords))]

    n = 10 if test else 1000

    def follow(p):
        if parents[p] == p:
            return p
        root = follow(parents[p])
        parents[p] = root
        return root

    for e in edges[:n]:
        p1 = follow(e[1])
        p2 = follow(e[2])
        if p1 == p2:
            continue
        parents[p1] = p2

    counts = defaultdict(int)
    for x in parents:
        counts[follow(x)] += 1

    return prod(sorted(counts.values())[-3:])


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 40
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part1 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part1} != {expected}{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part1)
        print()

part1_start = time.time()
print("Running input...")
ans_part1 = part1(input_lines)
part1_end = time.time()
print("Result:", ans_part1)

tries = [
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 123930
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    coords, G, edges = construct_graph(tuple(lines))
    parents = [i for i in range(len(coords))]

    n = 10 if test else 1000

    def follow(p):
        if parents[p] == p:
            return p
        root = follow(parents[p])
        parents[p] = root
        return root

    ans = 0
    for e in edges:
        p1 = follow(e[1])
        p2 = follow(e[2])
        if p1 == p2:
            continue
        parents[p1] = p2
        ans = coords[e[1]][0] * coords[e[2]][0]

        counts = defaultdict(int)
        for x in parents:
            counts[follow(x)] += 1
        if len(counts) == 1:
            return ans


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 25272
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part2} != {expected}{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part2)
        print()

part2_start = time.time()
print("Running input...")
ans_part2 = part2(input_lines)
part2_end = time.time()
print("Result:", ans_part2)

tries2 = [
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 27338688
if expected is not None:
    assert ans_part2 == expected

if DEBUG:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
