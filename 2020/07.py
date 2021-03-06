#! /usr/bin/env python3

import re
import sys
from collections import defaultdict
from typing import List

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


# Input parsing
with open("inputs/07.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]

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
        dependencies[c].append(color)
        dependencies2[color].append((int(n), c))

########################################################################################
print("Part 1:")


def part1():
    can = set()
    look = ["shiny gold"]
    while len(look) > 0:
        c = look.pop()
        for d in dependencies[c]:
            can.add(d)
            look.append(d)

    return len(can)


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
            needs[c1] += N * n
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
