#! /usr/bin/env python3

import functools as ft
import itertools as it
import math
import os
import re
import sys
from copy import deepcopy
from collections import defaultdict
from enum import IntEnum
from typing import Dict, Generator, Iterable, List, Match, Optional, Sized, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Constants
INF = float("inf")
COMPASS_GRID_DIRS: List[Tuple[int, int]] = [  # Tuples of (delta_row, delta_col)
    (0, 1),  # right
    (1, 0),  # below
    (0, -1),  # left
    (-1, 0),  # above
]
DIAG_GRID_DIRS: List[Tuple[int, int]] = [  # Tuples of (delta_row, delta_col)
    (-1, -1),  # top-left
    (-1, 1),  # top-right
    (1, -1),  # bottom-left
    (1, 1),  # bottom-right
]
GRID_DIRS: List[Tuple[int, int]] = COMPASS_GRID_DIRS + DIAG_GRID_DIRS


# Utilities
def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


def grid_adjs(
    row: int,
    col: int,
    max_row: int,
    max_col: int,
    dirs: List[Tuple[int, int]] = GRID_DIRS,
) -> Generator[Tuple[int, int], None, None]:
    """
    Yields all of the adjacent in-bounds (row, col) tuples in the directions specified
    in `dir`.
    """
    # Iterate through all of the directions and return all of the (row, col) tuples
    # representing the adjacent cells.
    for dy, dx in dirs:
        if 0 <= row + dy < max_row and 0 <= col + dx < max_col:
            yield row + dy, col + dx


def manhattan(x1: int, y1: int, x2: int = 0, y2: int = 0) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def pbits(num: int, pad: int = 32) -> str:
    """Return the bits of `num` in binary with the given padding."""
    return bin(num)[2:].zfill(pad)


def rot(
    x: float, y: float, deg: float, origin: Tuple[float, float] = (0, 0)
) -> Tuple[float, float]:
    """
    Rotate a point by `deg` around the `origin`. This does floating-point math, so
    you may encounter precision errors.
    """
    theta = deg * math.pi / 180
    x2 = (x - origin[0]) * math.cos(theta) - (y - origin[1]) * math.sin(theta)
    y2 = (x - origin[0]) * math.sin(theta) + (y - origin[1]) * math.cos(theta)
    return (x2 + origin[0], y2 + origin[1])


def irot(x: int, y: int, deg: int, origin: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    """
    Rotate an integer point by `deg` around the `origin`. Only works when deg % 90 == 0.
    """
    assert deg % 90 == 0
    for _ in range((deg // 90) % 4):
        x, y = -y, x
    return (x, y)


def sizezip(*iterables: Iterable) -> Generator[Tuple, None, None]:
    assert len(set(len(x) for x in iterables)) == 1  # type: ignore
    yield from zip(*iterables)


# Harvard-Architecture Machine
class OC(IntEnum):
    """Opcodes for the Harvard-architecture machine."""
    jmp = 0  # jump relative to PC+1
    acc = 1  # update accumulator
    nop = 2  # do nothing
    trm = 3  # terminate program


# Change if you add instructions
assert len(OC) == 4
Tape = List[Tuple[OC, Tuple[int, ...]]]


def decode_tape(lines: List[str]) -> Tape:
    return [(OC[c], tuple(int(v) for v in vals)) for c, *vals in map(str.split, lines)]


def run_harvard(tape: Tape, return_acc_if_loop: bool = True):
    a = 0
    pc = 0
    seen = set()
    while True:
        if pc in seen:
            return a if return_acc_if_loop else None

        seen.add(pc)

        oc, vs = tape[pc]
        if oc == OC.trm:
            return a
        elif oc == OC.jmp:
            pc += vs[0] - 1
        elif oc == OC.acc:
            a += vs[0]
        elif oc == OC.nop:
            pass

        pc += 1

    return a


# Input parsing
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
# tape = decode_tape(lines)
# seq = [int(x) for x in lines]
%HERE%
for line in lines:
    pass  # (<>)

# (<>)

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    pass  # (<>)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
# assert test or ans_part1 == (<>)

########################################################################################
print("\nPart 2:")


def part2() -> int:
    pass  # (<>)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
# assert test or ans_part2 == (<>)
