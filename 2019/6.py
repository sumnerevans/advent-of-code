#! /usr/bin/env python3

import re
from collections import defaultdict
from typing import Dict, List, Tuple
from queue import Queue
import itertools

# X -> Y ==> X orbits Y
orbits_tree = {}

# X -> [Y, Z] ==> you can get to Y or Z from X
orbits_graph = defaultdict(list)

orbit_re = re.compile(r'(.*)\)(.*)')
with open('6.txt') as f:
    for line in f:
        Y, X = orbit_re.match(line).groups()
        orbits_tree[X] = Y

        orbits_graph[X].append(Y)
        orbits_graph[Y].append(X)

print('Part 1:')

count = 0
for obj in orbits_tree:
    current = obj
    while current in orbits_tree:
        count += 1
        current = orbits_tree[current]

print(count)

print('Part 2:')


def bfs_step_count(start, finish):
    visited = set()
    queue = Queue()
    parents = {}
    queue.put(start)
    while not queue.empty():
        current = queue.get()
        if current in visited:
            continue
        visited.add(current)

        for adj in orbits_graph[current]:
            if adj in visited:
                continue
            queue.put(adj)
            parents[adj] = current

    # Traceback
    path_len = 0
    current = 'SAN'
    while current != 'YOU':
        path_len += 1
        current = parents[current]

    return path_len


print(bfs_step_count('YOU', 'SAN') - 2)
