#! /usr/bin/env python3

import sys
import time
from copy import deepcopy
from typing import List, Tuple, TypeVar, Union

test = False
debug = False
stdin = False
INFILENAME = "inputs/03.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/03.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


# Type variables
K = TypeVar("K")
V = TypeVar("V")


# Utilities
def bitstrtoint(s: Union[str, List]) -> int:
    if isinstance(s, list):
        s = "".join(map(str, s))
    return int(s, 2)


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines()]

# seq = [int(x) for x in lines]


input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()


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


shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    freq0, freq1 = calculate_frequencies(lines)

    # Store the bitmap as a list of integers. If there are more zeros than ones, then
    # that index is 0, otherwise, that index should be 1.
    gamma = [0 if zeros > ones else 1 for zeros, ones in zip(freq0, freq1)]

    # Epsilon is just the complement of gamma
    epsilon = [1 if x == 0 else 0 for x in gamma]
    return bitstrtoint(gamma) * bitstrtoint(epsilon)


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 1092896
if expected is not None:
    assert test or ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
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


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 4672151
if expected is not None:
    assert test or ans_part2 == expected

if debug:
    input_parsing = input_end - input_start
    shared = shared_end - shared_start
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Shared: {shared * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + shared + part1_time + part2_time) * 1000}ms")
