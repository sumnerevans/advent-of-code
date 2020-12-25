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


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()

lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
seq = [int(x) for x in lines[0].split()]

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

"""
I'm using nested tuples to represent the tree. The first index of each tuple is a tuple
containing the children nodes. The second index of each tuple is a tuple containing the
metadata.
"""

# Nodes contain a tuple of sub-nodes and a tuple of metadata.
Node = Tuple[Tuple["Node", ...], Tuple[int, ...]]


def read_node(i, d=0) -> Tuple[Node, int]:
    """
    Read in the node starting at index `i`. This is a recursive function that returns
    the node and the index that should be processed next (the one right after the last
    index we processed).
    """
    N, M = seq[i], seq[i + 1]  # number of children nodes and number of metadata items
    i += 2

    # Read in the children
    children = []
    for _ in range(N):
        node, i = read_node(i, d + 1)
        children.append(node)

    # Read in the metadata
    metadata = []
    for _ in range(M):
        metadata.append(seq[i])
        i += 1

    # Conver to tuples and return along with the index that we processed up to.
    return ((tuple(children), tuple(metadata)), i)


TREE, i = read_node(0)
assert i == len(seq)  # make sure we read the entire thing

shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    """
    Part 1 requires you to sum all of the metadata objects. I do this with the recursive
    traverse_sum function.
    """

    def traverse_sum(node):
        """
        Compute the sum of a given node by summing all of all of the metadata values and
        adding the sum of all of the recursive calls to traverse_sum for all of the
        child nodes.
        """
        return sum(node[1]) + sum(map(traverse_sum, node[0]))

    return traverse_sum(TREE)


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 45210

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    """
    Part 2 requires is very similar, but has a few different rules for the sum
    calculation.
    """

    def traverse_sum(node):
        s = 0
        if len(node[0]) == 0:
            # If a node has no child nodes, its value is the sum of its metadata
            # entries.
            return sum(node[1])
        else:
            # However, if a node does have child nodes, the metadata entries become
            # indexes which refer to those child nodes. A metadata entry of 1 refers to
            # the first child node, 2 to the second, 3 to the third, and so on. The
            # value of this node is the sum of the values of the child nodes referenced
            # by the metadata entries. If a referenced child node does not exist, that
            # reference is skipped. A child node can be referenced multiple time and
            # counts each time it is referenced. A metadata entry of 0 does not refer to
            # any child node.

            # Go thorugh all of the metadata IDs, and if they are valid for this node,
            # add them to the sum.
            for mid in node[1]:
                if 0 < mid <= len(node[0]):
                    s += traverse_sum(node[0][mid - 1])

        return s

    return traverse_sum(TREE)


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
