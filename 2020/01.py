#! /usr/bin/env python3

import sys

expenses = sorted(int(l) for l in sys.stdin.readlines())
L = len(expenses)

print("Part 1:")


def part1() -> int:
    for _, a in enumerate(expenses):
        complement = 2020 - a

        low, hi = 0, L
        prev = 0
        while True:
            mid_idx = low + (hi - low) // 2
            if mid_idx == prev:
                break
            mid = expenses[mid_idx]
            if mid == complement:
                return a * complement
            elif mid < complement:
                low = mid_idx
            else:
                hi = mid_idx

    assert False


ans_part1 = part1()
print(ans_part1)
assert ans_part1 == 355875

print("Part 2:")


def part2() -> int:
    for i, a in enumerate(expenses):
        for j, b in enumerate(expenses):
            if i < j:
                continue
            for k, c in enumerate(expenses):
                if k < j or k < i:
                    continue

                if a + b + c == 2020:
                    return a * b * c
    assert False


ans_part2 = part2()
print(ans_part2)
assert ans_part2 == 140379120
