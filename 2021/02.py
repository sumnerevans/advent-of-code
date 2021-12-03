#! /usr/bin/env python3

import re
import sys
import time
from typing import List, Match, Optional

test = False
debug = False
stdin = False
INFILENAME = "inputs/02.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/02.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


# Utilities
def rematch(pattern: str, s: str) -> Optional[Match]:
    return re.fullmatch(pattern, s)


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines()]

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    f = 0
    dep = 0
    for l in lines:
        d, n = rematch(r"(\w+) (\d+)", l).groups()
        n = int(n)
        if d == "forward":
            f += n
        elif d == "down":
            dep += n
        elif d == "up":
            dep -= n
        else:
            assert False

    return f * dep


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 2073315
if expected is not None:
    assert test or ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    f = 0
    dep = 0
    a = 0
    for l in lines:
        d, n = rematch(r"(\w+) (\d+)", l).groups()
        n = int(n)
        if d == "forward":
            f += n
            dep += n * a
        elif d == "down":
            a += n
        elif d == "up":
            a -= n

    return f * dep


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 1840311528
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
