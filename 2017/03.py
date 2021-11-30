#! /usr/bin/env python3

import itertools as it
import sys
import time
from typing import Dict, Generator, List, Tuple

test = False
debug = False
stdin = False
INFILENAME = "inputs/03.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/03.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


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
                elif not inclusive and not (low < coord[i] + d < high):
                    inbounds = False
                    break
            if not inbounds:
                continue

        yield tuple(c + d for c, d in zip(coord, delta))


def manhattan(x1: int, y1: int, x2: int = 0, y2: int = 0) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines()]

X = int(lines[0])

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    grid = {}
    x = 0
    y = 0
    d = (1, 0)
    for i in range(1, X + 1):
        grid[(x, y)] = i
        x += d[0]
        y += d[1]
        if -(x - 1) == y and x > 0:
            d = (0, 1)
        elif x == y and x > 0:
            d = (-1, 0)
        elif x < 0 and -x == y:
            d = (0, -1)
        elif x == y and x < 0:
            d = (1, 0)

    for (a, b), v in grid.items():
        if v == X:
            return manhattan(0, 0, a, b)
    assert False


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = [537, 538, 589]
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 419

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    ans = 0

    grid: Dict[Tuple[int, int], int] = {(0, 0): 1}

    def sum_adjs(coord):
        s = 0
        for a in grid_adjs(coord):
            if grid.get(a):
                s += grid[a]
        return s

    x = 1
    y = 0
    d = (0, 1)

    for _ in range(1, X + 1):
        grid[(x, y)] = sum_adjs((x, y))
        if grid[(x, y)] > X:
            return grid[(x, y)]

        x += d[0]
        y += d[1]
        if -(x - 1) == y and x > 0:
            d = (0, 1)
        elif x == y and x > 0:
            d = (-1, 0)
        elif x < 0 and -x == y:
            d = (0, -1)
        elif x == y and x < 0:
            d = (1, 0)

    return ans


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 295229

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
