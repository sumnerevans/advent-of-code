#! /usr/bin/env python3

import sys
import time
from typing import List

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "inputs/25.txt"
TESTFILENAME = "inputs/25.test.txt"
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
    with open(TESTFILENAME) as f:
        test_lines: List[str] = [l.strip() for l in f.readlines()]
except Exception:
    test_lines = []


# Shared
########################################################################################


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    cucumbers = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == ">":
                cucumbers[r, c] = ">"
            elif char == "v":
                cucumbers[r, c] = "v"

    R = len(lines)
    C = len(lines[0])

    i = 0
    while True:
        i += 1
        new_after_east_migrate = {}

        # east first
        for (r, c), x in cucumbers.items():
            if x == ">" and (r, (c + 1) % C) not in cucumbers:
                new_after_east_migrate[r, (c + 1) % C] = ">"
            else:
                new_after_east_migrate[r, c] = cucumbers[r, c]

        new_after_south_migrate = {}
        for (r, c), x in new_after_east_migrate.items():
            if x == "v" and ((r + 1) % R, c) not in new_after_east_migrate:
                new_after_south_migrate[(r + 1) % R, c] = "v"
            else:
                new_after_south_migrate[r, c] = new_after_east_migrate[r, c]

        if new_after_south_migrate == cucumbers:
            break

        cucumbers = new_after_south_migrate

    return i


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 58
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
expected = 579
if expected is not None:
    assert ans_part1 == expected

if DEBUG:
    part1_time = part1_end - part1_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"TOTAL: {part1_time * 1000}ms")
