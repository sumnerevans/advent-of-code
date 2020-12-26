#! /usr/bin/env python3

import sys
import time
from typing import List

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
with open("inputs/25.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]

PK1 = int(lines[0])
PK2 = int(lines[1])

input_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    """
    This problem involved doing efficient modular exponentiation. A memory efficient
    method is required:
    https://en.wikipedia.org/wiki/Modular_exponentiation#Memory-efficient_method

    The base algorithm is as follows:
    1. Set c = 1, e′ = 0.
    2. Increase e′ by 1.
    3. Set c = (b ⋅ c) mod m.
    4. If e′ < e, go to step 2. Else, c contains the correct solution to c ≡ b^e (mod m)

    There is one extra step for this, though, as during the above process, you have to
    check c against the two public keys and once we have the e' corresponding to each of
    the public keys, we can just exit the loop.
    """
    m = 20201227
    c = 1
    eprime = 0
    ls1, ls2 = 0, 0
    while True:
        eprime += 1
        c = (7 * c) % m
        if c == PK1:
            ls1 = eprime
        elif c == PK2:
            ls2 = eprime
        if ls1 > 0 or ls2 > 0:
            break

    # Doing the base algorithm to find the answer here
    c = 1
    eprime = 0
    if ls1 > 0:
        while eprime < ls1:
            eprime += 1
            c = (PK2 * c) % 20201227
        return c
    else:
        while eprime < ls2:
            eprime += 1
            c = (PK1 * c) % 20201227
        return c


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 448851

if debug:
    input_parsing = input_end - input_start
    part1_time = part1_end - part1_start
    print()
    print("DEBUG:")
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + part1_time) * 1000}ms")
