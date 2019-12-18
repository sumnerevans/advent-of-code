#! /usr/bin/env python3

import itertools

with open('2.txt') as f:
    intape = [int(x) for x in f.read().split(',')]


def run(noun, verb):
    tape = intape[:]
    tape[1] = noun
    tape[2] = verb

    pc = 0
    while tape[pc] != 99:
        op, in1, in2, out = tape[pc:pc + 4]
        if op == 1:
            tape[out] = tape[in1] + tape[in2]
        elif op == 2:
            tape[out] = tape[in1] * tape[in2]
        else:
            raise Exception('bad opcode')

        pc += 4

    return tape[0]


print('Part 1:')

print(run(12, 2))

print('Part 2:')

for noun, verb in itertools.product(range(100), range(100)):
    if run(noun, verb) == 19690720:
        print(100 * noun + verb)
        break
