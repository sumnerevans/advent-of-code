#! /usr/bin/env python3

import math
import string
import sys
import time
from collections import defaultdict
from typing import List

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


# Utilities
def manhattan(x1: int, y1: int, x2: int = 0, y2: int = 0) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


# Input parsing
input_start = time.time()

lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
COORDS = {tuple(map(int, line.split(","))) for line in lines}

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

MIN_X = min(c[0] for c in COORDS) - 200
MAX_X = max(c[0] for c in COORDS) + 200
MIN_Y = min(c[1] for c in COORDS) - 200
MAX_Y = max(c[1] for c in COORDS) + 200

shared_end = time.time()

# Part 1
########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    coord_to_char = dict(zip(COORDS, string.ascii_letters))
    coord_to_num_closest = defaultdict(int)
    exclude_coords = set()

    for x in range(MIN_X, MAX_X + 1):
        for y in range(MAX_Y, MIN_Y - 1, -1):
            min_c = (0, 0)
            min_dist = math.inf
            tie = False
            for (cx, cy) in COORDS:
                dist = manhattan(x, y, cx, cy)
                if dist == min_dist:
                    tie = True
                if dist < min_dist:
                    min_c = (cx, cy)
                    min_dist = dist
                    tie = False

            if tie:
                if debug:
                    print(".", end="")
                pass
            else:
                if debug:
                    print(coord_to_char[min_c], end="")
                coord_to_num_closest[min_c] += 1

                # Exclude any letters on the edges.
                if y == MAX_Y or y == MIN_Y:
                    exclude_coords.add(min_c)
                if x == MAX_X or x == MIN_X:
                    exclude_coords.add(min_c)
        if debug:
            print()

    ans = 0
    for k, v in coord_to_num_closest.items():
        if k in exclude_coords:
            continue
        if v > ans:
            ans = v
    return ans


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 3006

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    TOT_DIST_MAX = 10000 if not test else 32

    region = set()
    for x in range(MIN_X, MAX_X + 1):
        for y in range(MAX_Y, MIN_Y - 1, -1):
            total_dist = 0
            for (cx, cy) in COORDS:
                dist = manhattan(x, y, cx, cy)
                total_dist += dist
                if total_dist >= TOT_DIST_MAX:
                    if debug:
                        print(".", end="")
                    break
            else:  # nobreak
                region.add((x, y))
                if debug:
                    print("#", end="")
        if debug:
            print()

    return len(region)


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 42998

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
