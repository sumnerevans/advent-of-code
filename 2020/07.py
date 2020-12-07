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
dependencies = defaultdict(list)
dependencies2 = defaultdict(list)
# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
for line in lines:
    color, rules = rematch(r"(.*) bags contain (.*).", line).groups()
    for rule in rules.split(", "):
        if rule == "no other bags":
            continue
        n, c = rematch(r"(\d+) (.*) bags?", rule).groups()
        dependencies[c].append((int(n), color))
        dependencies2[color].append((int(n), c))

########################################################################################
print("Part 1:")


def part1():
    can = set()
    look = [(1, "shiny gold")]
    while len(look) > 0:
        needs, c = look.pop()
        for d in dependencies[c]:
            can.add(d)
            look.append(d)

    return len(set(x[1] for x in can))


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 151

########################################################################################
print("\nPart 2:")


def part2():
    needs = defaultdict(int)
    look = [(1, "shiny gold")]
    while len(look) > 0:
        N, c = look.pop()
        for n, c1 in dependencies2[c]:
            needs[c1] += n * N
            look.append((N * n, c1))

    return sum(needs.values())


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 41559
