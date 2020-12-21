#! /usr/bin/env python3
"""
Today's problem was very fun. It involved
"""

import functools as ft
import itertools as it
import math
import re
import sys
from copy import deepcopy
from typing import Generator, List, Match, Optional, Tuple

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


# Utilities
def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


# Input parsing
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]

TILES = {}
currentid = 0
current = []
for line in lines:
    if line == "":
        TILES[currentid] = current

    elif rematch(r"Tile (\d+):", line):
        currentid = int(rematch(r"Tile (\d+):", line).group(1))
        current = []
    else:
        current.append([x == "#" for x in line])

TILES[currentid] = current  # luckily I remembered this


# A few utilities for this problem.
def printtile(tile):
    """Print a tile. If a tile ID is passed, look it up in the TILES dictionary."""
    if isinstance(tile, int):
        tile = TILES[tile]

    for row in tile:
        for col in row:
            print("#" if col else ".", end="")
        print()


def print_assignments(assignments):
    """
    Print an entire assignments array. This can be used at the very end to print the
    picture.
    """
    for r in assignments:
        print(r)
    for row in assignments:
        print()
        sidelen = len(TILES[row[0][0]])
        rowlines = ["" for _ in range(sidelen)]

        for col, rotation, flip in row:
            for i in range(len(rowlines)):
                rowlines[i] += " "
            pic = TILES[col]
            if flip:
                pic = [list(reversed(x)) for x in pic]
            for _ in range(rotation):
                pic = list(zip(*pic[::-1]))
            for i, row in enumerate(pic):
                rowlines[i] += "".join([".#"[int(x)] for x in row])
        for row in rowlines:
            print(row)


# Functions to actually solve the problem
########################################################################################
# The following section contains the core functionality of stitching together the
# picture. I implemented all of this for part 1 because I didn't realize that you can
# just cheeze it by checking how many shared edges each tile has.


def edges(tile) -> Generator[Tuple[Tuple[int, ...], str, bool], None, None]:
    """Returns a generator of (edge, "r|b|l|t", flipped(bool)) for the given tile"""
    yield (tuple(tile[0]), "t", False)  # top
    yield (tuple(reversed(tile[0])), "t", True)  # top flipped
    yield (tuple(tile[-1]), "b", False)  # bottom
    yield (tuple(reversed(tile[-1])), "b", True)  # bottom flipped

    left = tuple(r[0] for r in tile)
    yield left, "l", False  # left
    yield tuple(reversed(left)), "l", True  # left flipped

    right = tuple(r[-1] for r in tile)
    yield right, "r", False  # right
    yield tuple(reversed(right)), "r", True  # right flipped


# Calculate the edges of every tile.
tile_rot_side_to_edge = {}

for tid, tile in TILES.items():
    for e in edges(tile):
        edge, side, reverse = e
        tile_rot_side_to_edge[(tid, side, reverse)] = edge

SIDELEN = int(math.sqrt(len(TILES)))
TIDS = set(TILES)

ROTS = [
    0,  # no rot
    1,  # right 90
    2,  # right 180
    3,  # right 270
]


@cache()
def getside(tid, rot, flip, side):
    """
    This is pretty ugly, but very useful. It allows you to get a side of a tile after
    rotating it to the right ``rot`` times, and flipping it if ``flip`` is True.

    I'm sure there's a better way, but I have no idea at this point.

    This function caused me a lot of pain, since I tried to do it without just
    hard-coding all of the rotations and flips. It got to complicated, and I just gave
    up.
    """
    if rot == 0:
        if not flip:
            return tile_rot_side_to_edge[(tid, side, False)]
        else:
            # Flip swaps r <-> l and reverses top and bottom
            if side in "rl":
                side = {"r": "l", "l": "r"}[side]
            reverse = side in "tb"
            return tile_rot_side_to_edge[(tid, side, reverse)]
    elif rot == 1:
        if not flip:
            side, reverse = {
                "t": ("l", True),
                "b": ("r", True),
                "r": ("t", False),
                "l": ("b", False),
            }[side]
            return tile_rot_side_to_edge[(tid, side, reverse)]
        else:
            side = {"t": "r", "b": "l", "r": "t", "l": "b"}[side]
            return tile_rot_side_to_edge[(tid, side, True)]
    elif rot == 2:
        if not flip:
            side = {"t": "b", "b": "t", "r": "l", "l": "r"}[side]
            return tile_rot_side_to_edge[(tid, side, True)]
        else:
            side, reverse = {
                "t": ("b", False),
                "b": ("t", False),
                "r": ("r", True),
                "l": ("l", True),
            }[side]
            return tile_rot_side_to_edge[(tid, side, reverse)]
    elif rot == 3:
        if not flip:
            side, reverse = {
                "t": ("r", False),
                "b": ("l", False),
                "r": ("b", True),
                "l": ("t", True),
            }[side]
            return tile_rot_side_to_edge[(tid, side, reverse)]
        else:
            side = {"t": "l", "b": "r", "r": "b", "l": "t"}[side]
            return tile_rot_side_to_edge[(tid, side, False)]

    assert False


# Tuples of (tid, rot, flipped) for each r, c
Placements = Tuple[Tuple[Tuple[int, int, bool], ...], ...]


def solve(placements: Placements, d=0) -> Optional[Placements]:
    """
    This is a recursive function which, given a set of placements, returns a valid
    configuration of valid placements if it exists, and ``None`` otherwise.
    """
    indent = "  " * d
    if debug:
        print(indent, "solve")
        for row in placements:
            print(indent, [x[0] for x in row])

    # This is the base case of the recursion. If we have filled up the picture, then we
    # can return all of the placements.
    if len(placements) == SIDELEN and all(len(x) == SIDELEN for x in placements):
        return placements

    # Calculate the next tile location to place.
    num_placed = sum(map(len, placements))
    nextloc = (num_placed // SIDELEN, num_placed % SIDELEN)

    # Calculate the possible options for the next tile to place.
    nexttile_opts = set(TIDS) - {cell[0] for row in placements for cell in row}

    # Go through all of the options for theh next tile to place and see if any of them
    # work.
    while len(nexttile_opts):
        nexttile = nexttile_opts.pop()

        # Try all rotations and flips of the next tile
        for flip, rot in it.product((False, True), ROTS):

            # Get the left and top side of the tile to be placed (after handling the
            # rotation and flip) so that we can compare against the adjacent cells.
            left = getside(nexttile, rot, flip, "l")
            top = getside(nexttile, rot, flip, "t")
            row, col = nextloc

            # Check if it works. Only check top and left because we are working from the
            # top left to the bottom right, so we only will ever have to check to the
            # top and left!
            rotworks = True
            if row > 0:
                # Check above
                adj = placements[row - 1][col]
                if getside(*adj, "b") != top:
                    rotworks = False

            if rotworks and col > 0:
                # Check left
                adj = placements[row][col - 1]
                if getside(*adj, "r") != left:
                    rotworks = False

            # This rotation works, recursively call solve with the new placements tuple.
            # This is a fairly stupid way of doing things, but it works, and that's all
            # that matters.
            if rotworks:
                new_placements = [[p for p in r] for r in placements]
                if nextloc[0] >= len(new_placements):
                    new_placements.append([])
                new_placements[-1].append((nexttile, rot, flip))
                return solve(tuple(map(tuple, (p for p in new_placements))), d=d + 1)


# try each tile_id as the placement in the top-left in all orientations
def dosolve() -> Placements:
    for tile_id in TILES:
        for rot in ROTS:
            for flip in (True, False):
                if debug:
                    print("TRY", tile_id, rot, flip)
                s = solve((((tile_id, rot, flip),),), d=0)
                if s is not None:
                    return s

    assert False


assignments = dosolve()
if debug:
    print_assignments(assignments)

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    """
    I had a bug here that cost me at least an hour? maybe more? No idea. I had the index
    on the second one of these wrong (I hard-coded it as 1, instead of -1)
    """
    return (
        assignments[0][0][0]
        * assignments[0][-1][0]
        * assignments[-1][0][0]
        * assignments[-1][-1][0]
    )


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = [6392972187097]
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 8272903687921

########################################################################################
print("\nPart 2:")


def part2() -> int:
    """
    I used a very inefficient and stupid algorithm for this. For each orientation, I am
    just checking every single possible start (row, col) pair of a monster (which is
    really highly unnecessary because monsters cannot overlap).
    """
    sidelen = len(list(TILES.values())[0])

    if debug:
        for row in assignments:
            print(row)

    seamonster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]
    seamonster_r = len(seamonster)
    seamonster_c = len(seamonster[0])

    # This part just stitches together the picture. Making sure to delete the borders.
    alllines = []
    for row in assignments:
        rowlines = [[] for _ in range(sidelen - 2)]

        for col, rotation, flip in row:
            pic = TILES[col]
            if flip:
                pic = [list(reversed(x)) for x in pic]
            for _ in range(rotation):
                pic = list(zip(*pic[::-1]))

            for i, row in list(enumerate(pic[1:-1])):
                rowlines[i].extend([".#"[int(x)] for x in row[1:-1]])

        if debug:
            for row in rowlines:
                print("".join(row))

        alllines.extend(rowlines)

    def turbulence(lines) -> Optional[int]:
        """
        Returns the turbulence if there are monsters in this orientation. It's
        guaranteed that there will be only one configuration that has monsters, so if
        there are no monsters, then this is not the correct orientation.
        """
        R = len(lines)
        C = len(lines[0])
        for r0 in range(R):
            for c0 in range(C):
                is_seamonster = True

                for r, c in it.product(range(seamonster_r), range(seamonster_c)):
                    if debug:
                        print(r, c, r0 + r, c0 + c)
                    if not (0 <= r0 + r < R and 0 <= c0 + c < C):
                        is_seamonster = False
                        break
                    if seamonster[r][c] == "#" and lines[r0 + r][c0 + c] not in "#O":
                        is_seamonster = False
                        break

                if is_seamonster:
                    for r, c in it.product(range(seamonster_r), range(seamonster_c)):
                        if seamonster[r][c] == "#":
                            lines[r0 + r][c0 + c] = "O"

        t = 0
        anyseamonster = False
        for l in lines:
            for c in l:
                if c == "#":
                    t += 1
                if c == "O":
                    anyseamonster = True

        if anyseamonster and debug:
            print("SEAMONSTERS:")
            for row in lines:
                print("".join(row))
        return t if anyseamonster else None

    for rot, flip in it.product(ROTS, (True, False)):
        rotated = deepcopy(alllines)
        if flip:
            rotated = [tuple(reversed(x)) for x in rotated]
        for _ in range(rot):
            rotated = list(zip(*rotated[::-1]))
        rotated = [list(x) for x in rotated]

        t = turbulence(rotated)
        if t:
            return t

    assert False


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 2304
