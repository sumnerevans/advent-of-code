#! /usr/bin/env python3

import os
from fractions import Fraction
import re
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple
import itertools
import progressbar

Point = namedtuple('Point', ('x', 'y'))

with open('10.txt') as f:
    grid = [[Point(x, y) for x, c in enumerate(line.strip()) if c == '#']
            for y, line in enumerate(f)]
    coords = tuple(itertools.chain(*grid))

print('Part 1:')


def obstructed(coord1, coord2):
    if coord1.x == coord2.x:
        # Veritcal line. Look at all coordinates between y1 and y2.
        for c in coords:
            if c == coord1 or c == coord2 or c.x != coord1.x:
                continue
            if coord1.y < c.y < coord2.y or coord1.y > c.y > coord2.y:
                return True
        return False

    if coord1.y == coord2.y:
        # Horizontal line. Look at all coordinates between x1 and x2.
        for c in coords:
            if c == coord1 or c == coord2 or c.y != coord1.y:
                continue
            if coord1.x < c.x < coord2.x or coord1.x > c.x > coord2.x:
                return True
        return False

    for c in coords:
        if c in (coord1, coord2):
            continue
        if ((coord1.x < c.x < coord2.x or coord2.x < c.x < coord1.x)
                and (coord1.y < c.y < coord2.y or coord2.y < c.y < coord1.y)):
            slope_AB = Fraction(coord2.y - coord1.y, coord2.x - coord1.x)
            slope_AC = Fraction(c.y - coord1.y, c.x - coord1.x)
            if slope_AB == slope_AC:
                return True

    return False


max_viewable = 0
for asteroid in progressbar.progressbar(coords):
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
