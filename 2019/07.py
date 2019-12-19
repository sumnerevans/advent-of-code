#! /usr/bin/env python3

import sys
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools

with open('07.txt') as f:
    intape = tuple(int(x) for x in f.read().split(','))


def run(tape, inputs, pc=0):
    inputs = iter(inputs)

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

    def get_value(idx, mode):
        if mode == 0:
            return tape[idx]
        else:
            return idx

    while True:
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
            tape[tape[pc + 1]] = int(next(inputs))
        elif opcode == 4:
            return get_value(tape[pc + 1], m1), pc + 2
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
        elif opcode == 99:
            return None, None
        else:
            print('!!!!! ERROR !!!!!')
            print(f'BAD OPCODE {opcode}')
            print(f'PC: {pc}')
            print(f'TAPE: {tape}')
            sys.exit(1)

        pc += pc_inc

    print('!!!!! ERROR !!!!!')
    print('Should exit using opcode 99.')
    sys.exit(1)


print('Part 1:')

max_thrust = 0
for phases in itertools.permutations(range(5)):
    current_input = 0
    for i in range(5):
        current_input, pc = run(list(intape), [phases[i], current_input])

    max_thrust = max(max_thrust, current_input)

print(max_thrust)

print('Part 2:')


def run_with_phases(phases):
    tapes = [list(intape) for _ in range(5)]
    pcs = [0 for _ in range(5)]

    current_input = 0

    # First round.
    for i in range(5):
        current_input, pcs[i] = run(
            tapes[i],
            [phases[i], current_input],
            pc=pcs[i],
        )

    # Subsequent rounds.
    i = 0
    while True:
        output, pcs[i] = run(
            tapes[i],
            [current_input],
            pc=pcs[i],
        )
        if output is None:
            return current_input

        current_input = output
        i = (i + 1) % 5

    raise Exception("shouldn't ge here")


max_thrust = 0
max_phases = None
for phases in itertools.permutations(range(5, 10)):
    result = run_with_phases(phases)
    if result > max_thrust:
        max_thrust = result
        max_phases = phases

print(max_thrust, 'with', max_phases)
