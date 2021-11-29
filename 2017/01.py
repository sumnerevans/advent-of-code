#! /usr/bin/env python3

import sys
import time

test = False
debug = False
stdin = False
INFILENAME = "inputs/01.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/01.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: list[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: list[str] = [l.strip() for l in f.readlines()]

chars = [int(x) for x in lines[0]]

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()
shared_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def part1() -> int:
    ans = 0

    for c1, c2 in zip(chars, chars[1:]):
        if c1 == c2:
            ans += c1

    if chars[0] == chars[-1]:
        ans += chars[-1]

    return ans


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 1119

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    ans = 0

    N = len(chars)

    for i in range(len(chars)):
        if chars[i] == chars[(i + (N // 2)) % N]:
            ans += chars[i]

    return ans


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 1420

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
