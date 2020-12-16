#! /usr/bin/env python3

import re
import sys
from copy import deepcopy
from typing import List, Match, Optional

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Constants
# Utilities
def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


# Input parsing
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]

# Keep track of where we are in the file.
endrules = False
endyours = False

rules = {}  # rule name -> ((low1, high1), (low2, high2))
yours = []  # your ticket
nearby = []  # the nearby tickets

for line in lines:
    if line.startswith("your") or line.startswith("nearby"):
        continue
    if line == "":
        if not endrules:
            endrules = True
        elif not endyours:
            endyours = True
        continue

    if not endrules:
        rn, *ranges = rematch(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", line).groups()
        ranges = [int(x) for x in ranges]
        rules[rn] = (tuple(ranges[:2]), tuple(ranges[2:]))
    elif not endyours:
        yours = [int(x) for x in line.split(",")]
    else:
        nearby.append([int(x) for x in line.split(",")])

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    scan_error_rate = 0
    for ticket in nearby:
        for field in ticket:
            inrange = False
            for ranges in rules.values():
                for low, high in ranges:
                    if low <= field <= high:
                        inrange = True
                        break
                if inrange:
                    break

            if not inrange:
                scan_error_rate += field
                break

    return scan_error_rate


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 20058

########################################################################################
print("\nPart 2:")


def part2() -> int:
    possibles = {i: set(rules.keys()) for i in range(len(nearby[0]))}
    for ticket in nearby:
        isinvalid = False
        for field in ticket:
            fieldvalid = False
            for rn, ranges in rules.items():
                for l, h in ranges:
                    if l <= field <= h:
                        fieldvalid = True
                        break
                if fieldvalid:
                    break

            if not fieldvalid:
                isinvalid = True
                break

        # Don't process invalid tickets
        if isinvalid:
            continue

        for i, field_value in enumerate(ticket):
            new_possibles = set(deepcopy(possibles[i]))
            for field_name in possibles[i]:
                (a, b), (c, d) = rules[field_name]
                if not (a <= field_value <= b) and not (c <= field_value <= d):
                    new_possibles.remove(field_name)
            possibles[i] = new_possibles

    # Calculate a mapping of the index to the field it must be.
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
            possibles[x].remove(truemap[remove_idx])

    # Calculate the product of all of the ticket fields in my ticket.
    prod = 1
    for i, field in truemap.items():
        if field.startswith("departure"):
            prod *= yours[i]

    return prod


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 366871907221
