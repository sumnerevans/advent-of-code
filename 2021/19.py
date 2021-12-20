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
from collections import defaultdict, namedtuple
from enum import Enum, IntEnum
from fractions import Fraction
from typing import (
    Callable,
    DefaultDict,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Match,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

test = True
debug = False
stdin = False
INFILENAME = "inputs/19.txt"
TESTFILENAME = "inputs/19.test.txt"
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


# Modified range functions
def irange(start, end=None, step=1) -> Generator[int, None, None]:
    """Inclusive range function."""
    if end is None:
        start, end = 0, start
    yield from range(start, end + 1, step=step)


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


ROTATIONS = [
    # 4 rotations facing +X axis
    lambda v: (v[0], v[1], v[2]),  # 0 deg
    lambda v: (v[0], -v[2], v[1]),  # 90 deg
    lambda v: (v[0], -v[1], -v[2]),  # 180 deg
    lambda v: (v[0], v[2], -v[1]),  # 270 deg
    # 4 rotations facing -X axis
    lambda v: (-v[0], v[1], v[2]),  # 0 deg
    lambda v: (-v[0], -v[2], v[1]),  # 90 deg
    lambda v: (-v[0], -v[1], -v[2]),  # 180 deg
    lambda v: (-v[0], v[2], -v[1]),  # 270 deg
    # 4 rotations facing +Y axis
    lambda v: (v[1], v[0], v[2]),  # 0 deg
    lambda v: (-v[2], v[0], v[1]),  # 90 deg
    lambda v: (-v[1], v[0], -v[2]),  # 180 deg
    lambda v: (v[2], v[0], -v[1]),  # 270 deg
    # 4 rotations facing -Y axis
    lambda v: (v[1], -v[0], v[2]),  # 0 deg
    lambda v: (-v[2], -v[0], v[1]),  # 90 deg
    lambda v: (-v[1], -v[0], -v[2]),  # 180 deg
    lambda v: (v[2], -v[0], -v[1]),  # 270 deg
    # 4 rotations facing +Z axis
    lambda v: (v[2], v[1], v[0]),  # 0 deg
    lambda v: (-v[1], v[2], v[0]),  # 90 deg
    lambda v: (-v[2], -v[1], v[0]),  # 180 deg
    lambda v: (v[1], -v[2], v[0]),  # 270 deg
    # 4 rotations facing -Z axis
    lambda v: (v[2], v[1], -v[0]),  # 0 deg
    lambda v: (-v[1], v[2], -v[0]),  # 90 deg
    lambda v: (-v[2], -v[1], -v[0]),  # 180 deg
    lambda v: (v[1], -v[2], -v[0]),  # 270 deg
]


assert len(list(ROTATIONS)) == 24


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], threshold: int = 12) -> int:
    Point = Tuple[int, ...]
    Diff = Tuple[int, ...]

    scanner_points: List[Set[Point]] = []
    point_size = 0
    for line in lines:
        if line.strip() == "":
            continue
        try:
            scanner_num = int(rematch(r"--- scanner (\d+) ---", line).group(1))
            assert scanner_num == len(scanner_points)
            scanner_points.append(set())
            continue
        except:
            pass
        line_tup = tuple(allints(line))
        scanner_points[-1].add(line_tup)
        point_size = len(line_tup)

    # [{rotation -> {start_point -> {end_point: diff}}}]
    scanner_point_diffs: List[
        DefaultDict[int, DefaultDict[Point, Dict[Point, Diff]]]
    ] = []
    for sp in scanner_points:
        scanner_point_diffs.append(defaultdict(lambda: defaultdict(dict)))
        for rot_num, rotation_fn in enumerate(ROTATIONS):
            rot_sp = maplist(rotation_fn, sp)
            for i, p1 in enumerate(rot_sp):
                for j, p2 in enumerate(rot_sp):
                    if i == j:
                        continue
                    scanner_point_diffs[-1][rot_num][p1][p2] = tuple(
                        b - a for a, b in zip(p1, p2)
                    )
    print()
    print(scanner_point_diffs[0][0])
    print(scanner_point_diffs[0][1])
    # ohea

    # dictionary of scanner number -> {scanner number -> (relative offset, fns)}
    scanner_rel_pos: DefaultDict[int, Dict[int, Tuple[Point, int]]] = defaultdict(
        dict, {0: {0: (tuple([0] * point_size), 0)}}
    )

    for i, spd1 in enumerate(scanner_point_diffs):
        for j, spd2 in enumerate(scanner_point_diffs[i + 1 :], start=i + 1):
            # spd1 stays stable, so only consider the 0th rotation.
            spd1_no_rot = spd1[0]

            # determine if any rotation of spd2 can get alignment with one of the points
            # in spd1
            for spd1_start_point, spd1_diffs_at_start_point in spd1_no_rot.items():
                # print("start", spd1_start_point, spd1_diffs_at_start_point)
                # print(spd2)
                foundmatch = False
                for rot_num, spd2_rot in spd2.items():
                    # print(rot_num, spd2_rot, ROTATIONS[rot_num])
                    for spd2k, spd2v in spd2_rot.items():
                        # print(" ", "rot", rot_num)
                        # print(" ", "spd1_start_point", spd1_start_point)
                        # print(" ", "spd2k", spd2k)
                        print(
                            " ", "spd1_diffs_at_start_point", spd1_diffs_at_start_point
                        )
                        print(" ", "spd2v                    ", spd2v)
                        intersection = set(spd1_diffs_at_start_point.values())
                        # print(">>", intersection)
                        # print(">>", set(spd2v.values()))
                        intersection &= set(spd2v.values())
                        print(">", intersection)
                        # -1 because includes self
                        if len(intersection) >= threshold - 1:
                            print("got here")
                            print(intersection)
                            print(spd1_start_point)
                            print(spd2k)
                            scanner_rel_pos[i][j] = (
                                tuple(
                                    map(
                                        lambda x: x[0] - x[1],
                                        zip(spd1_start_point, spd2k),
                                    )
                                ),
                                rot_num,
                            )
                            foundmatch = True
                            break
                    if foundmatch:
                        break
                print(foundmatch)
                if foundmatch:
                    break
                # print(matches)
                # if len(matches) >= threshold:
                #     print("HERE")
                #     print(i, j)
                #     p1, p2 = matches[0]
                #     scanner_rel_pos[i][j] = (p1[0] - p2[0], p1[1] - p2[1])
    print("relpos", scanner_rel_pos)
    ohea

    all_beacons_rel_to_0 = set()
    for i, sps in enumerate(scanner_points):
        offset_for_i, rotation_fn = scanner_rel_pos[0][i]

        print("  sn", i)
        print("  sps", sps)
        print("  ofi", offset_for_i)

        sps_rot = maplist(ROTATIONS[rotation_fn], sps)
        print("  sps_rot", sps_rot)

        for point in sps_rot:
            print("  p", point, offset_for_i)
            print(" ", tuple(map(sum, zip(offset_for_i, point))))
            all_beacons_rel_to_0.add(tuple(map(sum, zip(offset_for_i, point))))
        print(" ", all_beacons_rel_to_0)

    print("ohea")
    print(all_beacons_rel_to_0)
    # assert all_beacons_rel_to_0 == {(0, 2, 0), (4, 1, 0), (3, 3, 0)}
    print({(-1, -1, 1), (-2, -2, 2), (-3, -3, 3), (-2, -3, 1), (5, 6, -4), (8, 0, 7)})
    assert all_beacons_rel_to_0 == {
        (-1, -1, 1),
        (-2, -2, 2),
        (-3, -3, 3),
        (-2, -3, 1),
        (5, 6, -4),
        (8, 0, 7),
    }

    return len(all_beacons_rel_to_0)


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, 3)
        expected = 79
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
ans_part1 = part1(input_lines, 12)
part1_end = time.time()
print("Result:", ans_part1)

tries = [
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = None  # (<>)
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    ans = 0

    "(<>)"

    return ans


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = None  # (<>)
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

if debug:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
