#! /usr/bin/env python3

import functools as ft
import itertools as it
import heapq
import math
import operator
import os
import re
import string
import sys
import time
from copy import deepcopy
from collections import defaultdict
from enum import IntEnum
from typing import (
    Dict,
    Generator,
    Iterable,
    List,
    Match,
    Optional,
    Set,
    Sequence,
    Sized,
    Tuple,
    TypeVar,
    Union,
)

test = False
debug = False
stdin = False
INFILENAME = "inputs/15.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/15.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


# Type variables
K = TypeVar("K")
V = TypeVar("V")


# Utilities
def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


def chunk(iterable, n):
    if n < 1:
        raise Exception("not allowed")
    itertype = type(iterable) if type(iterable) in (list, set, tuple) else list

    container = []
    for x in iterable:
        container.append(x)
        if len(container) == n:
            yield itertype(container)
            container = []

    if len(container) > 0:
        yield itertype(container)


class Tape(List):
    def __init__(self, initial_tape_state):
        self.tape = list(initial_tape_state)

    def __len__(self):
        return len(self.tape)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if idx < len(self.tape):
                return self.tape[idx]
            else:
                return 0

        start = idx.start
        stop = idx.stop
        step = idx.step

        max_idx = max(start, stop)
        if max_idx >= len(self.tape):
            # Off the end of the tape, expand the tape to that point.
            self.tape.extend([0 for _ in range(max_idx - len(self.tape) + 1)])

        return self.tape[start:stop:step]

    def __setitem__(self, idx, value):
        if idx < 0:
            raise IndexError("Cannot set negative indexes on the tape.")

        if idx >= len(self.tape):
            # Off the end of the tape, expand the tape to that point.
            self.tape.extend([0 for _ in range(idx - len(self.tape) + 1)])

        self.tape[idx] = value

    def __str__(self):
        return str(self.tape)


def machine(tape: Tape, inputs):
    pc = 0
    relative_base = 0
    inputs = iter(inputs)

    def digits(number, n=None, default=0):
        digits = []
        while number > 0:
            digits.append(number % 10)
            number //= 10

        # Fill in the rest with the default.
        if n is not None:
            while len(digits) < n:
                digits.append(default)

        return digits

    def decode_instr(i):
        opcode = i % 100
        modes = tuple(x for x in digits(i // 100, n=3))
        return opcode, modes

    def get_value(idx, mode) -> int:
        if mode == 0:
            return tape[idx]
        elif mode == 1:
            return idx
        elif mode == 2:
            return tape[relative_base + idx]

    def set_value(idx, mode, value):
        if mode == 0:
            tape[idx] = value
        elif mode == 1:
            raise Exception("Immediate mode does not work on a dest parameter")
        elif mode == 2:
            tape[relative_base + idx] = value

    while True:
        opcode, (m1, m2, m3) = decode_instr(tape[pc])
        pc_inc = 0
        if opcode == 1:
            pc_inc = 4
            in1, in2, out = tape[pc + 1 : pc + 4]
            set_value(out, m3, get_value(in1, m1) + get_value(in2, m2))
        elif opcode == 2:
            pc_inc = 4
            in1, in2, out = tape[pc + 1 : pc + 4]
            set_value(out, m3, get_value(in1, m1) * get_value(in2, m2))
        elif opcode == 3:
            pc_inc = 2
            set_value(tape[pc + 1], m1, int(next(inputs)))
        elif opcode == 4:
            pc_inc = 2
            yield get_value(tape[pc + 1], m1)
        elif opcode == 5:
            cond, jump = tape[pc + 1 : pc + 3]
            if get_value(cond, m1) != 0:
                pc = get_value(jump, m2)
            else:
                pc_inc = 3
        elif opcode == 6:
            cond, jump = tape[pc + 1 : pc + 3]
            if get_value(cond, m1) == 0:
                pc = get_value(jump, m2)
            else:
                pc_inc = 3
        elif opcode == 7:
            pc_inc = 4
            in1, in2, out = tape[pc + 1 : pc + 4]
            set_value(
                out,
                m3,
                1 if get_value(in1, m1) < get_value(in2, m2) else 0,
            )
        elif opcode == 8:
            pc_inc = 4
            in1, in2, out = tape[pc + 1 : pc + 4]
            set_value(
                out,
                m3,
                1 if get_value(in1, m1) == get_value(in2, m2) else 0,
            )
        elif opcode == 9:
            pc_inc = 2
            relative_base += get_value(tape[pc + 1], m1)
        elif opcode == 99:
            return
        else:
            print("!!!!! ERROR !!!!!")
            print(f"BAD OPCODE {opcode}")
            print(f"PC: {pc}")
            print(f"TAPE: {tape}")
            sys.exit(1)

        pc += pc_inc

    print("!!!!! ERROR !!!!!")
    print("Should exit using opcode 99.")
    sys.exit(1)


def dijkstra(G: Dict[K, Iterable[Tuple[int, K]]], start: K, end: K) -> int:
    """
    A simple implementation of Dijkstra's shortest path algorithm for finding the
    shortest path from ``start`` to ``end`` in ``G``.
    """
    Q = []
    for k in G:
        heapq.heappush(Q, (math.inf, k))
    heapq.heappush(Q, (0, start))

    D = {}
    while Q:
        cost, el = heapq.heappop(Q)
        if cost < D.get(el, math.inf):
            D[el] = cost

        for c, x in G[el]:
            heapq.heappush(Q, (cost + c, x))

    return D[end]


def prod(it: Iterable):
    return ft.reduce(operator.mul, it, 1)


def rematch(pattern: str, s: str) -> Optional[Match]:
    return re.fullmatch(pattern, s)


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
    transformed_x = x - origin[0]
    transformed_y = y - origin[1]
    assert deg % 90 == 0
    for _ in range((deg // 90) % 4):
        transformed_x, transformed_y = -transformed_y, transformed_x
    return (transformed_x + origin[0], transformed_y + origin[1])


def sizezip(*iterables: Iterable) -> Generator[Tuple, None, None]:
    assert len(set(len(x) for x in iterables)) == 1  # type: ignore
    yield from zip(*iterables)


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


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines()]

INTAPE = tuple(int(x) for x in lines[0].split(","))

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

# (<>)

shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    ans = 0

    Q = [()]
    M = machine(Tape(INTAPE), ())

    while Q:
        current, *Q = Q
        print(current)

    M = machine(Tape(INTAPE), (int(input()) for _ in it.repeat(1)))
    while True:
        print(next(M))

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
# assert test or ans_part1 == (<>)

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    ans = 0

    # (<>)

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
# assert test or ans_part2 == (<>)

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
