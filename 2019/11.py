#! /usr/bin/env python3

import sys
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools

with open('11.txt') as f:
    intape = tuple(int(x) for x in f.read().split(','))


class Tape:
    def __init__(self, initial_tape_state):
        self.tape = list(initial_tape_state)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if idx < len(self.tape):
                return self.tape[idx]
            else:
                return 0

        start = idx.start
        stop = idx.stop
        step = idx.step

        max_idx = max(start, stop)
        if max_idx >= len(self.tape):
            # Off the end of the tape, expand the tape to that point.
            self.tape.extend([0 for _ in range(max_idx - len(self.tape) + 1)])

        return self.tape[start:stop:step]

    def __setitem__(self, idx, value):
        if idx < 0:
            raise IndexError('Cannot set negative indexes on the tape.')

        if idx >= len(self.tape):
            # Off the end of the tape, expand the tape to that point.
            self.tape.extend([0 for _ in range(idx - len(self.tape) + 1)])

        self.tape[idx] = value

    def __str__(self):
        return str(self.tape)


def machine(tape: Tape, inputs):
    pc = 0
    relative_base = 0
    inputs = iter(inputs)

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

    def get_value(idx, mode):
        if mode == 0:
            return tape[idx]
        elif mode == 1:
            return idx
        elif mode == 2:
            return tape[relative_base + idx]

    def set_value(idx, mode, value):
        if mode == 0:
            tape[idx] = value
        elif mode == 1:
            raise Exception('Immediate mode does not work on a dest parameter')
        elif mode == 2:
            tape[relative_base + idx] = value

    while True:
        opcode, (m1, m2, m3) = decode_instr(tape[pc])
        pc_inc = 0
        if opcode == 1:
            pc_inc = 4
            in1, in2, out = tape[pc + 1:pc + 4]
            set_value(out, m3, get_value(in1, m1) + get_value(in2, m2))
        elif opcode == 2:
            pc_inc = 4
            in1, in2, out = tape[pc + 1:pc + 4]
            set_value(out, m3, get_value(in1, m1) * get_value(in2, m2))
        elif opcode == 3:
            pc_inc = 2
            set_value(tape[pc + 1], m1, int(next(inputs)))
        elif opcode == 4:
            pc_inc = 2
            yield get_value(tape[pc + 1], m1)
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
            set_value(
                out,
                m3,
                1 if get_value(in1, m1) < get_value(in2, m2) else 0,
            )
        elif opcode == 8:
            pc_inc = 4
            in1, in2, out = tape[pc + 1:pc + 4]
            set_value(
                out,
                m3,
                1 if get_value(in1, m1) == get_value(in2, m2) else 0,
            )
        elif opcode == 9:
            pc_inc = 2
            relative_base += get_value(tape[pc + 1], m1)
        elif opcode == 99:
            return
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


def run_painter_robot(start_state):
    board = defaultdict(int)
    painted = set()
    current_pos = (0, 0)
    current_dir = 'U'

    board[current_pos] = start_state

    def read_board_state():
        return board[current_pos]

    program = machine(
        Tape(intape),
        (rbs() for rbs in itertools.repeat(read_board_state)),
    )

    try:
        while True:
            # Paint the board the color provided by the robot.
            board[current_pos] = next(program)
            painted.add(current_pos)

            dir_change = next(program)
            if dir_change == 0:
                # Go left
                current_dir = {
                    'U': 'L',
                    'R': 'U',
                    'D': 'R',
                    'L': 'D',
                }[current_dir]
            elif dir_change == 1:
                # Go right
                current_dir = {
                    'U': 'R',
                    'R': 'D',
                    'D': 'L',
                    'L': 'U',
                }[current_dir]
            else:
                raise Exception('fail!')

            translation = {
                'U': (0, 1),
                'R': (1, 0),
                'D': (0, -1),
                'L': (-1, 0),
            }[current_dir]
            current_pos = (
                current_pos[0] + translation[0],
                current_pos[1] + translation[1],
            )
    except StopIteration:
        pass

    return painted, board


print('Part 1:')

painted, board = run_painter_robot(0)
print(len(painted))

print('Part 2:')

painted, board = run_painter_robot(1)
xs = list(map(lambda k: k[0], board.keys()))
ys = list(map(lambda k: k[1], board.keys()))

min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)

for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
        print({0: ' ', 1: '@'}[board[(x, y)]], end='')
    print()
