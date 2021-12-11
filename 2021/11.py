#! /usr/bin/env python3

import itertools as it
import sys
import time
from enum import Enum
from typing import Iterable, List, Tuple

test = True
debug = False
stdin = False
INFILENAME = "inputs/11.txt"
TESTFILENAME = "inputs/11.test.txt"
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
    ans = 0

    seq = [[int(c) for c in x] for x in lines]
    for _ in range(100):
        ns = [[(x + 1) for x in r] for r in seq]

        flashed = set()

        while True:
            flashed_this_time = set()
            for r in range(len(seq)):
                for c in range(len(seq[0])):
                    if ns[r][c] > 9:
                        if (r, c) in flashed:
                            continue
                        flashed.add((r, c))
                        flashed_this_time.add((r, c))
                        for r, c in grid_adjs(
                            (r, c),
                            ((0, len(seq)), (0, len(seq[0]))),
                            AdjacenciesType.ALL,
                        ):
                            ns[r][c] += 1

            if len(flashed_this_time) == 0:
                break

        ans += sum(1 for r in ns for c in r if c > 9)
        seq = [[0 if x > 9 else x for x in r] for r in ns]

    return ans


def part_1_original_approach(lines: List[str]) -> int:
    """
    This was my original approach. I missed a few critical details that really bit me in
    the ass.

    1. Operator precedence for modulo.
    """
    ans = 0

    seq = [[int(c) for c in x] for x in lines]
    for _ in range(100):
        ns = [[(a + 1) % 10 for a in r] for r in seq]

        to_flash = {
            (r, c) for r in range(len(seq)) for c in range(len(seq[0])) if ns[r][c] == 0
        }
        flashed = set()
        while to_flash:
            f = to_flash.pop()

            if f in flashed:
                continue
            flashed.add(f)

            to_inc = set()
            for r, c in grid_adjs(
                f, ((0, len(seq)), (0, len(seq[0]))), AdjacenciesType.ALL
            ):
                to_inc.add((r, c))

            for r, c in to_inc:
                # Here was my operator precedence error. I originally had
                # ns[r][c] = 0 if ns[r][c] == 0 else ns[r][c] + 1 % 10
                # which is wrong since % binds tighter than +
                ns[r][c] = 0 if ns[r][c] == 0 else (ns[r][c] + 1) % 10
                if ns[r][c] == 0:
                    to_flash.add((r, c))

        ans += sum(1 for r in ns for c in r if c == 0)
        seq = ns

    return ans


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        assert test_ans_part1 == part_1_original_approach(test_lines)
        expected = 1656
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part1 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part1}{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part1)
        print()

part1_start = time.time()
print("Running input...")
ans_part1 = part1(input_lines)
assert ans_part1 == part_1_original_approach(input_lines)
part1_end = time.time()
print("Result:", ans_part1)

tries = [
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 1773
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    seq = [[int(c) for c in x] for x in lines]
    i = 0
    while True:
        i += 1
        ns = [[(x + 1) for x in r] for r in seq]

        flashed = set()

        while True:
            flashed_this_time = set()
            for r in range(len(seq)):
                for c in range(len(seq[0])):
                    if ns[r][c] > 9:
                        if (r, c) in flashed:
                            continue
                        flashed.add((r, c))
                        flashed_this_time.add((r, c))
                        for r, c in grid_adjs(
                            (r, c),
                            ((0, len(seq)), (0, len(seq[0]))),
                            AdjacenciesType.ALL,
                        ):
                            ns[r][c] += 1

            if not len(flashed_this_time):
                break

        # If everything flashed, this is the iteration.
        if len(flashed) == len(seq) * len(seq[0]):
            return i

        seq = [[0 if x > 9 else x for x in r] for r in ns]


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 195
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part2}{bcolors.ENDC}")
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
expected = 494
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
