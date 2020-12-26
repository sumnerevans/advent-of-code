#! /usr/bin/env python3

import operator
import re
import sys
from functools import reduce
from typing import Dict, Iterable, List, Match, Optional, Set, TypeVar

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Type variables
K = TypeVar("K")
V = TypeVar("V")


# Utilities
def prod(it: Iterable):
    return reduce(operator.mul, it, 1)


def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


def infer_one_to_one_from_possibles(possibles: Dict[K, Set[V]]):
    """
    This goes through a dictionary of key to potential values and computes the true
    value using simple inference where if a key can only be a single value, then it must
    be that value. For example:

        A -> {X, Y}
        B -> {Y}
        C -> {X, Z}

    then B -> Y, which means that A cannot be Y, thus A must be X, and by the same logic
    C must be Z.
    """
    inferred = {}
    while len(possibles):
        # Find the alergen that only has one ingredient associated with it and pull it
        # out of the possibles dictionary, and remove the ingredient from all of the
        # other sets.
        for idx, possible_fields in possibles.items():
            if len(possible_fields) == 1:
                inferred[idx] = possible_fields.pop()
                remove_idx = idx
                break
        else:  # nobreak
            assert False, "No keys have a single possible value"

        del possibles[remove_idx]
        for x in possibles:
            if inferred[remove_idx] in possibles[x]:
                possibles[x].remove(inferred[remove_idx])

    return inferred


# Input parsing
# I used a state machine of sorts to parse the input today. There are definitely cleaner
# ways of doing this, but this is what came to mind immediately.
# Generally, if you have an input with a few different distinct parts, a state machine
# like this is reasonable.
with open("inputs/16.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]

# Keep track of where we are in the file.
endrules = False
endyours = False

rules = {}  # rule name -> ((low1, high1), (low2, high2))
yours = []  # your ticket
nearby = []  # the nearby tickets

for line in lines:
    if line.startswith("your") or line.startswith("nearby"):  # Discard these lines
        continue
    if line == "":  # Update the state machine state if at an empty line
        if not endrules:
            endrules = True
        elif not endyours:
            endyours = True
        continue

    if not endrules:  # Parse the line as a rule <rule_name>: <bound1> or <bound2>
        rule_name, *ranges = rematch(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", line).groups()
        ranges = [int(x) for x in ranges]
        rules[rule_name] = (tuple(ranges[:2]), tuple(ranges[2:]))
    elif not endyours:  # This is our ticket, parse as a single list.
        yours = [int(x) for x in line.split(",")]
    else:  # This is somebody else's ticket, append to the nearby list.
        nearby.append([int(x) for x in line.split(",")])

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    # The scan error rate is just the sum of all the invalid fields.
    scan_error_rate = 0
    for ticket in nearby:
        # Check that each of the fields have at least one rule for which they are in
        # one of the ranges.
        for field in ticket:
            inrange = False
            for ranges in rules.values():
                (l1, h1), (l2, h2) = ranges
                if l1 <= field <= h1 or l2 <= field <= h2:
                    inrange = True
                    break

            # This field wasn't in any range, so add the field value to the
            # scan_error_rate.
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
    # This variable stores a mapping of index to set of rules that that index could be.
    possibles = {i: set(rules.keys()) for i in range(len(nearby[0]))}

    for ticket in nearby:
        # Detect if the ticket is invalid. If it is, then we won't process it.
        isinvalid = False
        for field in ticket:
            fieldvalid = False
            for ranges in rules.values():
                (l1, h1), (l2, h2) = ranges
                if l1 <= field <= h1 or l2 <= field <= h2:
                    fieldvalid = True
                    break

            if not fieldvalid:
                isinvalid = True
                break

        # Don't process invalid tickets
        if isinvalid:
            continue

        # Go through all of the fields in the ticket and eliminate any possibilities
        # that are impossible given the value of the field and ranges given by the
        # rules.
        # For example, if there is a rule "seat: 2-3 or 5-7", and index 0 of our ticket
        # is 4, then we know that index 0 cannot be "seat".
        for i, field_value in enumerate(ticket):
            new_possibles = set(possibles[i])
            for field_name in possibles[i]:
                (a, b), (c, d) = rules[field_name]
                if not (a <= field_value <= b) and not (c <= field_value <= d):
                    new_possibles.remove(field_name)
            possibles[i] = new_possibles

    # Calculate a mapping of the index to the field it must be.
    inferred = infer_one_to_one_from_possibles(possibles)

    # Calculate the product of all of the ticket fields in my ticket.
    return prod(yours[i] for i, f in inferred.items() if f.startswith("departure"))


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 366871907221
