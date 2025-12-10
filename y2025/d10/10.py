#! /usr/bin/env python3

import heapq
import math
import sys
import time
from typing import (Callable, Dict, Generator, Iterable, Iterator, List, Match, Optional, Set,
                    Tuple, TypeVar, Union)

import z3

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "10.txt"
TESTFILENAME = "10.test.01.txt"
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


def dijkstra(
    next_states: Callable[[K], Iterable[Tuple[int, K]]],
    start: K,
    end_state: Callable[[K], bool],
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


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    ans = 0

    for line in lines:
        lights, *buttons, _ = line.split()
        lights = lights[1:-1]
        buttons = [eval(b[:-1] + ",)") for b in buttons]

        def next_states(l):
            for b in buttons:
                s = ""
                for i, c in enumerate(l):
                    if i in b:
                        if c == "#":
                            s += "."
                        else:
                            s += "#"
                    else:
                        s += c
                yield (1, s)

        ans += dijkstra(next_states, lights.replace("#", "."), lambda l: l == lights)

    return ans


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 7
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
expected = 385
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    ans = 0

    for line in lines:
        _, *buttons, joltages = line.split()
        buttons = [eval(b[:-1] + ",)") for b in buttons]
        joltages = eval(joltages.replace("{", "(").replace("}", ")"))

        J = [z3.Int(f"j{i}") for i in range(len(joltages))]
        B = [z3.Int(f"b{i}") for i in range(len(buttons))]

        o = z3.Optimize()
        o.add(*[J[i] == j for i, j in enumerate(joltages)])
        o.add(*[b >= 0 for b in B])

        for i, j in enumerate(J):
            included = set()
            for idx, button in enumerate(buttons):
                if i in button:
                    included.add(idx)

            o.add(z3.Sum(B[i] for i in included) == j)

        o.minimize(z3.Sum(B))
        o.check()
        m = o.model()
        ans += sum(m[b].as_long() for b in B)

    return ans


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 33
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
expected = 16757
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
