#! /usr/bin/env python3

import sys
from enum import IntEnum
from typing import List, Optional, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Crazy Machine
class OC(IntEnum):
    """Opcodes for the Harvard-architecture machine."""

    jmp = 0  # jump relative to PC+1
    acc = 1  # update accumulator
    nop = 2  # do nothing
    trm = 3  # terminate program


# Change if you add instructions
assert len(OC) == 4
Tape = List[Tuple[OC, Tuple[int, ...]]]


def decode_tape(lines: List[str]) -> Tape:
    return [(OC[c], tuple(int(v) for v in vals)) for c, *vals in map(str.split, lines)]


def run_harvard(tape: Tape, return_acc_if_loop: bool = True) -> Optional[int]:
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


# Input parsing
with open("inputs/08.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]

tape = decode_tape(lines)


########################################################################################
print("Part 1:")


def part1():
    return run_harvard(tape)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = [1815]
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 1810

########################################################################################
print("\nPart 2:")


def part2():
    for i, (oc, v) in enumerate(tape):
        if oc == OC.jmp:
            ntape = tape[:i] + [(OC.nop, v)] + tape[i + 1 :] + [(OC.trm, (0,))]
        elif oc == OC.nop:
            ntape = tape[:i] + [(OC.jmp, v)] + tape[i + 1 :] + [(OC.trm, (0,))]
        else:
            continue

        result = run_harvard(ntape, return_acc_if_loop=False)
        if result:
            return result


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 969
