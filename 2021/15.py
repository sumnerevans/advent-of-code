#! /usr/bin/env python3

import itertools as it
import heapq
import math
import sys
import time
from collections import defaultdict
from enum import Enum
from typing import Callable, Dict, Iterable, List, Tuple, TypeVar

test = True
debug = False
stdin = False
# INFILENAME = "inputs/15.2.txt"
INFILENAME = "inputs/15.txt"
TESTFILENAME = "inputs/15.test.txt"
for arg in sys.argv:
    if arg == "--notest":
        test = False
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Type variables
K = TypeVar("K")
V = TypeVar("V")


# Enums
class BoundsType(Enum):
    """
    Different types of bounds to use while computing adjacencies.

    RANGE:      [low, high)
    INCLUSIVE:  [low, high]
    EXCLUSIVE:  (low, high)
    """

    RANGE = "range"
    INCLUSIVE = "inclusive"
    EXCLUSIVE = "exclusive"


class AdjacenciesType(Enum):
    """
    Different types of bounds to use while computing adjacencies.

    COMPASS: only directions where a single dimension changes (without diagonals)
    ALL:     all adjacencies including diagonals
    """

    COMPASS = "compass"
    ALL = "all"


# Utilities
def dijkstra(
    next_states: Callable[[K], Iterable[Tuple[int, K]]], start: K, end_state: Callable[[K], bool],
) -> int:
    """
    A simple implementation of Dijkstra's shortest path algorithm for finding the
    shortest path from ``start`` to any element where ``end_state(el) == True``.

    Arguments:
    :param next_states: a function which gives the next possible states of the graph from a given
        node.
    :param start: the start location of the search
    :param end_state: a function which determines if a given element is an end state or not.
    """
    Q = []
    D = {}
    heapq.heappush(Q, (0, start))
    seen = set()

    while Q:
        cost, el = heapq.heappop(Q)
        if el in seen:
            continue
        if end_state(el):
            return D[el]
        seen.add(el)
        for c, x in next_states(el):
            if cost + c < D.get(x, math.inf):
                D[x] = cost + c
                heapq.heappush(Q, (cost + c, x))

    assert False, "No path found to any end state"


def dijkstra_g(G: Dict[K, Iterable[Tuple[int, K]]], start: K, end: K) -> int:
    return dijkstra(lambda x: G[x], start, lambda x: x == end)


def grid_adjs(
    coord: Tuple[int, ...],
    bounds: Tuple[Tuple[int, int], ...] = None,
    adjs_type: AdjacenciesType = AdjacenciesType.COMPASS,
    bounds_type: BoundsType = BoundsType.RANGE,
) -> Iterable[Tuple[int, ...]]:
    """
    Compute the compass adjacencies for a given :math:`n`-dimensional point. Bounds can
    be specified, and only adjacent coordinates within those bounds will be returned.
    Bounds can be specified as any one of the :class:`BoundsType`s.

    :param coord: coordinate to calculate the adjacencies of
    :param bounds: ``(high, low)`` tuples for each of the dimensions
    :param adjs_type: the :class:`AdjacenciesType` to use
    :param bounds_type: the :class:`BoundsType` to use
    """
    # Iterate through all of the deltas for the N dimensions of the coord. A delta is
    # -1, 0, or 1 indicating that the adjacent cell is one lower, same level, or higher
    # than the given coordinate.
    for delta in it.product((-1, 0, 1), repeat=len(coord)):
        if all(d == 0 for d in delta):
            # This is the coord itself, skip.
            continue

        if adjs_type == AdjacenciesType.COMPASS:
            if sum(map(abs, delta)) > 1:
                # For compass adjacencies, we only care when there's only one dimension
                # different than the coordinate.
                continue

        if bounds is not None:
            in_bounds = True
            for i, (d, (low, high)) in enumerate(zip(delta, bounds)):
                if bounds_type == BoundsType.RANGE:
                    in_bounds &= low <= coord[i] + d < high
                elif bounds_type == BoundsType.INCLUSIVE:
                    in_bounds &= low <= coord[i] + d <= high
                elif bounds_type == BoundsType.EXCLUSIVE:
                    in_bounds &= low < coord[i] + d < high
                if not in_bounds:
                    continue

            if not in_bounds:
                continue
        yield tuple(c + d for c, d in zip(coord, delta))


print(f"\n{'=' * 30}\n")

# Read the input
if stdin:
    input_lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        input_lines: List[str] = [l.strip() for l in f.readlines()]

# Try and read in the test file.
try:
    with open(TESTFILENAME) as f:
        test_lines: List[str] = [l.strip() for l in f.readlines()]
except Exception:
    test_lines = []


# Shared
########################################################################################


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    G = defaultdict(set)

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            for r1, c1 in grid_adjs((r, c), ((0, len(lines)), (0, len(lines[0])))):
                if (r, c) == (0, 0):
                    G[(r, c)].add((0, (r1, c1)))
                else:
                    G[(r, c)].add((int(char), (r1, c1)))

    x = int(lines[-1][-1])
    if x > 9:
        x = 1 + (x - 10)

    G[(len(lines) - 1, len(lines[0]) - 1)].add((x, (2 ** 40, 2 ** 40)))
    return dijkstra_g(G, (0, 0), (2 ** 40, 2 ** 40))


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 40
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part1 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part1} != {expected}{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part1)
        print()

part1_start = time.time()
print("Running input...")
ans_part1 = part1(input_lines)
part1_end = time.time()
print("Result:", ans_part1)

tries = [
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 363
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    G = defaultdict(set)

    for shift_r in range(5):
        for shift_c in range(5):
            for r, line in enumerate(lines, start=len(lines) * shift_r):
                for c, char in enumerate(line, start=len(lines[0]) * shift_c):
                    for r1, c1 in grid_adjs((r, c)):
                        if r == c == 0:
                            cost = 0
                        else:
                            cost = int(char) + shift_r + shift_c
                            cost = 1 + (cost - 10) if cost > 9 else cost
                        G[(r, c)].add((cost, (r1, c1)))

    x = int(lines[-1][-1]) + 8
    if x > 9:
        x = 1 + (x - 10)

    G[(len(lines) * 5 - 1, len(lines[0]) * 5 - 1)].add((x, (2 ** 40, 2 ** 40)))
    return dijkstra_g(G, (0, 0), (2 ** 40, 2 ** 40))


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 315
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part2} != {expected}{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part2)
        print()

part2_start = time.time()
print("Running input...")
ans_part2 = part2(input_lines)
part2_end = time.time()
print("Result:", ans_part2)

tries2 = [
    2827
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 2835
if expected is not None:
    assert ans_part2 == expected

if debug:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
