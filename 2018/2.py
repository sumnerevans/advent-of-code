#! /usr/bin/env python3

from collections import defaultdict

with open('2.txt') as f:
    ids = [line.strip() for line in f]

print('Part 1:')
twos, threes = 0, 0
for i in ids:
    appearances = defaultdict(int)
    for c in i:
        appearances[c] += 1

    has_two, has_three = False, False
    for k, v in appearances.items():
        if v == 2:
            has_two = True
        elif v == 3:
            has_three = True

    if has_two:
        twos += 1
    if has_three:
        threes += 1

print('Twos:  ', twos)
print('Threes:', threes)

print('Twos * Threes = ', twos * threes)

print('Part 2')


def diff(id1, id2):
    diff = []
    for i in range(len(id1)):
        if id1[i] != id2[i]:
            diff.append(i)
    return diff


for i, id1 in enumerate(ids):
    for id2 in ids[i + 1:]:
        d = diff(id1, id2)
        if len(d) == 1:
            print(id1)
            print(id2)
            remove = d[0]
            print(id1[:remove] + '-' + id1[remove + 1:])
            print('Answer:', id1[:remove] + id1[remove + 1:])
