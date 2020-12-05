#! /usr/bin/env python3

import itertools
import math
import os
import re
import sys
from collections import defaultdict
from functools import partial
from typing import Dict, List, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == '--test':
        test = True


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


# Input parsing

lines = [l.strip() for l in sys.stdin.readlines()]
%HERE%
for line in lines:
    pass  # (<>)

# (<>)

########################################################################################
print('Part 1:')


def part1():
    pass  # (<>)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print(tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
# assert test or ans_part1 == (<>)

########################################################################################
print('\nPart 2:')


def part2():
    pass  # (<>)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries = []
print(tries)
assert ans_part2 not in tries, "Same as an incorrect answer!"

# Regression Test
# assert test or ans_part2 == (<>)
