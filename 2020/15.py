#! /usr/bin/env python3

import functools as ft
import itertools as it
import heapq
import math
import os
import re
import sys
from copy import deepcopy
from collections import defaultdict
from enum import IntEnum
from typing import (
    Dict,
    Generator,
    Iterable,
    List,
    Match,
    Optional,
    Sized,
    Tuple,
    TypeVar,
    Union,
)

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Input parsing
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
nums = list(map(int, lines[0].split(",")))


def solve(n: int) -> int:
    """
    This function solves both parts in O(n) time, but O(n^2) space. I tried doing some
    optimizations for it, but honestly, this is fast enough.
    """
    spokens = defaultdict(list)  # keep track of all the times you said every number
    prev = 0
    s = 0

    # This for loop (and actually all of the indexing) is 0-based, but that's OK because
    # all that matters is the difference.
    for i in range(n):
        if i < len(nums):
            # still in the initial seed
            s = nums[i]
        else:
            if len(spokens[prev]) < 2:
                # the previous number was said 0 or 1 times, say "0"
                s = 0
            else:
                # the previous number was said at i-1 and at the second-to-last index of
                # spokens[prev]. Compute the difference and say it.
                s = (i - 1) - spokens[prev][-2]

        # Reset prev note that this number was said at time `i`.
        prev = s
        spokens[s].append(i)
    return s


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    return solve(2020)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 639

########################################################################################
print("\nPart 2:")


def part2() -> int:
    return solve(30_000_000)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 266
