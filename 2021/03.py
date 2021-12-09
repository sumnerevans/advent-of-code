#! /usr/bin/env python3

import sys
import time
from copy import deepcopy
from typing import List, Tuple, Union

test = True
debug = False
stdin = False
INFILENAME = "inputs/03.txt"
TESTFILENAME = "inputs/03.test.txt"
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
def bitstrtoint(s: Union[str, List]) -> int:
    if isinstance(s, list):
        s = "".join(map(str, s))
    return int(s, 2)


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
def calculate_frequencies(candidates: List[str]) -> Tuple[List[int], List[int]]:
    """
    Calculate the frequencies of ``0``s and ``1``s at each index of each of the elements
    in the input.
    """
    zeros = [0] * len(candidates[0])
    ones = [0] * len(candidates[0])
    for candidate in candidates:
        for i, c in enumerate(candidate):
            if c == "0":
                zeros[i] += 1
            else:
                ones[i] += 1
    return zeros, ones


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    freq0, freq1 = calculate_frequencies(lines)

    # Store the bitmap as a list of integers. If there are more zeros than ones, then
    # that index is 0, otherwise, that index should be 1.
    gamma = [0 if zeros > ones else 1 for zeros, ones in zip(freq0, freq1)]

    # Epsilon is just the complement of gamma
    epsilon = [1 if x == 0 else 0 for x in gamma]
    return bitstrtoint(gamma) * bitstrtoint(epsilon)


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 198
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part1 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")

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
expected = None
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    def keep(candidates: List[str], i: int, val: str) -> List[str]:
        """
        Returns a new list with only the candidates that have ``val`` at index ``i``.
        """
        new_candidates = []
        for candidate in candidates:
            if candidate[i] == val:
                new_candidates.append(candidate)
        return new_candidates

    oxygen_candidates = deepcopy(lines)
    co2_candidates = deepcopy(lines)

    for i in range(len(lines)):
        if len(oxygen_candidates) == 1 == len(co2_candidates):
            return bitstrtoint(oxygen_candidates[0]) * bitstrtoint(co2_candidates[0])

        freq0_oxygen, freq1_oxygen = calculate_frequencies(oxygen_candidates)
        freq0_co2, freq1_co2 = calculate_frequencies(co2_candidates)

        if len(oxygen_candidates) > 1:
            oxygen_candidates = keep(
                oxygen_candidates,
                i,
                # Keep 1s if there are more ones than zeros
                "1" if freq0_oxygen[i] <= freq1_oxygen[i] else "0",
            )

        if len(co2_candidates) > 1:
            co2_candidates = keep(
                co2_candidates,
                i,
                # Keep 0s if there are more ones than zeros (we want the complement)
                "0" if freq0_co2[i] <= freq1_co2[i] else "1",
            )

    assert False


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 230
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")

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
expected = None
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
