#! /usr/bin/env python3

import re
import sys
import time
from typing import Generator, List, Match, Optional

test = True
debug = False
stdin = False
INFILENAME = "inputs/17.txt"
TESTFILENAME = "inputs/17.test.txt"
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


# Modified range functions
def irange(start, end=None, step=1) -> Generator[int, None, None]:
    """Inclusive range function."""
    if end is None:
        start, end = 0, start
    yield from range(start, end + 1, step=step)


# Utilities
def rematch(pattern: str, s: str) -> Match:
    match = re.fullmatch(pattern, s)
    assert match is not None
    return match


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
def simulate(
    initial_x_vel: int,
    initial_y_vel: int,
    x1: int,
    x2: int,
    y1: int,
    y2: int,
) -> Optional[int]:
    X, Y = 0, 0
    dx, dy = initial_x_vel, initial_y_vel
    max_y = 0
    hit_target = False
    while X <= x2 and Y >= y1 and not hit_target:
        # On each step, these changes occur in the following order:

        # The probe's x position increases by its x velocity.
        X += dx
        # The probe's y position increases by its y velocity.
        Y += dy
        # Due to drag, the probe's x velocity changes by 1 toward the value 0;
        # that is, it decreases by 1 if it is greater than 0, increases by 1 if
        # it is less than 0, or does not change if it is already 0.
        if dx != 0:
            dx = dx - 1 if dx > 0 else dx + 1

        # Due to gravity, the probe's y velocity decreases by 1.
        dy -= 1

        max_y = max(max_y, Y)

        if x1 <= X <= x2 and y1 <= Y <= y2:
            hit_target = True

    return max_y if hit_target else None


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    ans = 0

    x1, x2, y1, y2 = map(
        int,
        rematch(r".*x=([-\d]+)..([-\d]+), y=([-\d]+)..([-\d]+)", lines[0]).groups(),
    )

    for initial_x_vel in range(0, 100):
        for initial_y_vel in range(0, abs(y1)):
            sim_result = simulate(initial_x_vel, initial_y_vel, x1, x2, y1, y2)
            if sim_result is not None:
                ans = max(ans, sim_result)

    return ans


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 45
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
    4950
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 7875
if expected is not None:

    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    ans = 0

    x1, x2, y1, y2 = map(
        int,
        rematch(r".*x=([-\d]+)..([-\d]+), y=([-\d]+)..([-\d]+)", lines[0]).groups(),
    )

    for initial_x_vel in irange(0, x2):
        for initial_y_vel in range(y1, 300):
            sim_result = simulate(initial_x_vel, initial_y_vel, x1, x2, y1, y2)
            if sim_result is not None:
                ans += 1

    return ans


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 112
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
    929
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 2321
if expected is not None:
    assert ans_part2 == expected

if debug:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
