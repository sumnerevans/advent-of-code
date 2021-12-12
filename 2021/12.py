#! /usr/bin/env python3

import functools as ft
import re
import sys
import time
from collections import Counter, defaultdict
from typing import DefaultDict, List, Match, Optional, Set, Tuple

test = True
debug = False
stdin = False
INFILENAME = "inputs/12.txt"
TESTFILENAME = "inputs/12.test.txt"
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


# Utilities
def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


def rematch(pattern: str, s: str) -> Optional[Match]:
    return re.fullmatch(pattern, s)


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
    # So, all paths you find should visit small caves at most once, and can visit big
    # caves any number of times.

    G: DefaultDict[str, Set[str]] = defaultdict(set)

    for line in lines:
        x, y = rematch("(.*)-(.*)", line).groups()
        G[x].add(y)
        G[y].add(x)

    def paths(key, visited: Set[str]) -> int:
        if key == "end":
            return 1

        count = 0
        for a in G[key]:
            if a == "start":
                continue
            if a.islower() and a in visited:
                # This is a small cave, and we've only been here once.
                continue

            count += paths(a, {*visited, a})

        return count

    return paths("start", set())


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 10
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
part1_end = time.time()
print("Result:", ans_part1)

tries = [
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 4970
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    # After reviewing the available paths, you realize you might have time to visit a
    # single small cave twice. Specifically, big caves can be visited any number of
    # times, a single small cave can be visited at most twice, and the remaining small
    # caves can be visited at most once. However, the caves named start and end can only
    # be visited exactly once each: once you leave the start cave, you may not return to
    # it, and once you reach the end cave, the path must end immediately.

    G: DefaultDict[str, Set[str]] = defaultdict(set)

    for line in lines:
        x, y = rematch("(.*)-(.*)", line).groups()
        G[x].add(y)
        G[y].add(x)

    @cache()
    def paths(key, visited: Tuple[str]) -> int:
        if key == "end":
            return 1

        count = 0
        for a in G[key]:
            if a == "start":
                continue

            nv = visited
            if a.islower():
                if any(x >= 2 for x in Counter(visited).values()) and a in visited:
                    continue
                nv = (*nv, a)

            count += paths(a, tuple(sorted(nv)))

        return count

    return paths("start", tuple())


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 36
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
    4970
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 137948
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
