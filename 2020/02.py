#! /usr/bin/env python3

import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools
from functools import partial

passwords = []

with open('02.txt') as f:
    for line in f:
        bounds, letter, password = line.split()
        lower, upper = map(int, bounds.split('-'))
        letter = letter[0]
        passwords.append((lower, upper, letter, password))

########################################################################################


def part1():
    print('Part 1:')

    num_valid = 0
    for l, u, c, p in passwords:
        if l <= p.count(c) <= u:
            num_valid += 1
    return num_valid


print(part1())

########################################################################################


def part2():
    print('Part 2:')

    num_valid = 0
    for l, u, c, p in passwords:
        if (p[l - 1] == c) ^ (p[u - 1] == c):
            num_valid += 1
    return num_valid


print(part2())
