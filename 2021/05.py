#! /usr/bin/env python3

import re
import sys
import time
from collections import defaultdict
from typing import Iterable, List, Match, Optional, Tuple

test = True
debug = False
stdin = False
INFILENAME = "inputs/05.txt"
TESTFILENAME = "inputs/05.test.txt"
for arg in sys.argv:
    if arg == "--notest":
        test = False
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


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
def rematch(pattern: str, s: str) -> Optional[Match]:
    return re.fullmatch(pattern, s)


print(f"\n{'=' * 30}\n")

# Read the input
if stdin:
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


def parselines(lines: List[str]) -> Iterable[Tuple[Tuple[int, int], Tuple[int, int]]]:
    for line in lines:
        x1, y1, x2, y2 = map(int, rematch(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups())
        yield tuple(sorted(((x1, y1), (x2, y2))))


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    """
    For part 1, you only have to consider horizontal and vertical lines. That is, lines
    where either x1 = x2 or y1 = y2.
    """
    G = defaultdict(int)
    for (x1, y1), (x2, y2) in parselines(lines):
        if x1 != x2 and y1 != y2:
            # This technique works for part 1 because x1 = x2 or y1 = y2 so sorting will
            # actually do what we want (which is to put the one that is smaller first,
            # making the range based for loop work better later).
            continue

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                G[(x, y)] += 1

    return sum([1 for x in G.values() if x > 1])


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 5
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part1 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
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
expected = 4826
if expected is not None:
    assert test or ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    G = defaultdict(int)
    for (x1, y1), (x2, y2) in parselines(lines):
        if x1 == x2 or y1 == y2:
            # Horizontal or vertical
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    G[(x, y)] += 1
        else:
            # Must calculate scope because math. Basic algebra that I literally forgot.
            slope = 1 if y2 > y1 else -1
            for i in range(abs(x1 - x2) + 1):
                G[(x1 + i, y1 + (i * slope))] += 1

    return sum([1 for x in G.values() if x > 1])


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 12
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part2)

part2_start = time.time()
print("Running input...")
ans_part2 = part2(input_lines)
part2_end = time.time()
print("Result:", ans_part2)

tries2 = [
    12730,
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 16793
if expected is not None:
    assert test or ans_part2 == expected

if debug:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
