#! /usr/bin/env python3

import sys

expenses = [int(l) for l in sys.stdin.readlines()]

print("Part 1:")

for i, a in enumerate(expenses):
    found = False
    for j, b in enumerate(expenses):
        if i == j:
            continue
        if a + b == 2020:
            print(a * b)
            found = True
            break
    if found:
        break

print("Part 2:")

for i, a in enumerate(expenses):
    found = False
    for j, b in enumerate(expenses):
        if i == j:
            continue
        for k, c in enumerate(expenses):
            if k == j or k == i:
                continue

            if a + b + c == 2020:
                print(a * b * c)
                found = True
                break

        if found:
            break
    if found:
        break
