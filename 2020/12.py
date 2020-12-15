#! /usr/bin/env python3

import sys
from typing import Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def irot(x: int, y: int, deg: int, origin: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    """
    Rotate an integer point by `deg` around the `origin`. Only works when deg % 90 == 0.
    """
    transformed_x = x - origin[0]
    transformed_y = y - origin[1]
    assert deg % 90 == 0
    for _ in range((deg // 90) % 4):
        transformed_x, transformed_y = -transformed_y, transformed_x
    return (transformed_x + origin[0], transformed_y + origin[1])


def manhattan(x1: int, y1: int, x2: int = 0, y2: int = 0) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]
actions = []
for line in lines:
    actions.append((line[0], int(line[1:])))


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    pos = (0, 0)
    facing = (1, 0)
    for c, v in actions:
        if c == "N":
            # Action N means to move north by the given value.
            pos = (pos[0], pos[1] + v)
        if c == "S":
            # Action S means to move south by the given value.
            pos = (pos[0], pos[1] - v)
        if c == "E":
            # Action E means to move east by the given value.
            pos = (pos[0] + v, pos[1])
        if c == "W":
            # Action W means to move west by the given value.
            pos = (pos[0] - v, pos[1])
        if c == "F":
            # Action F means to move forward by the given value in the direction the
            # ship is currently facing.
            pos = (pos[0] + v * facing[0], pos[1] + v * facing[1])
        if c == "L":
            # Action L means to turn left the given number of degrees.
            facing = dirs[(dirs.index(facing) + v // 90) % 4]
        if c == "R":
            # Action R means to turn right the given number of degrees.
            facing = dirs[(dirs.index(facing) - v // 90) % 4]

    return manhattan(pos[0], pos[1])


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 1186

########################################################################################
print("\nPart 2:")


def part2() -> int:
    pos = (0, 0)
    wp = (10, 1)
    for c, v in actions:
        if c == "N":
            wp = (wp[0], wp[1] + v)
        if c == "S":
            wp = (wp[0], wp[1] - v)
        if c == "E":
            wp = (wp[0] + v, wp[1])
        if c == "W":
            wp = (wp[0] - v, wp[1])
        if c == "F":
            pos = (pos[0] + v * wp[0], pos[1] + v * wp[1])
        if c == "L":
            wp = irot(*wp, v)
        if c == "R":
            wp = irot(*wp, -v)
    return manhattan(pos[0], pos[1])


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 47806
