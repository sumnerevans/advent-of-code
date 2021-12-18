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
from enum import Enum, IntEnum
from fractions import Fraction
from typing import (
    Callable,
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
INFILENAME = "inputs/18.txt"
TESTFILENAME = "inputs/18.test.txt"
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


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    def explode_in_left(pair, val) -> Union[int, List[int]]:
        if isinstance(pair, int):
            return pair + val
        else:
            return [explode_in_left(pair[0], val), pair[1]]

    def explode_in_right(pair, val) -> Union[int, List[int]]:
        if isinstance(pair, int):
            return pair + val
        else:
            return [pair[0], explode_in_right(pair[1], val)]

    def reduce(pair, d=0):
        if d == 4:
            if isinstance(pair, int):
                return ("nothing", ()), pair
            return ("explodeBoth", tuple(pair)), 0
        if isinstance(pair, int):
            return ("nothing", ()), pair

        (op_l, params_l), lhs = reduce(pair[0], d + 1)
        # print(" " * d, op_l, params_l, lhs, pair)
        if op_l == "done":
            return ("done", params_l), [lhs, pair[1]]
        elif op_l == "explodeBoth":
            return ("explodeLeft", params_l), [
                lhs,
                explode_in_left(pair[1], params_l[1]),
            ]
        elif op_l == "explodeLeft":
            return ("explodeLeft", params_l), [lhs, pair[1]]
        elif op_l == "explodeRight":
            return ("done", ()), [lhs, explode_in_left(pair[1], params_l[1])]
        else:
            (op_r, params_r), rhs = reduce(pair[1], d + 1)
            # print(" " * d, op_r, params_r, rhs, pair)
            if op_r == "done":
                return ("done", params_r), [pair[0], rhs]
            elif op_r == "explodeBoth":
                return ("explodeRight", params_r), [
                    explode_in_right(pair[0], params_r[0]),
                    rhs,
                ]
            elif op_r == "explodeLeft":
                return ("done", ()), [explode_in_right(pair[0], params_r[0]), rhs]
            elif op_r == "explodeRight":
                return ("explodeRight", params_r), [pair[0], rhs]
        return ("nothing", ()), pair

    def reduce_split(pair):
        """
        To split a regular number, replace it with a pair; the left element of the
        pair should be the regular number divided by two and rounded down, while the
        right element of the pair should be the regular number divided by two and
        rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes
        [6,6], and so on.
        """
        if isinstance(pair, int):
            if pair >= 10:
                return [math.floor(pair / 2), math.ceil(pair / 2)]
            return pair
        split_l = reduce_split(pair[0])
        if split_l != pair[0]:
            return [split_l, pair[1]]
        else:
            return [split_l, reduce_split(pair[1])]

    TC = {
        # base case
        "4": 4,
        # Splits
        "10": "[5, 5]",
        "11": "[5, 6]",
        "[11, 11]": "[[5, 6], 11]",
        "[[5, 6], 11]": "[[5, 6], [5, 6]]",
        "[8, 11]": "[8, [5, 6]]",
        "[[5, 6], 11]": "[[5, 6], [5, 6]]",
        "[[[[1,1],[2,2]], [3,3]], [4,4]]": "[[[[1,1],[2,2]],[3,3]],[4,4]]",
        # Explodes
        "[[[[[9,8],1],2],3],4]": "[[[[0,9],2],3],4]",
        "[7,[6,[5,[4,[3,2]]]]]": "[7,[6,[5,[7,0]]]]",
        "[[6,[5,[4,[3,2]]]],1]": "[[6,[5,[7,0]]],3]",
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]": "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]": "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
    }
    if True:
        p = True
        for t, ex in TC.items():
            print("=" * 100)
            print("test", t)
            test_expr = eval(t) if isinstance(t, str) else t
            x = reduce_split(reduce(test_expr)[1])
            # prev = deepcopy(test_expr)
            # while True:
            #     x = reduce(prev)[1]
            #     if x == prev:
            #         break
            #     prev = deepcopy(x)

            expected_expr = eval(ex) if isinstance(ex, str) else ex

            if x != expected_expr:
                print(bcolors.FAIL)
            print(x)
            print(expected_expr)
            print(bcolors.ENDC)
            p &= x == expected_expr
            assert x == expected_expr
        assert p, "TC FAILED"

    loop_TC = {
        "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]": "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        "[[[[1,1],[2,2]],[3,3]],[4,4]]": "[[[[1,1],[2,2]],[3,3]],[4,4]]",
        "[[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]]": "[[[[3,0],[5,3]],[4,4]],[5,5]]",
    }
    if True:
        p = True
        for t, ex in loop_TC.items():
            print("=" * 100)
            print("loop test", t)
            test_expr = eval(t) if isinstance(t, str) else t
            prev = deepcopy(test_expr)
            while True:
                print(prev)
                new = reduce(prev)[1]
                if prev != new:
                    prev = new
                    continue
                x = reduce_split(new)
                if x == prev:
                    break
                prev = deepcopy(x)

            expected_expr = eval(ex) if isinstance(ex, str) else ex

            if prev != expected_expr:
                print(bcolors.FAIL)
            print("GOT", prev)
            print("EXP", expected_expr)
            print(bcolors.ENDC)
            p &= prev == expected_expr
            assert prev == expected_expr
        assert p, "TC FAILED"

    C = eval(lines[0])
    for line in lines[1:]:
        if line.strip() == "#":
            break
        # Add line to C
        added = [C, eval(line)]
        # print(added)
        prev = deepcopy(added)
        while True:
            print(prev)
            new = reduce(prev)[1]
            if prev != new:
                prev = new
                continue
            x = reduce_split(new)
            if x == prev:
                break
            prev = deepcopy(x)

        C = prev

    # To check whether it's the right answer, the snailfish teacher only checks the
    # magnitude of the final sum. The magnitude of a pair is 3 times the magnitude of
    # its left element plus 2 times the magnitude of its right element. The magnitude of
    # a regular number is just that number.
    def mag(pair):
        if isinstance(pair, int):
            return pair
        return 3 * mag(pair[0]) + 2 * mag(pair[1])

    return mag(C)


def part1_2(lines: List[str]) -> int:
    def explode_in_left(pair, val) -> Union[int, List[int]]:
        if isinstance(pair, int):
            return pair + val
        else:
            return [explode_in_left(pair[0], val), pair[1]]

    def explode_in_right(pair, val) -> Union[int, List[int]]:
        if isinstance(pair, int):
            return pair + val
        else:
            return [pair[0], explode_in_right(pair[1], val)]

    def reduce(pair, d=0, cmd=None):
        print(" " * d, "reduce", pair)
        if d == 4:
            # print(" " * d, "explodeBoth", pair)
            return ("explodeBoth", (pair)), 0

        if isinstance(pair, int):
            """
            To split a regular number, replace it with a pair; the left element of the
            pair should be the regular number divided by two and rounded down, while the
            right element of the pair should be the regular number divided by two and
            rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes
            [6,6], and so on.
            """
            if pair >= 10:
                return ("done", ()), [math.floor(pair / 2), math.ceil(pair / 2)]
            return ("nothing", ()), pair

        (op_l, params_l), res_l = reduce(pair[0], d + 1)
        if op_l == "done":
            return ("done", ()), [res_l, pair[1]]
        elif op_l == "nothing":
            (op_r, params_r), res_r = reduce(pair[1], d + 1)
            if op_r == "done":
                return (op_r, params_r), [res_l, res_r]
            elif op_r == "nothing":
                return (op_r, ()), [res_l, res_r]
            elif op_r == "explodeBoth":
                return ("explodeRight", params_r), [
                    explode_in_right(pair[0], params_r[0]),
                    0,
                ]
            assert False, f"1 {op_r}"
        elif op_l == "explodeBoth":
            return ("explodeLeft", params_l), [0, explode_in_left(pair[1], params_l[1])]
        else:
            (op_l, params_l), res_r = reduce(pair[1], d + 1, cmd=(op_l, params_l))
            return ("done", ()), [res_l, res_r]

    TC = {
        # base case
        "4": 4,
        # Splits
        "10": "[5, 5]",
        "11": "[5, 6]",
        "[11, 11]": "[[5, 6], 11]",
        "[8, 11]": "[8, [5, 6]]",
        "[[5, 6], 11]": "[[5, 6], [5, 6]]",
        "[[5, [11, 23]], 11]": "[[5, [[5, 6], 23]], 11]",
        "[[5, [[5, 6], 23]], 11]": "[[5, [[5, 6], [11, 12]]], 11]",
        # Explosions
        "[[[[[9,8],1],2],3],4]": "[[[[0,9],2],3],4]",
        "[[[[1,[9,8]],2],3],4]": "[[[[10,0],10],3],4]",
        "[7, [6, [5, [4, [3, 2]]]]]": [7, [6, [5, [7, 0]]]],
        "[[6,[5,[4,[3,2]]]],1]": [[6, [5, [7, 0]]], 3],
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]": [
            [3, [2, [8, 0]]],
            [9, [5, [4, [3, 2]]]],
        ],
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]": [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        "[[3, [2, [1, 2]]], [[[[8, 1], 3], 4], 5]]": [
            [3, [2, [1, 10]]],
            [[[0, 4], 4], 5],
        ],
        "[[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]": [
            [[[0, 7], 4], [15, [0, 13]]],
            [1, 1],
        ],
        "[[[[0,7],4],[15,[0,13]]],[1,1]]": [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
        "[[[[0, [3, 2]], [4, 3]], [5, 4]], [6, 5]]": [
            [[[3, 0], [6, 3]], [5, 4]],
            [6, 5],
        ],
        "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]": "[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]",
        "[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]": "[[[[4,0],[5,4]],[[0,[7,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]",
    }
    if True:
        p = True
        for t, ex in TC.items():
            print("=" * 100)
            print("test", t)
            x = reduce(eval(t))[1]
            e = eval(ex) if isinstance(ex, str) else ex
            if x != e:
                print(bcolors.FAIL)
            print(x)
            print(e)
            print(bcolors.ENDC)
            p &= x == e
            assert x == e
        if p:
            assert False, "ran tests, all PASS"
        else:
            assert False, "ran tests with FAILs"
    return 0


def part1_old(lines: List[str]) -> int:
    ans = 0

    # seq = [int(x) for x in lines]
    # seq = [int(x) for x in lines[0].split(",")]
    # L = [[int(x) for x in l] for l in lines]

    def explode_in_left(pair, val) -> Union[int, List[int]]:
        if isinstance(pair, int):
            return pair + val
        else:
            return [explode_in_left(pair[0], val), pair[1]]

    def explode_in_right(pair, val) -> Union[int, List[int]]:
        if isinstance(pair, int):
            return pair + val
        else:
            return [pair[0], explode_in_right(pair[1], val)]

    """
    To reduce a snailfish number, you must repeatedly do the first action in this list that applies to the snailfish number:

        If any pair is nested inside four pairs, the leftmost such pair explodes.
        If any regular number is 10 or greater, the leftmost such regular number splits.
    """

    def reduce(pair, d=0):
        print(" " * d, "reduce", pair, d)
        if d == 4:
            # print(" " * d, "explodeBoth", pair)
            return "explodeBoth", 0, pair

        if isinstance(pair, int):
            """
            To split a regular number, replace it with a pair; the left element of the
            pair should be the regular number divided by two and rounded down, while the
            right element of the pair should be the regular number divided by two and
            rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes
            [6,6], and so on.
            """
            if pair >= 10:
                # print(" " * d, "split", [math.floor(pair / 2), math.ceil(pair / 2)])
                return "done", [math.floor(pair / 2), math.ceil(pair / 2)]
            # print(" " * d, "nothing", pair)
            return "nothing", pair

        """
        To explode a pair, the pair's left value is added to the first
        regular number to the left of the exploding pair (if any), and the
        pair's right value is added to the first regular number to the right
        of the exploding pair (if any). Exploding pairs will always consist
        of two regular numbers. Then, the entire exploding pair is replaced
        with the regular number 0.
        """
        op, *a = reduce(pair[0], d + 1)
        # print(" " * d, "ohea", op, a, pair)
        if op in ("explodeBoth", "explodeRight"):
            if isinstance(pair[1], int):
                newop = "explodeLeft" if op == "explodeBoth" else "done"
                # print(" "*d,'int', [a[0], a[1][1] + pair[1]], newop)
                # print(" "*d, newop, [a[0], a[1][1] + pair[1]], a[1])
                return newop, [a[0], a[1][1] + pair[1]], a[1]
            else:
                if op == "explodeBoth":
                    ex = explode_in_left(pair[1], a[1][1])
                    if ex != pair[1]:
                        op = "done"
                else:
                    print("here")
                    ex = pair[1]

                return op, [a[0], ex], a[1]
        elif op == "explodeLeft":
            return "explodeLeft", [a[0], pair[1]], a[1]
        elif op == "done":
            return "done", [a[0], pair[1]]
        elif op == "nothing":
            # print('nc', pair[1])
            # print(reduce(pair[1], d + 1))
            op, *b = reduce(pair[1], d + 1)
            # print(" " * d, "nothing case", op, b, pair)
            if op in ("explodeBoth", "explodeLeft"):
                if isinstance(pair[0], int):
                    newop = "explodeRight" if op == "explodeBoth" else "done"
                    # print(" " * d, "ret", newop, [b[1][0] + pair[0], b[0]], b[1])
                    return newop, [b[1][0] + pair[0], b[0]], b[1]
                else:
                    return "done", [explode_in_right(pair[0], b[1][0]), b[0]], b[1]
            else:
                # print('got here', pair, b)
                return op, [pair[0], b[0]], *b[1:]
            if b == "explode":
                # print("b", [pair[0] + pair[1][0], 0])
                return [pair[0] + pair[1][0], 0]
            # print(b, b)
            return [b, b]

        assert False

        for i, p in enumerate(pair):
            if isinstance(p, list):
                res, cont = reduce(p, d + 1)
                if cont == "break":
                    break
                if cont == "explode":
                    print(p)
                    if i == 0:
                        return [res, pair[1] + p[1]], "break"
                    else:
                        return [pair[0] + p[0], 0], "break"
                else:
                    return []
        print("got here", pair)

    # TEST CASES
    print()
    TC = {
        "[[[[[9, 8], 1], 2], 3], 4]": [[[[0, 9], 2], 3], 4],
        "[7, [6, [5, [4, [3, 2]]]]]": [7, [6, [5, [7, 0]]]],
        "[[6,[5,[4,[3,2]]]],1]": [[6, [5, [7, 0]]], 3],
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]": [
            [3, [2, [8, 0]]],
            [9, [5, [4, [3, 2]]]],
        ],
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]": [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        "[[3, [2, [1, 2]]], [[[[8, 1], 3], 4], 5]]": [
            [3, [2, [1, 10]]],
            [[[0, 4], 4], 5],
        ],
        "[[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]": [
            [[[0, 7], 4], [15, [0, 13]]],
            [1, 1],
        ],
        "[[[[0,7],4],[15,[0,13]]],[1,1]]": [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
        "[[[[0, [3, 2]], [4, 3]], [5, 4]], [6, 5]]": [
            [[[3, 0], [6, 3]], [5, 4]],
            [6, 5],
        ],
        "[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]": "[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]",
        "[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]": "[[[[4,0],[5,4]],[[0,[7,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]",
    }
    if True:
        p = True
        for t, ex in TC.items():
            print("=" * 100)
            x = reduce(eval(t))[1]
            e = eval(ex) if isinstance(ex, str) else ex
            if x == e:
                print("pass")
                print(x)
                print(e)
            if x != e:
                print(bcolors.FAIL)
                print(x)
                print(e)
                print(bcolors.ENDC)
                p = False
        if p:
            assert False, "ran tests, all PASS"
        else:
            assert False, "ran tests with FAILs"

    print()
    C = eval(lines[0])
    for line in lines[1:]:
        if line.strip() == "#":
            break
        # Add line to C
        added = [C, eval(line)]
        # print(added)
        prev = deepcopy(added)
        new = reduce(added)[1]
        # print("prev", prev)
        # print("new", new)
        while prev != new:
            print(new)
            prev = deepcopy(new)
            new = reduce(prev)[1]
        # print(new)
        C = new
    print("C", C)
    print(eval("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"))
    assert C == eval("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")

    # To check whether it's the right answer, the snailfish teacher only checks the
    # magnitude of the final sum. The magnitude of a pair is 3 times the magnitude of
    # its left element plus 2 times the magnitude of its right element. The magnitude of
    # a regular number is just that number.
    def mag(pair):
        if isinstance(pair, int):
            return pair
        return 3 * mag(pair[0]) + 2 * mag(pair[1])

    return mag(C)

    return ans


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 4140
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
