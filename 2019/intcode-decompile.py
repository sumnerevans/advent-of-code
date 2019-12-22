#! /usr/bin/env python3

import sys
import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools
from functools import partial

with open(sys.argv[1]) as f:
    intape = enumerate(int(x) for x in f.read().split(','))


def digits(number, n=None, default=0):
    digits = []
    while number > 0:
        digits.append(number % 10)
        number //= 10

    # Fill in the rest with the default.
    if n is not None:
        while len(digits) < n:
            digits.append(default)

    return digits


def decode_instr(i):
    opcode = i % 100
    modes = tuple(x for x in digits(i // 100, n=3))
    return opcode, modes


def nextval():
    try:
        return next(intape)[1]
    except StopIteration:
        return 0


# Handle offset arg.
offset = 0
if len(sys.argv) > 2:
    offset = int(sys.argv[2])

instructions = []
for idx, i in intape:
    if idx < offset or len(digits(i)) > 5:
        instructions.append((idx, i, None))
        continue

    opcode, modes = decode_instr(i)
    if opcode == 1:
        in1, in2, out = nextval(), nextval(), nextval()
        instructions.append((idx, 'ADD', modes, in1, in2, out))
    elif opcode == 2:
        in1, in2, out = nextval(), nextval(), nextval()
        instructions.append((idx, 'MULT', modes, in1, in2, out))
    elif opcode == 3:
        out = nextval()
        instructions.append((idx, 'READTO', modes, out))
    elif opcode == 4:
        val = nextval()
        instructions.append((idx, 'OUTPUT', modes, val))
    elif opcode == 5:
        cond, jump = nextval(), nextval()
        instructions.append((idx, 'JNEQZ', modes, cond, jump))
    elif opcode == 6:
        cond, jump = nextval(), nextval()
        instructions.append((idx, 'JEQZ', modes, cond, jump))
    elif opcode == 7:
        in1, in2, out = nextval(), nextval(), nextval()
        instructions.append((idx, 'SLT', modes, in1, in2, out))
    elif opcode == 8:
        in1, in2, out = nextval(), nextval(), nextval()
        instructions.append((idx, 'SEQ', modes, in1, in2, out))
    elif opcode == 9:
        rb = nextval()
        instructions.append((idx, 'SRB', modes, rb))
    elif opcode == 99:
        instructions.append((idx, 'EXIT', None))
    else:
        instructions.append((idx, i, None))

for idx, op, modes, *vals in instructions:

    def val_with_mode(value, mode):
        if mode == 0:
            return f'T[{value}]'
        elif mode == 1:
            return str(value)
        elif mode == 2:
            return f'T[RB+{value}]'

    args = []
    if vals is not None and modes is not None:
        args = map(val_with_mode, vals, modes)

    print(f'{idx:>5}: {op:>6}', *map(lambda x: f'{x:9}', args))
