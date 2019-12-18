#! /usr/bin/env python3

import sys
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools

with open('5.txt') as f:
    intape = tuple(int(x) for x in f.read().split(','))


def digits(number, n=None, default=0):
    digits = []
    while number > 0:
        digits = [number % 10] + digits
        number //= 10

    # Fill in the rest with the default.
    if n is not None:
        while len(digits) < n:
            digits = [default] + digits

    return digits


def decode_instr(i):
    opcode = i % 100
    modes = reversed(tuple(x == 1 for x in digits(i // 100, n=3)))
    return opcode, tuple(modes)


def run(tape):
    def get_value(idx, mode):
        if mode == 0:
            return tape[idx]
        else:
            return idx

    pc = 0
    while tape[pc] != 99:
        opcode, (m1, m2, m3) = decode_instr(tape[pc])
        pc_inc = 0
        if opcode == 1:
            pc_inc = 4
            in1, in2, out = tape[pc + 1:pc + 4]
            tape[out] = get_value(in1, m1) + get_value(in2, m2)
        elif opcode == 2:
            pc_inc = 4
            in1, in2, out = tape[pc + 1:pc + 4]
            tape[out] = get_value(in1, m1) * get_value(in2, m2)
        elif opcode == 3:
            pc_inc = 2
            tape[tape[pc + 1]] = int(input())
        elif opcode == 4:
            pc_inc = 2
            print(get_value(tape[pc + 1], m1))
        elif opcode == 5:
            cond, jump = tape[pc + 1:pc + 3]
            if get_value(cond, m1) != 0:
                pc = get_value(jump, m2)
            else:
                pc_inc = 3
        elif opcode == 6:
            cond, jump = tape[pc + 1:pc + 3]
            if get_value(cond, m1) == 0:
                pc = get_value(jump, m2)
            else:
                pc_inc = 3
        elif opcode == 7:
            pc_inc = 4
            in1, in2, out = tape[pc + 1:pc + 4]
            tape[out] = 1 if get_value(in1, m1) < get_value(in2, m2) else 0
        elif opcode == 8:
            pc_inc = 4
            in1, in2, out = tape[pc + 1:pc + 4]
            tape[out] = 1 if get_value(in1, m1) == get_value(in2, m2) else 0
        else:
            print('!!!!! ERROR !!!!!')
            print(f'BAD OPCODE {opcode}')
            print(f'PC: {pc}')
            print(f'TAPE: {tape}')
            sys.exit(1)

        pc += pc_inc

    return tape[0]


print('Part 1:')

run(list(intape))

print('Part 2:')

run(list(intape))
