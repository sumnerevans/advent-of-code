#! /usr/bin/env python3

import itertools as it
import math
import sys
from copy import deepcopy
from typing import Generator, Iterable, List, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
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


def seqminmax(sequence: Iterable[int]) -> Tuple[int, int]:
    min_, max_ = math.inf, -math.inf
    for x in sequence:
        min_ = min(min_, x)
        max_ = max(max_, x)
    return int(min_), int(max_)


# Input parsing
with open("inputs/17.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]

grid = [[x == "#" for x in l] for l in lines]

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def print_grid(actives, rrange, crange, zrange):
    # I used this while debugging. It was pretty useful as it printed out the grid.
    for z in range(zrange[0], zrange[1] + 1):
        print("z", z)
        for r in range(rrange[0], rrange[1] + 1):
            for c in range(crange[0], crange[1] + 1):
                print("#" if (r, c, z) in actives else ".", end="")
            print()


def part1() -> int:
    """
    Each of the 6 iterations is O(n^3) where n is the max dimension in any direction.
    """
    actives = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c]:
                actives.add((r, c, 0))

    for _ in range(6):
        newactives = set(actives)

        minR, maxR = seqminmax(a[0] for a in actives)
        minC, maxC = seqminmax(a[1] for a in actives)
        minZ, maxZ = seqminmax(a[2] for a in actives)

        for r in range(minR - 1, maxR + 2):
            for c in range(minC - 1, maxC + 2):
                for z in range(minZ - 1, maxZ + 2):
                    cell = (r, c, z)
                    count = 0
                    for adj_coordinates in grid_adjs(cell):
                        if adj_coordinates in actives:
                            count += 1

                    # Apply the rules.
                    # 1. If the cell is inactive and there are 3 adjacent cells that are
                    #    active, then it becomes active.
                    # 2. If the cell is active, then if there are 2 or 3 adjacent cells
                    #    that are active, then it stays active, otherwise it becomes
                    #    inactive.
                    if cell not in actives:
                        if count == 3:
                            newactives.add(cell)
                    else:  # the cell is active
                        if count not in (2, 3):
                            newactives.remove(cell)

        actives = newactives

    return len(actives)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 218

########################################################################################
print("\nPart 2:")


def part2() -> int:
    """
    Part 2 is the same as part 1, execpt for an added dimension.
    Each of the 6 iterations is O(n^4) where n is the max dimension in any direction.
    """

    actives = set()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c]:
                actives.add((r, c, 0, 0))

    for _ in range(6):
        newactives = set(deepcopy(actives))

        minR, maxR = seqminmax(a[0] for a in actives)
        minC, maxC = seqminmax(a[1] for a in actives)
        minZ, maxZ = seqminmax(a[2] for a in actives)
        minA, maxA = seqminmax(a[3] for a in actives)

        for r in range(minR - 1, maxR + 2):
            for c in range(minC - 1, maxC + 2):
                for z in range(minZ - 1, maxZ + 2):
                    for a in range(minA - 1, maxA + 2):
                        cell = (r, c, z, a)
                        count = 0
                        for x in grid_adjs(cell):
                            if x in actives:
                                count += 1

                        if cell not in actives:
                            if count == 3:
                                newactives.add(cell)
                        else:  # the cell is active
                            if count not in (2, 3):
                                newactives.remove(cell)

        actives = newactives

    return len(actives)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 1908
