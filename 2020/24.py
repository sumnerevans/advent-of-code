#! /usr/bin/env python3
"""
This problem requires you to navigate a hexagonal grid. There are many ways of doing
this, but the way I chose was make the indexes in the x direction skip 2 for each cell.

                 (-1,1)   (1,1)
            (-2,0)    (0,0)    (2, 0)
                (-1,-1)   (1,-1)

This is called the "Doubled coordinates" method.
https://www.redblobgames.com/grids/hexagons/#coordinates-doubled

Other ways of doing this are mentioned in the above article, but this is the first one
that my dumb brain was able to figure out.
"""

import sys
import time
from copy import deepcopy
from collections import defaultdict
from typing import List

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


# Input parsing
input_start = time.time()

lines: List[str] = [l.strip() for l in sys.stdin.readlines()]

# Take each string and turn it in to a list of directions that correspond to the dx, dy
# motions necessary.
DIRECTIONS = []
for line in lines:
    i = 0
    directions = []
    while i < len(line):
        c = line[i]

        # East/west motions correspond to |dx| = 2
        if c == "e":
            directions.append((2, 0))
        elif c == "w":
            directions.append((-2, 0))

        # If we go south, then the dy is going to be -1
        elif c == "s":
            c2 = line[i + 1]
            if c2 == "e":
                directions.append((1, -1))
            elif c2 == "w":
                directions.append((-1, -1))

            # This is very important to remember, because if you don't do this, you will
            # read too many "e" or "w"s. (This is what I did, and it screwed me.)
            i += 1

        # If we go north, then the dy is going to be +1
        elif c == "n":
            c2 = line[i + 1]
            if c2 == "e":
                directions.append((1, 1))
            elif c2 == "w":
                directions.append((-1, 1))
            i += 1
        i += 1

    DIRECTIONS.append(directions)

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()


def pos(directions):
    """
    Given a set of directions, figure out the actual index on the (x,y) coordinate grid.
    """
    x, y = 0, 0
    for dx, dy in directions:
        x, y = x + dx, y + dy
    return x, y


# This is a mapping of coord -> is_black
INITIAL_FLIPPED = defaultdict(bool)
for c in DIRECTIONS:
    position = pos(c)
    INITIAL_FLIPPED[position] = not INITIAL_FLIPPED[position]

shared_end = time.time()

# Part 1
########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    """
    All we do is count the number of `True`s in the values of the flipped dictionary.
    """
    return list(INITIAL_FLIPPED.values()).count(True)


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 332

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    def adjs(x, y):
        """Get the adjacent tiles to the given coordinate."""
        return (
            (x + 2, y),  # e
            (x - 2, y),  # w
            (x + 1, y + 1),  # ne
            (x + 1, y - 1),  # se
            (x - 1, y + 1),  # nw
            (x - 1, y - 1),  # sw
        )

    blacks = INITIAL_FLIPPED

    for _ in range(100):
        newblacks = deepcopy(blacks)

        # Find the set of tiles that need to be evaluated. Any tile that is either
        # currently flipped or is adjacent to a currently flipped tile needs to be
        # evaluated.
        looks = set()
        for k in (x[0] for x in blacks.items() if x[1]):
            looks = looks.union(set(adjs(*k)))
            looks.add(k)

        for l in looks:  # for each tile that needs to be evaluated...
            # Count number of active adjacent tiles.
            active_adjs = 0
            for ax, ay in adjs(*l):
                if blacks[(ax, ay)]:
                    active_adjs += 1

            if blacks[l]:  # black
                # Any black tile with zero or more than 2 black tiles immediately
                # adjacent to it is flipped to white.
                if active_adjs == 0 or active_adjs > 2:
                    newblacks[l] = False  # white
            else:  # white
                # Any white tile with exactly 2 black tiles immediately adjacent to it
                # is flipped to black.
                if active_adjs == 2:
                    newblacks[l] = True

        blacks = newblacks

    return list(blacks.values()).count(True)


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = [3763]
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 3900

if debug:
    input_parsing = input_end - input_start
    shared = shared_end - shared_start
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Shared: {shared * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + shared + part1_time + part2_time) * 1000}ms")
