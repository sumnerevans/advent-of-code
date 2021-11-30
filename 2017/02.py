#! /usr/bin/env python3

import math
import sys
import time
from typing import Iterable, List, Tuple

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
def seqminmax(sequence: Iterable[int]) -> Tuple[int, int]:
    """
    Returns a tuple containing the minimum and maximum element of the ``sequence``.
    """
    min_, max_ = math.inf, -math.inf
    for x in sequence:
        min_ = min(min_, x)
        max_ = max(max_, x)
    return int(min_), int(max_)


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines()]

S = [[int(x) for x in line.split()] for line in lines]

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()


shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    ans = 0

    # For each row, determine the difference between the largest value and the smallest
    # value; the checksum is the sum of all of these differences.

    for r in S:
        i, x = seqminmax(r)
        ans += x - i

    return ans


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 45351

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    ans = 0

    def x(r) -> int:
        # Find the only two numbers in each row where one evenly divides the other -
        # that is, where the result of the division operation is a whole number. Then
        # return the division of the largest over the smallest.
        for i, x1 in enumerate(r):
            for j, x2 in enumerate(r):
                if i != j:
                    if x1 % x2 == 0 or x2 % x1 == 0:
                        if x1 > x2:
                            return x1 // x2
                        else:
                            return x2 // x1
        assert False

    for r in S:
        ans += x(r)

    return ans


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 275

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
