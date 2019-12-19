#! /usr/bin/env python3

import os
from fractions import Fraction
import re
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple
import itertools

Point = namedtuple('Point', ('x', 'y'))

with open('10.txt') as f:
    grid = [[Point(x, y) for x, c in enumerate(line.strip()) if c == '#']
            for y, line in enumerate(f)]
    coords = list(itertools.chain(*grid))

print('Part 1:')


def obstructed(coord1, coord2):
    if coord2.x == coord2.x:
        # TODO
        return False
    slope = Fraction(coord2.y - coord1.y, coord2.x - coord1.x)
    print(slope)


max_viewable = 0
for asteroid in coords:
    viewable = 0
    for other in coords:
        if asteroid == other:
            continue

        if not obstructed(asteroid, other):
            viewable += 1

    if viewable > max_viewable:
        max_viewable = viewable

print(max_viewable)

print('Part 2:')

