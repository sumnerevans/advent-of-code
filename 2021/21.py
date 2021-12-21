#! /usr/bin/env python3

import functools as ft
import re
import sys
import time
from collections import defaultdict
from typing import Generator, List, Tuple, Iterator

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "inputs/21.txt"
TESTFILENAME = "inputs/21.test.txt"
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


# Modified range functions
def irange(start, end=None, step=1) -> Generator[int, None, None]:
    """Inclusive range function."""
    if end is None:
        start, end = 0, start
    yield from range(start, end + 1, step)


# Utilities
def allints(s: str) -> Iterator[int]:
    """
    Returns a list of all of the integers in the string.
    """
    return map(lambda m: int(m.group(0)), re.finditer(r"-?\d+", s))


def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


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
    p1 = list(allints(lines[0]))[1]
    p2 = list(allints(lines[1]))[1]

    p1score = 0
    p2score = 0
    rolls = 0
    dice_val = 1

    isp1 = True

    while p1score < 1000 and p2score < 1000:
        dice_vals = (dice_val * 3) + 3
        rolls += 3

        if isp1:
            spot = (p1 + dice_vals - 1) % 10 + 1
            p1 = spot
            p1score += spot
        else:
            spot = (p2 + dice_vals - 1) % 10 + 1
            p2 = spot
            p2score += spot

        isp1 = not isp1
        dice_val = (dice_val + 2) % 100 + 1

    return min(p1score, p2score) * rolls


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 739785
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
expected = 503478
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    roll_freq = defaultdict(int)
    for i in irange(1, 3):
        for j in irange(1, 3):
            for k in irange(1, 3):
                roll_freq[i + j + k] += 1

    @cache()
    def wins(
        p1_loc: int, p2_loc: int, p1score: int, p2score: int, isp1: bool
    ) -> Tuple[int, int]:
        if p1score >= 21:
            return (1, 0)
        if p2score >= 21:
            return (0, 1)

        winsp1 = 0
        winsp2 = 0
        if isp1:
            for roll_val, roll_frequency in roll_freq.items():
                spot = (p1_loc + roll_val - 1) % 10 + 1
                wp1, wp2 = wins(spot, p2_loc, p1score + spot, p2score, not isp1)
                winsp1 += roll_frequency * wp1
                winsp2 += roll_frequency * wp2
        else:
            for roll_val, roll_frequency in roll_freq.items():
                spot = (p2_loc + roll_val - 1) % 10 + 1
                wp1, wp2 = wins(p1_loc, spot, p1score, p2score + spot, not isp1)
                winsp1 += roll_frequency * wp1
                winsp2 += roll_frequency * wp2
        return winsp1, winsp2

    p1 = list(allints(lines[0]))[1]
    p2 = list(allints(lines[1]))[1]

    result = max(wins(p1, p2, 0, 0, True))
    print(wins.cache_info())
    return result


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 444356092776315
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
expected = 716241959649754
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
