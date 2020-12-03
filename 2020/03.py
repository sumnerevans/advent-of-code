#! /usr/bin/env python3

import os
import re
import select
import sys
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools
from functools import partial

rows = [l.strip() for l in sys.stdin.readlines()]
n = len(rows)
cols = len(rows[0])

########################################################################################

print('Part 1:')


def part1(dx, dy):
    col = 0
    t = 0
    for row in range(0, n, dy):
        if rows[row][col % cols] == '#':
            t += 1

        col += dx
    return t


print(part1(3, 1))

########################################################################################
print('\nPart 2:')


def part2():
    return part1(3, 1) * part1(1, 1) * part1(5, 1) * part1(7, 1) * part1(1, 2)


print(part2())
