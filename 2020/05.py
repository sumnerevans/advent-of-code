#! /usr/bin/env python3

import math
import re
import sys

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


# Input parsing

lines = [l.strip() for l in sys.stdin.readlines()]

########################################################################################
print("Part 1:")
sids = set()


def part1():
    max_sid = 0
    for l in lines:
        bf = l[:7]
        lr = l[7:]

        low, hi = 0, 127

        for d in bf:
            m = math.ceil(low + (hi - low) / 2)
            if d == "B":
                low = m
            else:
                hi = m

        row = low

        low, hi = 0, 7
        for d in lr:
            m = math.ceil(low + (hi - low) / 2)
            if d == "R":
                low = m
            else:
                hi = m

        col = low
        sid = row * 8 + col
        if sid > max_sid:
            max_sid = sid

        sids.add(sid)

    return max_sid


ans_part1 = part1()
print(ans_part1)

# Regression Test
assert test or ans_part1 == 987

########################################################################################
print("\nPart 2:")


def part2():
    for i in range(max(sids) + 1):
        if i - 1 in sids and i + 1 in sids and i not in sids:
            return i


ans_part2 = part2()
print(ans_part2)

# Regression Test
assert test or ans_part2 == 603
