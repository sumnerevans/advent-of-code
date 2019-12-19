#! /usr/bin/env python3

import re
from collections import defaultdict
from typing import Dict, List, Tuple

masses = []

with open('01.txt') as f:
    for line in f:
        masses.append(int(line))


def fuel(m):
    return m // 3 - 2


print('Part 1')
added_fuel = sum(fuel(m) for m in masses)
print(added_fuel)

print('Part 2')

total_fuel = 0

for m in masses:
    module_fuel = 0
    added_fuel = fuel(m)
    while added_fuel > 0:
        module_fuel += added_fuel
        added_fuel = fuel(added_fuel)

    total_fuel += module_fuel

print(total_fuel)
