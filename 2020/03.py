#! /usr/bin/env python3

from typing import List

with open("inputs/03.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]

n = len(lines)
cols = len(lines[0])

########################################################################################

print("Part 1:")


def part1(dx, dy):
    col = 0
    t = 0
    for row in range(0, n, dy):
        if lines[row][col % cols] == "#":
            t += 1

        col += dx
    return t


print(part1(3, 1))

########################################################################################
print("\nPart 2:")


def part2():
    return part1(3, 1) * part1(1, 1) * part1(5, 1) * part1(7, 1) * part1(1, 2)


print(part2())
