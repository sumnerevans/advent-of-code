#! /usr/bin/env python3

import re
from collections import defaultdict
from functools import lru_cache
from typing import Dict, List, Tuple

INF = float('inf')

coordinates = []
with open('6.txt') as f:
    for line in f:
        x, y = (int(x) for x in line.split(', '))
        coordinates.append((x, y))


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


@lru_cache(maxsize=None)
def closest_coord(p):
    return min(coordinates, key=lambda c: dist(c, p))


def area(coord):
    return 10000


print('Part 1:')

max_area = 0
for c in coordinates:
    a = area(c)
    if a < INF and a > max_area:
        max_area = a

print(max_area)

print('Part 2:')
