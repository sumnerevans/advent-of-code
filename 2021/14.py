#! /usr/bin/env python3

import functools as ft
import math
import sys
import time
from typing import Counter, Dict, Iterable, List, Tuple, TypeVar, Union

test = True
debug = False
stdin = False
INFILENAME = "inputs/14.txt"
TESTFILENAME = "inputs/14.test.txt"
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


# Utilities
def cache():  # Python 3.9 compat
    """
    LRU cache. Make sure to treat output as immutable so that you don't override the
    cache.
    """
    return ft.lru_cache(maxsize=None)


def seqminmax(sequence: Iterable[int]) -> Tuple[int, int]:
    """
    Returns a tuple containing the minimum and maximum element of the ``sequence``.
    """
    min_, max_ = math.inf, -math.inf
    for x in sequence:
        min_ = min(min_, x)
        max_ = max(max_, x)
    return int(min_), int(max_)


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
    """
    I'm going to leave this in a cleaned-up form of my original approach.
    """
    template = lines[0]
    insertion_rules = {a: b for a, b in map(lambda line: line.split(" -> "), lines[2:])}

    for _ in range(10):
        new_template = (
            "".join(a + insertion_rules[a + b] for a, b in window(template, 2))
            + template[-1]
        )
        template = new_template

    min_, max_ = seqminmax(Counter(template).values())
    return max_ - min_


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 1588
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
expected = 2549
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    template = lines[0]
    insertion_rules = {a: b for a, b in map(lambda line: line.split(" -> "), lines[2:])}

    @cache()
    def count_between_keys(a, b, d) -> Dict[str, int]:
        """
        This really bit me in the ass because I forgot that when I return dictionaries,
        I have to actually deepcopy them before using or else it modifies the cache.
        """
        counts = Counter()
        counts[insertion_rules[a + b]] += 1
        if d == 1:
            return counts

        for k, v in count_between_keys(a, insertion_rules[a + b], d - 1).items():
            counts[k] += v
        for k, v in count_between_keys(insertion_rules[a + b], b, d - 1).items():
            counts[k] += v
        return counts

    # Add the counts for all of the elements in the actual initial template.
    counts = Counter(template)

    # Calculate the counts of characters between each of the sliding-window pairs in the
    # template.
    for a, b in window(template, 2):
        for k, v in count_between_keys(a, b, 40).items():
            counts[k] += v

    print(count_between_keys.cache_info())
    min_, max_ = seqminmax(counts.values())
    return max_ - min_


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 2188189693529
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
expected = 2516901104210
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
