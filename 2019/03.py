#! /usr/bin/env python3

import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools
from functools import partial

with open('03.txt') as f:
    wire_paths = [[x for x in line.strip().split(',')] for line in f]

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


def manhattan_distance(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2

    return abs(p2x - p1x) + abs(p2y - p1y)


print('Part 1:')
print(min(map(partial(manhattan_distance, (0, 0)),
              intersections(*wire_paths))))

print('Part 2:')


def steps(path, intersection):
    pos = (0, 0)
    steps = 0
    current_segment_steps = 0
    path_idx = 0

    # Step one-by-one to find the intersection from the start position.
    while pos != intersection:
        # Determine the direction we are going.
        direction, length = dir_re.match(path[path_idx]).groups()
        length = int(length)
        if direction == 'L':
            pos = (pos[0] - 1, pos[1])
        elif direction == 'R':
            pos = (pos[0] + 1, pos[1])
        elif direction == 'U':
            pos = (pos[0], pos[1] + 1)
        elif direction == 'D':
            pos = (pos[0], pos[1] - 1)

        # Go on to the next segment when we reach the end of this one.
        current_segment_steps += 1
        if length == current_segment_steps:
            current_segment_steps = 0
            path_idx += 1
        steps += 1

    return steps


print(
    min(
        steps(wire_paths[0], intersection) + steps(wire_paths[1], intersection)
        for intersection in intersections(*wire_paths)))
