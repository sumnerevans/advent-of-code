#! /usr/bin/env python3

import re
from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Tuple

line_re = re.compile(r'#(\d*) @ (\d*),(\d*): (\d*)x(\d*)')
claims: [Tuple[int]] = []
with open('3.txt') as f:
    for line in f:
        claims.append(tuple(int(x) for x in line_re.match(line).groups()))

print('Part 1:')

max_x = max(x + dx for (i, x, y, dx, dy) in claims)
max_y = max(y + dy for (i, x, y, dx, dy) in claims)

plane = [[0 for j in range(max_x)] for i in range(max_y)]

for c in claims:
    id_, x, y, dx, dy = c
    for i in range(y, y + dy):
        for j in range(x, x + dx):
            plane[i][j] += 1

count_intersect = 0
for row in plane:
    for col in row:
        if col > 1:
            count_intersect += 1

print('Intersection:', count_intersect)

print('Part 2:')


def claim_intersects(x, y, dx, dy):
    for i in range(y, y + dy):
        for j in range(x, x + dx):
            if plane[i][j] > 1:
                return True

    return False


for c in claims:
    id_, *dimens = c
    if not claim_intersects(*dimens):
        print(id_)
