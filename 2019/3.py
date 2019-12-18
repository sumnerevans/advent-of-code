#! /usr/bin/env python3

import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools

with open('3.txt') as f:
    wire_paths = [[x for x in line.split(',')] for line in f]

dir_re = re.compile(r'(L|R|U|D)(.*)')


def lines(path):
    vert_lines = []
    hor_lines = []
    pos = (0, 0)
    for dir_spec in path:
        direction, length = dir_re.match(dir_spec).groups()
        length = int(length)
        if direction in ('L', 'R'):
            if direction == 'L':
                x1, x2 = pos[0] - length, pos[0]
            else:
                x1, x2 = pos[0], pos[0] + length
            hor_lines.append((pos[1], (x1, x2)))
        elif direction in ('U', 'D'):
            if direction == 'D':
                y1, y2 = pos[1] - length, pos[1]
            else:
                y1, y2 = pos[1], pos[1] + length
            vert_lines.append((pos[0], (y1, y2)))

        if direction == 'L':
            pos = (pos[0] - length, pos[1])
        elif direction == 'R':
            pos = (pos[0] + length, pos[1])
        elif direction == 'U':
            pos = (pos[0], pos[1] + length)
        elif direction == 'D':
            pos = (pos[0], pos[1] - length)

    return vert_lines, hor_lines


def intersections(p1, p2):
    vert_lines1, hor_lines1 = lines(p1)
    vert_lines2, hor_lines2 = lines(p2)

    def intersects(hor_line, vert_line):
        y, (x_0, x_1) = hor_line
        x, (y_0, y_1) = vert_line

        if x_0 <= x <= x_1 and y_0 <= y <= y_1:
            return (x, y)

    for hl1 in hor_lines1:
        for vl2 in vert_lines2:
            i = intersects(hl1, vl2)
            if i:
                yield i

    for hl2 in hor_lines2:
        for vl1 in vert_lines1:
            i = intersects(hl2, vl1)
            if i:
                yield i


print('Part 1:')

(map(lambda i: (sum(i), i), intersections(*wire_paths)))

print(list(intersections(*wire_paths)))

print('Part 2:')
