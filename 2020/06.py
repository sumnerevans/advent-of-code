#! /usr/bin/env python3

import itertools
import math
import os
import re
import sys
from collections import defaultdict
from functools import partial
from typing import Dict, List, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


# Input parsing

lines = [l.strip() for l in sys.stdin.readlines()]
groups = []
groups2 = []
current = set()
current2 = []
for line in lines:
    if line == "":
        groups.append(current)
        groups2.append(current2)
        current = set()
        current2 = []
    else:
        for c in line:
            current.add(c)
        current2.append(line)

groups.append(current)
groups2.append(current2)

########################################################################################
print("Part 1:")


def part1():
    return sum(len(g) for g in groups)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print('Tries Part 1:', tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 6382

########################################################################################
print("\nPart 2:")


def part2():
    s = 0
    for g in groups2:
        for c in "abcdefghijklmnopqrstuvwxyz":
            no = False
            for p in g:
                if c not in p:
                    no = True
                    break

            if not no:
                s += 1

    return s


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print('Tries Part 2:', tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 3197
