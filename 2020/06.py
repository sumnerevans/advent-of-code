#! /usr/bin/env python3

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
groups = []
current = []
for line in lines:
    if line == "":
        groups.append(current)
        current = []
    else:
        current.append(set(line))

groups.append(current)

########################################################################################
print("Part 1:")


def part1():
    """
    This part is just a sum of the number of letters in the *union* of all of the
    responses for each group.
    """
    return sum(len(set.union(*g)) for g in groups)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 6382

########################################################################################
print("\nPart 2:")


def part2():
    """
    This part is just a sum of the number of letters in the *intersection* of all of the
    responses for each group.
    """
    return sum(len(set.intersection(*g)) for g in groups)

    # The following was what I implemented when I solved night-of. The nice thing about
    # this method is that it was very easy to think about and I didn't take too much
    # work to bang out.
    s = 0
    for g in groups:
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
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 3197
