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
from dataclasses import dataclass
from collections import defaultdict
from enum import Enum, IntEnum
from fractions import Fraction
from typing import (
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Match,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Iterator,
    Union,
)

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "inputs/23.txt"
TESTFILENAME = "inputs/23.test.txt"
for arg in sys.argv:
    if arg == "--notest":
        TEST = False
    if arg == "--debug":
        DEBUG = True
    if arg == "--stdin":
        STDIN = True


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


# Modified range functions
def irange(start, end=None, step=1) -> Generator[int, None, None]:
    """Inclusive range function."""
    if end is None:
        start, end = 0, start
    yield from range(start, end + 1, step)


def dirange(start, end=None, step=1) -> Generator[int, None, None]:
    """
    Directional, inclusive range. This range function is an inclusive version of
    :class:`range` that figures out the correct step direction to make sure that it goes
    from `start` to `end`, even if `end` is before `start`.

    >>> dirange(2, -2)
    [2, 1, 0, -1, -2]
    >>> dirange(-2)
    [0, -1, -2]
    >>> dirange(2)
    [0, 1, 2]
    """
    assert step > 0
    if end is None:
        start, end = 0, start

    if end >= start:
        yield from irange(start, end, step)
    else:
        yield from range(start, end - 1, step=-step)


# Utilities
def allints(s: str) -> Iterator[int]:
    """
    Returns a list of all of the integers in the string.
    """
    return map(lambda m: int(m.group(0)), re.finditer(r"-?\d+", s))


def bitstrtoint(s: Union[str, List[Union[int, str, bool]]]) -> int:
    if isinstance(s, list):
        if isinstance(s[0], bool):
            s = list(map(int, s))

        s = "".join(map(str, s))
    return int(s, 2)


def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


def chunks(iterable, n):
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


def dijkstra(G: Dict[K, Iterable[Tuple[int, K]]], start: K, end: K) -> int:
    """
    A simple implementation of Dijkstra's shortest path algorithm for finding the
    shortest path from ``start`` to ``end`` in ``G``.
    """
    Q = []
    D = {}
    heapq.heappush(Q, (0, start))
    seen = set()

    while Q:
        cost, el = heapq.heappop(Q)
        if el in seen:
            continue
        seen.add(el)
        for c, x in G[el]:
            if cost + c < D.get(x, math.inf):
                D[x] = cost + c
                heapq.heappush(Q, (cost + c, x))

    return D[end]


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


def infer_one_to_one_from_possibles(possibles: Dict[K, Set[V]]) -> Dict[K, V]:
    """
    This goes through a dictionary of key to potential values and computes the true
    value using simple inference where if a key can only be a single value, then it must
    be that value. For example::

        A -> {X, Y}
        B -> {Y}
        C -> {X, Z}

    then ``B`` must be ``Y``, which means that ``A`` cannot be ``Y``, thus ``A`` must be
    ``X``, and by the same logic ``C`` must be ``Z``.
    """
    inferred = {}
    while len(possibles):
        # Find the item that only has one possibility associated with it and pull it out
        # of the possibles dictionary, and remove the ingredient from all of the other
        # sets.
        for key, possible_fields in possibles.items():
            if len(possible_fields) == 1:
                inferred[key] = possible_fields.pop()
                remove_item = inferred[key]
                del possibles[key]
                break
        else:  # nobreak
            assert False, "No keys have a single possible value"

        for x in possibles:
            if remove_item in possibles[x]:
                possibles[x].remove(remove_item)

    return inferred


def int_points_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Generator[Tuple[int, int], None, None]:
    """
    Return a generator of all of the integer points between two given points. Note that
    you are *not* guaranteed that the points will be given from `start` to `end`, but
    all points will be included.
    """
    x1, y1 = start
    x2, y2 = end
    if x1 == x2:
        yield from ((x1, y) for y in dirange(y1, y2))
    elif y1 == y2:
        yield from ((x, y1) for x in dirange(x1, x2))
    else:
        # If `x1 > x2`, that means that `start` is to the right of `end`, so we need to
        # switch the points around so iteration always goes in the positive `x`
        # direction.
        if x1 > x2:
            x1, x2, y1, y2 = x2, x1, y2, y1
        dy = y2 - y1
        dx = x2 - x1
        slope = Fraction(dy, dx)
        for i in irange(dy // slope.numerator):
            yield (x1 + (i * slope.denominator), y1 + (i * slope.numerator))


def invert_dict(d: Dict[K, V]) -> Dict[V, K]:
    return {v: k for k, v in d.items()}


def invert_graph(graph: Dict[K, Iterable[V]]) -> Dict[V, Set[K]]:
    new_graph = {}
    for k, vals in graph.items():
        for v in vals:
            if v not in new_graph:
                new_graph[v] = set()
            new_graph[v].add(k)
    return new_graph


def irot(x: int, y: int, deg: int, origin: Tuple[int, int] = (0, 0)) -> Tuple[int, int]:
    """
    Rotate an integer point ``(x, y)`` by ``deg`` around the ``origin``. Only works when
    ``deg % 90 == 0``.
    """
    transformed_x = x - origin[0]
    transformed_y = y - origin[1]
    assert deg % 90 == 0
    for _ in range((deg // 90) % 4):
        transformed_x, transformed_y = -transformed_y, transformed_x
    return (transformed_x + origin[0], transformed_y + origin[1])


def manhattan(x1: int, y1: int, x2: int = 0, y2: int = 0) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def maplist(fn: Callable[[K], V], l: Iterable[K]) -> List[V]:
    return list(map(fn, l))


def pbits(num: int, pad: int = 32) -> str:
    """Return the bits of `num` in binary with the given padding."""
    return bin(num)[2:].zfill(pad)


def prod(it: Iterable):
    return ft.reduce(operator.mul, it, 1)


def rematch(pattern: str, s: str) -> Match:
    match = re.fullmatch(pattern, s)
    assert match is not None
    return match


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


def seqminmax(sequence: Iterable[int]) -> Tuple[int, int]:
    """
    Returns a tuple containing the minimum and maximum element of the ``sequence``.
    """
    min_, max_ = math.inf, -math.inf
    for x in sequence:
        min_ = min(min_, x)
        max_ = max(max_, x)
    return int(min_), int(max_)


def sizezip(*iterables: Union[List, Set]) -> Iterable[Tuple]:
    """
    Same as the :class:`zip` function, but verifies that the lengths of the
    :class:`list`s or :class:`set`s are the same.
    """
    assert len(set(len(x) for x in iterables)) == 1
    yield from zip(*iterables)


def window(
    iterable: Union[List[K], str],
    n: int,
) -> Iterable[Tuple[Union[K, str], ...]]:
    """
    Return a sliding window of size ``n`` of the given iterable.
    """
    for start_idx in range(len(iterable) - n + 1):
        yield tuple(iterable[start_idx + idx] for idx in range(n))


print(f"\n{'=' * 30}\n")

# Read the input
if STDIN:
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


@dataclass(frozen=True)
class Square:
    type_: str = ""
    moved: int = 0
    empty: bool = False

    def __lt__(self, other: "Square"):
        return (
            self.empty < other.empty
            or self.type_ < other.type_
            or self.moved < other.moved
        )

    def __repr__(self):
        return "S()" if self.empty else f"S({self.type_}, {self.moved})"

    def __str__(self):
        if self.empty:
            return "."
        else:
            return self.type_

    def __hash__(self):
        return hash(self.type_)

    def __eq__(self, other: "Square"):
        return (self.empty and other.empty) or (self.type_ == other.type_)


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    Config = Tuple[
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
    ]

    if test:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("B", 0),
            Square("C", 0),
            Square("B", 0),
            Square("D", 0),
            Square("A", 0),
            Square("D", 0),
            Square("C", 0),
            Square("A", 0),
        )
    else:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("A", 0),
            Square("D", 0),
            Square("A", 0),
            Square("C", 0),
            Square("C", 0),
            Square("D", 0),
            Square("B", 0),
            Square("B", 0),
        )

    def swap(i, j, cfg: Config) -> Config:
        def newval(x: Square):
            if x.empty:
                return x
            return Square(x.type_, x.moved + 1)

        return tuple(
            newval(cfg[i]) if k == j else (newval(cfg[j]) if k == i else x)
            for k, x in enumerate(cfg)
        )

    def printcfg(cfg: Config):
        print("#############")
        print("#{}{}.{}.{}.{}.{}{}#".format(*map(str, cfg[:7])))
        print("###{}#{}#{}#{}###".format(*map(str, cfg[7:11])))
        print("  #{}#{}#{}#{}#  ".format(*map(str, cfg[11:15])))
        print("  #########  ")

    print()

    def next_states(config: Config) -> Iterator[Tuple[int, Config]]:
        # Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper
        # amphipods require 100, and Desert ones require 1000.
        costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
        order = "ABCD"

        def cost(frm, to, type_: str) -> int:
            out = {
                7: {0: 3, 1: 2, 2: 2, 3: 4, 4: 6, 5: 8, 6: 9},
                8: {0: 5, 1: 4, 2: 2, 3: 2, 4: 4, 5: 6, 6: 7},
                9: {0: 7, 1: 6, 2: 4, 3: 2, 4: 2, 5: 4, 6: 5},
                10: {0: 9, 1: 8, 2: 6, 3: 4, 4: 2, 5: 2, 6: 3},
                #
                11: {0: 4, 1: 3, 2: 3, 3: 5, 4: 7, 5: 9, 6: 10},
                12: {0: 6, 1: 5, 2: 3, 3: 3, 4: 5, 5: 7, 6: 8},
                13: {0: 8, 1: 7, 2: 5, 3: 3, 4: 3, 5: 5, 6: 6},
                14: {0: 10, 1: 9, 2: 7, 3: 5, 4: 3, 5: 3, 6: 4},
            }
            if out.get(frm):
                return out[frm][to] * costs[type_]
            else:
                return out[to][frm] * costs[type_]

        # Out L1
        for i in irange(7, 10):
            if config[i].type_ == order[i - 7] == config[i + 4].type_:
                # Already in the right place, as is the one underneath
                continue

            if not config[i].empty and config[i].moved < 2:
                # Left
                for j in dirange(i - 6, 0):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

                # Right
                for j in dirange(i - 5, 6):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

        # Out L2
        for i in irange(11, 14):
            if config[i].type_ == order[i - 11]:
                # Already in the right place
                continue
            if not config[i].empty and config[i].moved == 0 and config[i - 4].empty:
                # Left
                for j in dirange(i - 10, 0):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

                # Right
                for j in dirange(i - 9, 6):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

        # In
        for i in irange(0, 6):
            if config[i].empty:
                continue

            # Left
            if i >= 2:
                for j in dirange(min(5, i), 2):
                    # print("l", i, j, not config[j].empty)
                    if config[j + 5].empty:
                        if config[j + 9].empty:
                            if config[i].type_ == order[j - 2]:
                                yield cost(i, j + 9, config[i].type_), swap(
                                    i, j + 9, config
                                )
                        elif config[j + 9].type_ == config[i].type_:
                            yield cost(i, j + 5, config[i].type_), swap(
                                i, j + 5, config
                            )
                    if not config[j - 1].empty:
                        break

            # Right
            if i <= 4:
                for j in dirange(max(1, i), 4):
                    if config[j + 6].empty:  # upper is empty
                        if config[j + 10].empty:  # lower is empty
                            if config[i].type_ == order[j - 1]:
                                yield cost(i, j + 10, config[i].type_), swap(
                                    i, j + 10, config
                                )
                        elif config[j + 10].type_ == config[i].type_:
                            yield cost(i, j + 6, config[i].type_), swap(
                                i, j + 6, config
                            )
                    if not config[j + 1].empty:
                        break

    Q: List[Tuple[int, Config]] = []
    D = {}
    P = {}
    heapq.heappush(Q, (0, init))
    seen = set()

    i = 0
    while Q:
        cost, el = heapq.heappop(Q)
        if (
            el[7].type_ == "A"
            and el[8].type_ == "B"
            and el[9].type_ == "C"
            and el[10].type_ == "D"
            and el[11].type_ == "A"
            and el[12].type_ == "B"
            and el[13].type_ == "C"
            and el[14].type_ == "D"
        ):
            return cost
        i += 1
        if el in seen:
            continue
        seen.add(el)

        for c, x in next_states(el):
            if cost + c < D.get(x, math.inf):
                D[x] = cost + c
                P[x] = el
                heapq.heappush(Q, (cost + c, x))

    assert False


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 12521
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
    12519,
    15361,
    15405
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 15385
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    Config = Tuple[
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
    ]

    if test:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("B", 0),
            Square("C", 0),
            Square("B", 0),
            Square("D", 0),
            # new
            Square("D", 0),
            Square("C", 0),
            Square("B", 0),
            Square("A", 0),
            Square("D", 0),
            Square("B", 0),
            Square("A", 0),
            Square("C", 0),
            # endnew
            Square("A", 0),
            Square("D", 0),
            Square("C", 0),
            Square("A", 0),
        )
    else:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("A", 0),
            Square("D", 0),
            Square("A", 0),
            Square("C", 0),
            # new
            Square("D", 0),
            Square("C", 0),
            Square("B", 0),
            Square("A", 0),
            Square("D", 0),
            Square("B", 0),
            Square("A", 0),
            Square("C", 0),
            # endnew
            Square("C", 0),
            Square("D", 0),
            Square("B", 0),
            Square("B", 0),
        )

    def swap(i, j, cfg: Config) -> Config:
        def newval(x: Square):
            if x.empty:
                return x
            return Square(x.type_, x.moved + 1)

        return tuple(
            newval(cfg[i]) if k == j else (newval(cfg[j]) if k == i else x)
            for k, x in enumerate(cfg)
        )

    def printcfg(cfg: Config):
        print("#############")
        print("#{}{}.{}.{}.{}.{}{}#".format(*map(str, cfg[:7])))
        print("###{}#{}#{}#{}###".format(*map(str, cfg[7:11])))
        print("  #{}#{}#{}#{}#  ".format(*map(str, cfg[11:15])))
        print("  #########  ")

    print()

    def next_states(config: Config) -> Iterator[Tuple[int, Config]]:
        # Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper
        # amphipods require 100, and Desert ones require 1000.
        costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
        order = "ABCD"

        def cost(frm, to, type_: str) -> int:
            out = {
                7: {0: 3, 1: 2, 2: 2, 3: 4, 4: 6, 5: 8, 6: 9},
                8: {0: 5, 1: 4, 2: 2, 3: 2, 4: 4, 5: 6, 6: 7},
                9: {0: 7, 1: 6, 2: 4, 3: 2, 4: 2, 5: 4, 6: 5},
                10: {0: 9, 1: 8, 2: 6, 3: 4, 4: 2, 5: 2, 6: 3},
                #
                11: {0: 4, 1: 3, 2: 3, 3: 5, 4: 7, 5: 9, 6: 10},
                12: {0: 6, 1: 5, 2: 3, 3: 3, 4: 5, 5: 7, 6: 8},
                13: {0: 8, 1: 7, 2: 5, 3: 3, 4: 3, 5: 5, 6: 6},
                14: {0: 10, 1: 9, 2: 7, 3: 5, 4: 3, 5: 3, 6: 4},
                #
                15: {0: 5, 1: 4, 2: 4, 3: 6, 4: 8, 5: 10, 6: 11},
                16: {0: 7, 1: 6, 2: 4, 3: 4, 4: 6, 5: 8, 6: 9},
                17: {0: 9, 1: 8, 2: 6, 3: 4, 4: 4, 5: 6, 6: 7},
                18: {0: 11, 1: 10, 2: 8, 3: 6, 4: 4, 5: 4, 6: 5},
                #
                19: {0: 6, 1: 5, 2: 5, 3: 7, 4: 9, 5: 11, 6: 12},
                20: {0: 8, 1: 7, 2: 5, 3: 5, 4: 7, 5: 9, 6: 10},
                21: {0: 10, 1: 9, 2: 7, 3: 5, 4: 5, 5: 7, 6: 8},
                22: {0: 12, 1: 11, 2: 9, 3: 6, 4: 5, 5: 5, 6: 6},
            }
            if out.get(frm):
                return out[frm][to] * costs[type_]
            else:
                return out[to][frm] * costs[type_]

        # Out L1
        for i in irange(7, 10):
            if config[i].type_ == order[i - 7] == config[i + 4].type_:
                # Already in the right place, as is the one underneath
                continue

            if not config[i].empty and config[i].moved < 2:
                # Left
                for j in dirange(i - 6, 0):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

                # Right
                for j in dirange(i - 5, 6):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

        # Out L2
        for i in irange(11, 14):
            if config[i].type_ == order[i - 11]:
                # Already in the right place
                continue
            if not config[i].empty and config[i].moved == 0 and config[i - 4].empty:
                # Left
                for j in dirange(i - 10, 0):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

                # Right
                for j in dirange(i - 9, 6):
                    if not config[j].empty:
                        break
                    yield cost(i, j, config[i].type_), swap(i, j, config)

        # In
        for i in irange(0, 6):
            if config[i].empty:
                continue

            # Left
            if i >= 2:
                for j in dirange(min(5, i), 2):
                    # print("l", i, j, not config[j].empty)
                    if config[j + 5].empty:
                        if config[j + 9].empty:
                            if config[i].type_ == order[j - 2]:
                                yield cost(i, j + 9, config[i].type_), swap(
                                    i, j + 9, config
                                )
                        elif config[j + 9].type_ == config[i].type_:
                            yield cost(i, j + 5, config[i].type_), swap(
                                i, j + 5, config
                            )
                    if not config[j - 1].empty:
                        break

            # Right
            if i <= 4:
                for j in dirange(max(1, i), 4):
                    if config[j + 6].empty:  # upper is empty
                        if config[j + 10].empty:  # lower is empty
                            if config[i].type_ == order[j - 1]:
                                yield cost(i, j + 10, config[i].type_), swap(
                                    i, j + 10, config
                                )
                        elif config[j + 10].type_ == config[i].type_:
                            yield cost(i, j + 6, config[i].type_), swap(
                                i, j + 6, config
                            )
                    if not config[j + 1].empty:
                        break

    Q: List[Tuple[int, Config]] = []
    D = {}
    P = {}
    heapq.heappush(Q, (0, init))
    seen = set()

    i = 0
    while Q:
        cost, el = heapq.heappop(Q)
        if (
            el[7].type_ == "A"
            and el[8].type_ == "B"
            and el[9].type_ == "C"
            and el[10].type_ == "D"
            and el[11].type_ == "A"
            and el[12].type_ == "B"
            and el[13].type_ == "C"
            and el[14].type_ == "D"
            and el[15].type_ == "A"
            and el[16].type_ == "B"
            and el[17].type_ == "C"
            and el[18].type_ == "D"
            and el[19].type_ == "A"
            and el[20].type_ == "B"
            and el[21].type_ == "C"
            and el[22].type_ == "D"
        ):
            return cost
        i += 1
        if el in seen:
            continue
        seen.add(el)

        for c, x in next_states(el):
            if cost + c < D.get(x, math.inf):
                D[x] = cost + c
                P[x] = el
                heapq.heappush(Q, (cost + c, x))


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 44169
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
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = None  # (<>)
if expected is not None:
    assert ans_part2 == expected

if DEBUG:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
