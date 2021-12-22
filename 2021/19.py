#! /usr/bin/env python3

import re
import sys
import time
from collections import defaultdict
from typing import (
    Callable,
    DefaultDict,
    Dict,
    Iterable,
    Iterator,
    List,
    Match,
    Set,
    Tuple,
    TypeVar,
)

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "inputs/19.txt"
TESTFILENAME = "inputs/19.test.txt"
for arg in sys.argv:
    if arg == "--notest":
        TEST = False
    if arg == "--debug":
        DEBUG = True
    if arg == "--stdin":
        STDIN = True

THRESHOLD = 12


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
def allints(s: str) -> Iterator[int]:
    """
    Returns a list of all of the integers in the string.
    """
    return map(lambda m: int(m.group(0)), re.finditer(r"-?\d+", s))


def maplist(fn: Callable[[K], V], l: Iterable[K]) -> List[V]:
    return list(map(fn, l))


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


def rot_px_0(v):
    return (v[0], v[1], v[2])


def rot_px_90(v):
    return (v[0], -v[2], v[1])


def rot_px_180(v):
    return (v[0], -v[1], -v[2])


def rot_px_270(v):
    return (v[0], v[2], -v[1])


def rot_nx_0(v):
    return (-v[0], v[2], v[1])


def rot_nx_90(v):
    return (-v[0], -v[1], v[2])


def rot_nx_180(v):
    return (-v[0], -v[2], -v[1])


def rot_nx_270(v):
    return (-v[0], v[1], -v[2])


def rot_py_0(v):
    return (-v[1], v[0], v[2])


def rot_py_90(v):
    return (-v[2], v[0], -v[1])


def rot_py_180(v):
    return (v[1], v[0], -v[2])


def rot_py_270(v):
    return (v[2], v[0], v[1])


def rot_ny_0(v):
    return (-v[1], -v[0], -v[2])


def rot_ny_90(v):
    return (v[2], -v[0], -v[1])


def rot_ny_180(v):
    return (v[1], -v[0], v[2])


def rot_ny_270(v):
    return (-v[2], -v[0], v[1])


def rot_pz_0(v):
    return (-v[2], v[1], v[0])


def rot_pz_90(v):
    return (-v[1], -v[2], v[0])


def rot_pz_180(v):
    return (v[2], -v[1], v[0])


def rot_pz_270(v):
    return (v[1], v[2], v[0])


def rot_nz_0(v):
    return (-v[2], -v[1], -v[0])


def rot_nz_90(v):
    return (v[1], -v[2], -v[0])


def rot_nz_180(v):
    return (v[2], v[1], -v[0])


def rot_nz_270(v):
    return (-v[1], v[2], -v[0])


ROTATIONS = [
    # 4 rotations facing +X axis
    rot_px_0,
    rot_px_90,
    rot_px_180,
    rot_px_270,
    # 4 rotations facing -X axis
    rot_nx_0,
    rot_nx_90,
    rot_nx_180,
    rot_nx_270,
    # 4 rotations facing +Y axis
    rot_py_0,
    rot_py_90,
    rot_py_180,
    rot_py_270,
    # 4 rotations facing -Y axis
    rot_ny_0,
    rot_ny_90,
    rot_ny_180,
    rot_ny_270,
    # 4 rotations facing +Z axis
    rot_pz_0,
    rot_pz_90,
    rot_pz_180,
    rot_pz_270,
    # 4 rotations facing -Z axis
    rot_nz_0,
    rot_nz_90,
    rot_nz_180,
    rot_nz_270,
]

ROT_INVERSES = {}
for rf1 in ROTATIONS:
    for rf2 in ROTATIONS:
        if rf1(rf2((1, 2, 3))) == (1, 2, 3):
            ROT_INVERSES[rf1] = rf2
            break

Point = Tuple[int, ...]
Diff = Tuple[int, ...]
Transformer = Callable[[Point], Point]


def get_scanner_points_and_diffs(lines: List[str]):
    scanner_points: List[Set[Point]] = []
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

    # [{rotation -> {start_point -> {end_point: diff}}}]
    scanner_point_diffs: List[
        DefaultDict[Transformer, DefaultDict[Point, Dict[Point, Diff]]]
    ] = []
    for sp in scanner_points:
        scanner_point_diffs.append(defaultdict(lambda: defaultdict(dict)))
        for rotation_fn in ROTATIONS:
            rot_sp = maplist(rotation_fn, sp)
            for i, p1 in enumerate(rot_sp):
                for j, p2 in enumerate(rot_sp):
                    if i == j:
                        continue
                    scanner_point_diffs[-1][rotation_fn][p1][p2] = tuple(
                        b - a for a, b in zip(p1, p2)
                    )
    return scanner_points, scanner_point_diffs


def calc_scanner_rel_pos(scanner_point_diffs, threshold):
    # dictionary of scanner number -> {scanner number -> (relative offset, fns)}
    scanner_rel_pos: DefaultDict[
        int, Dict[int, Tuple[Point, Transformer]]
    ] = defaultdict(dict)

    for i, spd1 in enumerate(scanner_point_diffs):
        for j, spd2 in enumerate(scanner_point_diffs):
            # spd1 stays stable, so only consider the 0th rotation.
            spd1_no_rot = spd1[rot_px_0]

            # determine if any rotation of spd2 can get alignment with one of the points
            # in spd1
            for spd1_start_point, spd1_diffs_at_start_point in spd1_no_rot.items():
                foundmatch = False
                for rot_fn, spd2_rot in spd2.items():
                    for spd2k, spd2v in spd2_rot.items():
                        intersection = set(spd1_diffs_at_start_point.values())
                        intersection &= set(spd2v.values())
                        if len(intersection) >= threshold - 1:
                            scanner_rel_pos[i][j] = (
                                tuple(a - b for a, b in zip(spd1_start_point, spd2k)),
                                rot_fn,
                            )
                            foundmatch = True
                            break
                    if foundmatch:
                        break

                if foundmatch:
                    break
    return scanner_rel_pos


TEST_POINTS, TEST_DIFFS = get_scanner_points_and_diffs(test_lines)
TEST_SCANNER_REL_POS = calc_scanner_rel_pos(TEST_DIFFS, THRESHOLD)
REAL_POINTS, REAL_DIFFS = get_scanner_points_and_diffs(input_lines)
REAL_SCANNER_REL_POS = calc_scanner_rel_pos(REAL_DIFFS, THRESHOLD)

# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    scanner_points = TEST_POINTS if test else REAL_POINTS
    scanner_rel_pos = TEST_SCANNER_REL_POS if test else REAL_SCANNER_REL_POS

    all_beacons_rel_to_0 = set()
    for i in range(len(scanner_points)):

        def dfs(x, visited: Set[int]):
            if x == 0:
                return [((0, 0, 0), rot_px_0)]

            for a in scanner_rel_pos[x]:
                offset, rotation_fn_num = scanner_rel_pos[x][a]
                if a in visited:
                    continue
                offset_rotation_stack = dfs(a, visited.union({x}))
                if offset_rotation_stack is not None:
                    return offset_rotation_stack + [(offset, rotation_fn_num)]
            return None

        offset_rotation_stack = dfs(i, set())

        points = scanner_points[i]
        while offset_rotation_stack:
            (offset, rot_fn) = offset_rotation_stack.pop()
            points = maplist(
                lambda p: tuple(b - a for a, b in zip(ROT_INVERSES[rot_fn](offset), p)),
                map(ROT_INVERSES[rot_fn], points),
            )

        # print("  points", points)
        all_beacons_rel_to_0 = all_beacons_rel_to_0.union(points)

    return len(all_beacons_rel_to_0)


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
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
ans_part1 = part1(input_lines)
part1_end = time.time()
print("Result:", ans_part1)

tries = [
    761
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 350
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    scanner_points = TEST_POINTS if test else REAL_POINTS
    scanner_rel_pos = TEST_SCANNER_REL_POS if test else REAL_SCANNER_REL_POS

    def positions(scanner_no, visited: Set[int]) -> Set[Point]:
        points = set()
        for other_scanner_no, (offset, rotation) in scanner_rel_pos[scanner_no].items():
            if other_scanner_no in visited:
                continue
            visited.add(other_scanner_no)

            points.add(offset)
            x = positions(other_scanner_no, visited.union({scanner_no}))
            for p in x:
                points.add(tuple(a + b for a, b in zip(offset, rotation(p))))

        return points

    POSES = positions(0, set())
    if test:
        assert (-92, -2380, -20) in POSES
        assert (1105, -1205, 1229) in POSES
    assert len(POSES) == len(scanner_points)
    # ohea

    max_man = 0
    for sp1 in POSES:
        for sp2 in POSES:
            M = abs(sp1[0] - sp2[0]) + abs(sp1[1] - sp2[1]) + abs(sp1[2] - sp2[2])
            if M > max_man:
                max_man = M

    return max_man


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 3621
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
expected = 10895
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
