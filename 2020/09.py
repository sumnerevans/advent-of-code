#! /usr/bin/env python3

import sys

test = False
P = 25
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True
        P = 5


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]
seq = [int(x) for x in lines]

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    current = seq[:P]
    i = P
    while True:
        sumof = False
        for j, a in enumerate(current):
            for k, b in enumerate(current):
                if j < k:
                    continue
                if a + b == seq[i]:
                    sumof = True
                    break
        if not sumof:
            return seq[i]

        current = current[1:] + [seq[i]]

        i += 1


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 18272118

########################################################################################
print("\nPart 2:")


# This is what I used to solve first. It's very inefficient, but effective.
def part2():  # O(3n^3)
    for s in range(len(seq)):
        for e in range(s, len(seq)):
            if sum(seq[s : e + 1]) == ans_part1:
                return max(seq[s : e + 1]) + min(seq[s : e + 1])


# This is a much cleaner way to do the same thing, removing a factor of 3n from the
# complexity.
def part2_cleaner():  # O(n^2)
    for s in range(len(seq)):
        current_sum = 0
        current_min = float("inf")
        current_max = 0
        for e in range(len(seq) - s):
            c = seq[s + e]
            current_sum += c
            current_min = min(current_min, c)
            current_max = max(current_max, c)
            if current_sum == ans_part1:
                return current_min + current_max


ans_part2 = part2_cleaner()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 2186361
