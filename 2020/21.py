#! /usr/bin/env python3

import itertools as it
import re
import sys
import time
from collections import defaultdict
from copy import deepcopy
from typing import List, Match, Optional

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


# Utilities
def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


# Input parsing
input_start = time.time()
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]

FOODS = []  # list of all the foods
ALL_INGS_SET = set()
ALL_INGS_OCURRENCES = defaultdict(int)

for line in lines:
    ingredients, contains = rematch(r"(.*) \(contains (.*)\)", line).groups()
    ingredients = ingredients.split()
    contains = contains.split(", ")
    for i in ingredients:
        ALL_INGS_SET.add(i)
        ALL_INGS_OCURRENCES[i] += 1
    FOODS.append((set(ingredients), set(contains)))

input_end = time.time()

# Shared
########################################################################################

shared_start = time.time()

alergen_to_can_be = defaultdict(list)

for ing, alg in FOODS:
    for a in alg:
        alergen_to_can_be[a].append(ing)

NOALERGEN = set(ALL_INGS_SET)
for can_be in alergen_to_can_be.values():
    NOALERGEN -= set.intersection(*can_be)

shared_end = time.time()

# Part 1
########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    return sum(ALL_INGS_OCURRENCES[x] for x in NOALERGEN)


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = [2484]
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 2211

########################################################################################
print("\nPart 2:")


def part2() -> str:
    possibles = defaultdict(lambda: deepcopy(ALL_INGS_SET))

    for a, b in it.product(FOODS, FOODS):
        ing_intersects = b[0] & a[0]
        alg_intersects = b[1] & a[1]
        if len(alg_intersects) == 1:
            alg_name = list(alg_intersects)[0]
            possibles[alg_name] &= ing_intersects - NOALERGEN

    truemap = {}
    while len(possibles):
        remove_idx = 0
        for idx, possible_fields in possibles.items():
            if len(possible_fields) == 1:
                truemap[idx] = list(possible_fields)[0]
                remove_idx = idx
                break

        del possibles[remove_idx]
        for x in possibles:
            if truemap[remove_idx] in possibles[x]:
                possibles[x].remove(truemap[remove_idx])

    return ",".join(v for _, v in sorted(truemap.items()))


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)
assert ans_part2 != ans_part1

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == "vv,nlxsmb,rnbhjk,bvnkk,ttxvphb,qmkz,trmzkcfg,jpvz"

if debug:
    print(f"Input parsing: {(input_end - input_start) * 1000}ms")
    print(f"Shared: {(shared_end - shared_start) * 1000}ms")
    print(f"Part 1: {(part1_end - part1_start) * 1000}ms")
    print(f"Part 2: {(part2_end - part2_start) * 1000}ms")
