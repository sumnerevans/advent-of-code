#! /usr/bin/env python3

import math
import os
from fractions import Fraction
import re
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple
import itertools
import progressbar
from functools import partial

Point = namedtuple('Point', ('x', 'y'))

with open('10.txt') as f:
    grid = [[Point(x, -y) for x, c in enumerate(line.strip()) if c == '#']
            for y, line in enumerate(f)]
    coords = tuple(itertools.chain(*grid))


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


def angle_between(coord1, coord2):
    return math.atan2((coord2.y - coord1.y), (coord2.x - coord1.x))


def angle_from_pi_over_2(angle):
    if angle > math.pi / 2:
        return 1.5 * math.pi + (math.pi - angle)

    return (math.pi / 2) - angle


max_viewable = 0
base_coord = None
for asteroid in progressbar.progressbar(coords):
    viewable = 0
    for other in coords:
        if asteroid == other:
            continue

        if not obstructed(asteroid, other):
            viewable += 1

    if viewable > max_viewable:
        max_viewable = viewable
        base_coord = asteroid

print('Part 1:')
print(max_viewable)

print('Part 2:')

points_with_angle = defaultdict(list)

for coord in coords:
    if coord == base_coord:
        continue

    points_with_angle[angle_between(base_coord, coord)].append(coord)

sorted_angles = list(sorted(points_with_angle, key=angle_from_pi_over_2))

vaporized = set()

i = 0
while len(vaporized) < 200:
    in_line = list(
        sorted(
            points_with_angle[sorted_angles[i]],
            key=partial(math.dist, base_coord),
        ))
    for p in in_line:
        if p in vaporized:
            continue
        vaporized.add(p)

        if len(vaporized) == 200:
            # subtract y instead of add because we are using an inverse Y-axis.
            print(p.x * 100 - p.y)
        break

    i = (i + 1) % len(sorted_angles)
