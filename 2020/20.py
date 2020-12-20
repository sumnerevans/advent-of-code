#! /usr/bin/env python3

import functools as ft
import itertools as it
import heapq
import math
import operator
import re
import sys
from copy import deepcopy
from enum import IntEnum
from typing import Dict, Generator, Iterable, List, Match, Optional, Tuple, TypeVar

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


def grid_adjs(
    coord: Tuple[int, ...],
    bounds: Tuple[Tuple[int, int], ...] = None,
    inclusive: bool = True,
) -> Generator[Tuple[int, ...], None, None]:
    # Iterate through all of the deltas for the N dimensions of the coord. A delta is
    # -1, 0, or 1 indicating that the adjacent cell is one lower, same level, or higher
    # than the given coordinate.
    for delta in it.product((-1, 0, 1), repeat=len(coord)):
        if all(d == 0 for d in delta):
            # This is the coord itself, skip.
            continue

        if sum(map(abs, delta)) > 1:
            continue

        # Check the bounds
        if bounds is not None:
            inbounds = True
            for i, (d, (low, high)) in enumerate(zip(delta, bounds)):
                if inclusive and not (low <= coord[i] + d <= high):
                    inbounds = False
                    break
                elif not inclusive and not (low <= coord[i] + d <= high):
                    inbounds = False
                    break
            if not inbounds:
                continue

        yield tuple(c + d for c, d in zip(coord, delta))


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

TILES[currentid] = current


def printtile(tile):
    if isinstance(tile, int):
        tile = TILES[tile]

    for row in tile:
        for col in row:
            print("#" if col else ".", end="")
        print()


def print_assignments(assignments):
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


# Shared
########################################################################################


def edges(tile) -> Generator[Tuple[Tuple[int, ...], str, bool], None, None]:
    # returns generator of (edge, "r|b|l|t", flipped(bool))
    # top
    yield (tuple(tile[0]), "t", False)
    # top flipped
    yield (tuple(reversed(tile[0])), "t", True)
    # bottom
    yield (tuple(tile[-1]), "b", False)
    # bottom flipped
    yield (tuple(reversed(tile[-1])), "b", True)

    # left
    left = tuple(r[0] for r in tile)
    yield left, "l", False
    yield tuple(reversed(left)), "l", True  # left flipped

    # right
    right = tuple(r[-1] for r in tile)
    yield right, "r", False
    yield tuple(reversed(right)), "r", True  # right flipped


# edge_to_tile_info = defaultdict(set)
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
SIDE_NAMES = "rblt"


def getside(tid, rot, flip, side):
    if rot == 0:
        if not flip:
            side, flip = {
                "t": ("t", False),
                "b": ("b", False),
                "r": ("r", False),
                "l": ("l", False),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]
        else:
            side, flip = {
                "t": ("t", True),
                "b": ("b", True),
                "r": ("l", False),
                "l": ("r", False),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]
    elif rot == 1:
        if not flip:
            side, flip = {
                "t": ("l", True),
                "b": ("r", True),
                "r": ("t", False),
                "l": ("b", False),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]
        else:
            side, flip = {
                "t": ("r", True),
                "b": ("l", True),
                "r": ("t", True),
                "l": ("b", True),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]
    elif rot == 2:
        if not flip:
            side, flip = {
                "t": ("b", True),
                "b": ("t", True),
                "r": ("l", True),
                "l": ("r", True),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]
        else:
            side, flip = {
                "t": ("b", False),
                "b": ("t", False),
                "r": ("r", True),
                "l": ("l", True),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]
    elif rot == 3:
        if not flip:
            side, flip = {
                "t": ("r", False),
                "b": ("l", False),
                "r": ("b", True),
                "l": ("t", True),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]
        else:
            side, flip = {
                "t": ("l", False),
                "b": ("r", False),
                "r": ("b", False),
                "l": ("t", False),
            }[side]
            return tile_rot_side_to_edge[(tid, side, flip)]

    assert False


# Tuples of (tid, rot, flipped) for each r, c
Placements = Tuple[Tuple[Tuple[int, int, bool]]]


def solve(placements: Placements, d=0) -> Optional[Placements]:
    # indent = " " * d
    if len(placements) == SIDELEN and all(len(x) == SIDELEN for x in placements):
        return placements

    num_placed = sum(map(len, placements))

    nexttile_opts = set(TIDS)
    for r in placements:
        for c in r:
            nexttile_opts.remove(c[0])

    nextloc = (num_placed // SIDELEN, num_placed % SIDELEN)
    nexttile_opts = list(nexttile_opts)

    while len(nexttile_opts):
        nexttile, *nexttile_opts = nexttile_opts
        adjs = tuple(grid_adjs(nextloc, bounds=((0, len(placements)), (0, SIDELEN))))

        # Try all rotations and flips of the next tile
        for flip, rot in it.product((False, True), ROTS):
            # Check if it works
            rotworks = True

            left = getside(nexttile, rot, flip, "l")
            top = getside(nexttile, rot, flip, "t")

            # Check if it works. Only check top and left because grids!
            for r, c in adjs:
                if r >= len(placements) or c >= len(placements[r]):
                    continue
                adj = placements[r][c]
                # is left
                if r == nextloc[0] and c < nextloc[1]:
                    if getside(*adj, "r") != left:
                        rotworks = False
                        break
                # is above
                if r < nextloc[0]:
                    if getside(*adj, "b") != top:
                        rotworks = False
                        break

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
                print("TRY", tile_id, rot, flip)
                s = solve((((tile_id, rot, flip),),), d=0)
                if s is not None:
                    return s

    assert False


assignments = dosolve()
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
    sidelen = len(list(TILES.values())[0])

    for row in assignments:
        print(row)

    seamonster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]
    seamonster_r = len(seamonster)
    seamonster_c = len(seamonster[0])

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

        for row in rowlines:
            print("".join(row))

        alllines.extend(rowlines)

    def turbulence(lines) -> Optional[int]:
        lines = deepcopy(lines)
        R = len(lines)
        C = len(lines[0])
        for r0 in range(R):
            for c0 in range(C):
                is_seamonster = True
                debug = r0 == 16 and c0 == 2 and False

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
        return t if anyseamonster else None

    for rot, flip in it.product(ROTS, (True, False)):
        rotated = deepcopy(alllines)
        if flip:
            rotated = [list(reversed(x)) for x in rotated]
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
