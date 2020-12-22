#! /usr/bin/env python3

import functools as ft
import itertools as it
import heapq
import math
import operator
import os
import re
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
    Sized,
    Tuple,
    TypeVar,
    Union,
)

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


# Type variables
K = TypeVar("K")
V = TypeVar("V")


# Utilities
def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


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
input_start = time.time()
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]

DECKP1 = []
DECKP2 = []

p2 = False
for line in lines:
    if line.startswith("Player"):
        continue
    if line == "":
        p2 = True
        continue
    if not p2:
        DECKP1.append(int(line))
    else:
        DECKP2.append(int(line))

input_end = time.time()

# Part 1
########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    dp1 = deepcopy(DECKP1)
    dp2 = deepcopy(DECKP2)

    # Loop until one player has all the cards.
    tot = len(dp1) + len(dp2)
    while len(dp1) < tot and len(dp2) < tot:
        # Pull of the top of each deck. This is where having pattern matching that isn't
        # terrible would be nice. Or having a Queue in the stdlib that isn't impossible
        # to remember how to use.
        c1, *dp1r = dp1
        c2, *dp2r = dp2

        # Determine who has won, and set their decks accordingly.
        if c1 < c2:
            dp1 = dp1r
            dp2 = dp2r + [c2, c1]
        elif c2 < c1:
            dp1 = dp1r + [c1, c2]
            dp2 = dp2r

    # Reverse so that the lower indexes are associated with the cards at the bottom of
    # the deck (note we are guaranteed at this point than only one of `dp1` or `dp2` has
    # anything in it, so we can just add them together to get the winning deck).
    ans = 0
    for i, x in enumerate(reversed(dp1 + dp2)):
        ans += (i + 1) * x

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
assert test or ans_part1 == 35397

# Part 2
########################################################################################
print("\nPart 2:")


def play_game(deck1, deck2, depth=0) -> Tuple[int, Tuple[int, ...]]:
    dp1 = tuple(deck1)
    dp2 = tuple(deck2)
    seen = set()
    tot = len(dp1) + len(dp2)

    while len(dp1) < tot and len(dp2) < tot:
        # Detect if the state has been seen before.
        if (dp1, dp2) in seen:
            return 1, dp1
        seen.add((dp1, dp2))

        c1, *dp1r = dp1
        c2, *dp2r = dp2
        p1wins = False

        # Determine how we should decide this round. If there are enough cards to play a
        # subgame, then call this function recursively. Otherwise, we just determine it
        # like normal.
        if len(dp1r) >= c1 and len(dp2r) >= c2:
            # Recursively call play_game to determine who wins the subgame.
            w, _ = play_game(dp1r[:c1], dp2r[:c2], depth + 1)
            if w == 1:
                p1wins = True
        else:
            if c1 < c2:
                p1wins = False
            elif c2 < c1:
                p1wins = True
            else:
                assert False

        if p1wins:
            dp1 = tuple(dp1r) + (c1, c2)
            dp2 = tuple(dp2r)
        else:
            dp1 = tuple(dp1r)
            dp2 = tuple(dp2r) + (c2, c1)

    if len(dp1) > 0:
        return 1, dp1
    else:
        return 2, dp2


def part2() -> int:
    _, winnerdeck = play_game(DECKP1, DECKP2)

    ans = 0
    for i, x in enumerate(reversed(winnerdeck)):
        ans += (i + 1) * x
    return ans


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = [30976, 36271]
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 31120

if debug:
    input_parsing = input_end - input_start
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + part1_time + part2_time) * 1000}ms")
