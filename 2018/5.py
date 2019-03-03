#! /usr/bin/env python3

import re
from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Tuple

with open('5.txt') as f:
    polymer = f.readline().strip()

alphabet = ''.join([chr(ord('a') + i) for i in range(26)])
ALPHABET = ''.join([chr(ord('A') + i) for i in range(26)])

print(alphabet)
print(ALPHABET)


def should_remove(a, b):
    if a in alphabet:
        if b in ALPHABET:
            return alphabet.index(a) == ALPHABET.index(b)
    elif b in alphabet:
        if a in ALPHABET:
            return alphabet.index(b) == ALPHABET.index(a)
    return False


def react(polymer):
    i = len(polymer) - 1
    while i > 0:
        if len(polymer) <= i:  # Prevent explosions
            break
        if should_remove(polymer[i - 1], polymer[i]):
            polymer = polymer[:i - 1] + polymer[i + 1:]

        i -= 1

    return polymer


print('Part 1:')
print(len(react(polymer)))

print('Part 2:')

min_len = 2**20
for c in alphabet:
    new_polymer = polymer
    i = len(new_polymer) - 1
    while i >= 0:
        if new_polymer[i].lower() == c:
            new_polymer = new_polymer[:i] + new_polymer[i + 1:]
        i -= 1

    r = react(new_polymer)
    assert not c in new_polymer
    assert not c.upper() in new_polymer
    if len(r) < min_len:
        min_len = len(r)

print(min_len)
