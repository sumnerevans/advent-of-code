#! /usr/bin/env python3

import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools

low, high = (178416, 676461)

print('Part 1:')


def ascending(p):
    return p == ''.join(sorted(p))


def two_adjacent_same(p):
    for a, b in zip(p, p[1:]):
        if a == b:
            return True
    return False


count = 0
for password in range(low, high + 1):
    password = str(password)
    if not ascending(password):
        continue
    if not two_adjacent_same(password):
        continue
    count += 1

print(count)

print('Part 2:')


def adjacents_lengths(p):
    counts = set()
    current_numeral = p[0]
    current_count = 1
    for x in p[1:]:
        if x != current_numeral:
            counts.add(current_count)
            current_count = 0

        current_count += 1
        current_numeral = x

    counts.add(current_count)

    return counts


count = 0
for password in range(low, high + 1):
    password = str(password)
    if not ascending(password):
        continue
    if 2 not in adjacents_lengths(password):
        continue
    count += 1

print(count)
