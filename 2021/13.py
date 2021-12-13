#! /usr/bin/env python3

import re
import sys
import time
from typing import Generator, List, Match, Optional

test = True
debug = False
stdin = False
INFILENAME = "inputs/13.txt"
TESTFILENAME = "inputs/13.test.txt"
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


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    dots = set()
    folds = []

    dotsover = False
    for line in lines:
        if line == "":
            dotsover = True
        elif not dotsover:
            x, y = map(int, line.split(","))
            dots.add((y, x))
        else:
            d, x = rematch(r"fold along (x|y)=(\d+)", line).groups()
            folds.append((d, int(x)))

    axis, fold_loc = folds[0]
    new_dots = set()
    for r, c in dots:
        if axis == "y":
            if r > fold_loc:
                new_dots.add((fold_loc - (r - fold_loc), c))
            else:
                new_dots.add((r, c))
        else:
            if c > fold_loc:
                new_dots.add((r, fold_loc - (c - fold_loc)))
            else:
                new_dots.add((r, c))

    return len(new_dots)


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 17
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
    738,
    794
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 655
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> str:
    dots = set()
    folds = []
    dotsover = False
    for line in lines:
        if line == "":
            dotsover = True
        elif not dotsover:
            dots.add(tuple(reversed(tuple(map(int, line.split(","))))))
        else:
            d, x = rematch(r"fold along (x|y)=(\d+)", line).groups()
            folds.append((d, int(x)))

    for axis, fold_loc in folds:
        new_dots = set()
        for r, c in dots:
            if axis == "y":
                if r > fold_loc:
                    new_dots.add((fold_loc - (r - fold_loc), c))
                else:
                    new_dots.add((r, c))
            else:
                if c > fold_loc:
                    new_dots.add((r, fold_loc - (c - fold_loc)))
                else:
                    new_dots.add((r, c))

        dots = new_dots

    output = ""
    max_row = max(a[0] for a in dots)
    max_col = max(a[1] for a in dots)
    for r in irange(max_row):
        for c in irange(max_col):
            output += '#' if (r, c) in dots else '.'
        output += "\n"
    return output.strip()


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = """
#####
#...#
#...#
#...#
#####""".strip()
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part2} != {expected}{bcolors.ENDC}")
            assert False

        print(f"Result:\n{test_ans_part2}")
        print()

part2_start = time.time()
print("Running input...")
ans_part2 = part2(input_lines)
part2_end = time.time()
print(f"Result:\n{ans_part2}")

tries2 = [
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = """
..##.###..####..##..#..#..##..#..#.###.
...#.#..#....#.#..#.#..#.#..#.#..#.#..#
...#.#..#...#..#....#..#.#..#.#..#.#..#
...#.###...#...#....#..#.####.#..#.###.
#..#.#....#....#..#.#..#.#..#.#..#.#.#.
.##..#....####..##...##..#..#..##..#..#""".strip()
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
