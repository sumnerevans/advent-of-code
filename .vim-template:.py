#! /usr/bin/env python3

import itertools
import math
import os
import re
import sys
from collections import defaultdict
from enum import Enum
from functools import partial, lru_cache
from typing import Dict, List, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Constants
INF = float('inf')


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


# Crazy Machine
class OC(Enum):
    jmp = 0  # jump relative to PC+1
    acc = 1  # update accumulator
    nop = 2  # do nothing
    trm = 3  # terminate program


def decode_tape(lines):
    ops = []
    for line in lines:
        opcode, *vals = line.split()
        ops.append((OC[opcode], tuple(int(v) for v in vals)))
    return ops


def run_machine(tape, return_acc_if_loop=True):
    a = 0
    pc = 0
    seen = set()
    while True:
        if pc in seen:
            return a if return_acc_if_loop else None

        seen.add(pc)

        oc, vs = tape[pc]
        if oc == OC.trm:
            return a
        elif oc == OC.jmp:
            pc += vs[0] - 1
        elif oc == OC.acc:
            a += vs[0]
        elif oc == OC.nop:
            pass

        pc += 1

    return a


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]
# tape = decode_tape(lines)
%HERE%
for line in lines:
    pass  # (<>)

# (<>)

########################################################################################
print("Part 1:")


def part1():
    pass  # (<>)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
# assert test or ans_part1 == (<>)

########################################################################################
print("\nPart 2:")


def part2():
    pass  # (<>)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
# assert test or ans_part2 == (<>)
