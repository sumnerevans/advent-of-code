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
INFILENAME = "11.txt"
TEST1FILENAME = "11.test.01.txt"
TEST2FILENAME = "11.test.02.txt"
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


print(f"\n{'=' * 30}\n")

# Read the input
if STDIN:
    input_lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        input_lines: List[str] = [l.strip() for l in f.readlines()]

# Try and read in the test file.
try:
    with open(TEST1FILENAME) as f:
        test1_lines: List[str] = [l.strip() for l in f.readlines()]
    with open(TEST2FILENAME) as f:
        test2_lines: List[str] = [l.strip() for l in f.readlines()]
except Exception:
    test1_lines = []
    test2_lines = []


# Shared
########################################################################################


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    devices = {}
    for line in lines:
        d, outs = line.split(": ")
        outputs = outs.split()
        devices[d] = outs.split()

    def count(curr):
        if curr == "out":
            return 1
        return sum(count(x) for x in devices[curr])

    return count("you")


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test1_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test1_lines, test=True)
        expected = 5
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
expected = 431
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    devices = {}
    for line in lines:
        d, outs = line.split(": ")
        outputs = outs.split()
        devices[d] = outs.split()

    @ft.cache
    def count(curr, p1, p2):
        if curr == "out":
            return 1 if p1 and p2 else 0
        if curr == "dac":
            p1 = True
        if curr == "fft":
            p2 = True
        return sum(count(x, p1, p2) for x in devices[curr])

    return count("svr", False, False)


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test2_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test2_lines, test=True)
        expected = 2
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
expected = None  # (<>)
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
