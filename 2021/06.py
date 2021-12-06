#! /usr/bin/env python3

import sys
import time
from collections import defaultdict
from typing import List

test = True
debug = False
stdin = False
INFILENAME = "inputs/06.txt"
TESTFILENAME = "inputs/06.test.txt"
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


def calculate_lanternfish(start_seq: List[int], iterations: int) -> int:
    """
    This calculate function aggregates all of the lanternfish at the same stage in life
    together to keep track of them.

    Each day, all lanternfish at ``0`` days before they create a new lanternfish become
    a ``6`` and starts a new lanternfish initialized at ``8`` to the end of the list,
    while each other number decreases by ``1`` if it was present at the start of the
    day.
    """
    number_of_laternfish = defaultdict(int)
    for x in start_seq:
        number_of_laternfish[x] += 1

    for _ in range(iterations):
        new_number_of_lanternfish = defaultdict(int)
        for k, v in number_of_laternfish.items():
            if k == 0:
                # v lanternfishes is at 0, make `v` new lanternfishes, and reset all of
                # the lanternfish at 0 to 6.
                new_number_of_lanternfish[8] += v
                new_number_of_lanternfish[6] += v
            else:
                new_number_of_lanternfish[k - 1] += v
        number_of_laternfish = new_number_of_lanternfish

    return sum(number_of_laternfish.values())


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    return calculate_lanternfish([int(x) for x in lines[0].split(",")], 80)


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 5934
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part1 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part1}{bcolors.ENDC}")
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
expected = 372984
if expected is not None:
    assert test or ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    return calculate_lanternfish([int(x) for x in lines[0].split(",")], 256)


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 26984457539
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part2}{bcolors.ENDC}")
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
expected = 1681503251694
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
