#! /usr/bin/env python3

import math
import sys
import time
from copy import deepcopy
from typing import Callable, Iterable, List, TypeVar, Union

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


# Utilities
def maplist(fn: Callable[[K], V], l: Iterable[K]) -> List[V]:
    return list(map(fn, l))


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


def add(expr1, expr2):
    added = [expr1, expr2]
    prev = deepcopy(added)
    while True:
        new = reduce(prev)[1]
        if prev != new:
            prev = new
            continue
        x = reduce_split(new)
        if x == prev:
            break
        prev = deepcopy(x)
    return prev


# To check whether it's the right answer, the snailfish teacher only checks the
# magnitude of the final sum. The magnitude of a pair is 3 times the magnitude of
# its left element plus 2 times the magnitude of its right element. The magnitude of
# a regular number is just that number.
def mag(pair):
    if isinstance(pair, int):
        return pair
    return 3 * mag(pair[0]) + 2 * mag(pair[1])


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    C = eval(lines[0])
    for line in lines[1:]:
        C = add(C, eval(line))
    return mag(C)


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
expected = 4132
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    ans = 0
    nums = maplist(eval, lines)
    for i, line1 in enumerate(nums):
        for j, line2 in enumerate(nums):
            if i == j:
                continue
            ans = max(ans, mag(add(line1, line2)))
    return ans


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 3993
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
expected = 4685
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
