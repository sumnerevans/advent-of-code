#! /usr/bin/env python3

from dataclasses import dataclass
import re
import sys
import time
from typing import List, Match, Optional, Set, Iterator

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "inputs/22.txt"
TESTFILENAME = "inputs/22.test.txt"
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


# Utilities
def rematch(pattern: str, s: str) -> Match:
    match = re.fullmatch(pattern, s)
    assert match is not None
    return match


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
INF = 2 ** 128


@dataclass(frozen=True)
class Cuboid:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def __post_init__(self):
        assert self.x1 <= self.x2
        assert self.y1 <= self.y2
        assert self.z1 <= self.z2

    def area(self):
        return abs(self.x2 - self.x1) * abs(self.y2 - self.y1) * abs(self.z2 - self.z1)

    def complement_cuboids(self) -> Iterator["Cuboid"]:
        yield Cuboid(-INF, self.x1, -INF, INF, -INF, INF)
        yield Cuboid(self.x2, INF, -INF, INF, -INF, INF)
        yield Cuboid(self.x1, self.x2, -INF, INF, -INF, self.z1)
        yield Cuboid(self.x1, self.x2, -INF, INF, self.z2, INF)
        yield Cuboid(self.x1, self.x2, -INF, self.y1, self.z1, self.z2)
        yield Cuboid(self.x1, self.x2, self.y2, INF, self.z1, self.z2)

    def intersect(self, other: "Cuboid") -> Optional["Cuboid"]:
        if other is None:
            return self
        nx1 = max(self.x1, other.x1)
        nx2 = min(self.x2, other.x2)
        ny1 = max(self.y1, other.y1)
        ny2 = min(self.y2, other.y2)
        nz1 = max(self.z1, other.z1)
        nz2 = min(self.z2, other.z2)
        if nx1 >= nx2 or ny1 >= ny2 or nz1 >= nz2:
            return None
        return Cuboid(nx1, nx2, ny1, ny2, nz1, nz2)


def calc_lit(lines: List[str], CULLER=None) -> int:
    lit_cuboids: Set[Cuboid] = set()

    for line in lines:
        onoff, *vals = rematch(
            r"(on|off) x=([\d-]+)..([\d-]+),y=([\d-]+)..([\d-]+),z=([\d-]+)..([\d-]+)",
            line,
        ).groups()

        x1, x2, y1, y2, z1, z2 = map(int, vals)
        C = Cuboid(x1, x2 + 1, y1, y2 + 1, z1, z2 + 1)

        new_lit_cuboids = set()
        if onoff == "on":
            new_lit_cuboids.add(C.intersect(CULLER))

        for comp_c in C.complement_cuboids():
            for cc in lit_cuboids:
                nc = comp_c.intersect(cc)
                if nc and nc.area() > 0:
                    new_lit_cuboids.add(nc.intersect(CULLER))

        lit_cuboids = {x for x in new_lit_cuboids if x is not None}

    return sum(map(Cuboid.area, lit_cuboids))


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    return calc_lit(lines, Cuboid(-50, 50, -50, 50, -50, 50))


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 474140
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
expected = 542711
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    return calc_lit(lines)


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 2758514936282235
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part2} != {expected}{bcolors.ENDC}")
            print(f"{bcolors.FAIL}{test_ans_part2}\n{expected}{bcolors.ENDC}")
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
expected = 1160303042684776
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
