#! /usr/bin/env python3

import functools as ft
import sys
from collections import defaultdict

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]
seq = sorted([int(x) for x in lines])

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    ones = 1
    threes = 1
    for x, y in zip(seq, seq[1:]):
        if y - x == 1:
            ones += 1
        if y - x == 3:
            threes += 1
    return ones * threes


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 2263

########################################################################################
print("\nPart 2:")

# Store a mapping of adapter to eligible adapters to plug in.
Es = defaultdict(set)
Es[0] = {1, 2, 3}
m = max(seq)
Es[m].add(m + 3)
for i, s in enumerate(seq):
    for k in seq[i + 1 :]:
        if abs(s - k) <= 3:
            Es[s].add(k)


# Count the number of paths to the end of the chain.
@cache()
def paths(x):
    if m + 3 in Es[x]:
        return 1
    return sum(paths(d) for d in Es[x])


def part2():
    return paths(0)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 396857386627072
