#! /usr/bin/env python3

import functools as ft
import itertools as it
import math
import os
import re
import sys
from copy import deepcopy
from collections import defaultdict
from enum import IntEnum
from typing import Dict, List, Tuple

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


def pbits(num, pad=32):
    return bin(num)[2:].zfill(pad)


def sizezip(*iterables):
    assert len(set(len(x) for x in iterables)) == 1
    yield from zip(*iterables)


# Input parsing
lines = [l.strip() for l in sys.stdin.readlines()]

# Here's a bit of code that I wrote after solving to figure out the bounds of my input.
max_mem_loc = 0
for l in lines:
    if rematch(r"mem\[(\d+)\] = (\d+)", l):
        max_mem_loc = max(max_mem_loc, int(rematch(r"mem\[(\d+)\] = \d+", l).group(1)))
print("The maximum memory location was:", max_mem_loc)


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    """
    Part 1, I did some bit-hacking instead of doing it stringly typed which was a
    mistake as it screwed me for part 2, and it was also way more difficult than it was
    worth.

    I also need to be better at Python's built-in integer conversion libraries.
    """
    # Using a dict to store memory because I don't want to figure out much memory to
    # pre-allocate.
    mem = {}

    # andmask and ormask start out as the identity for each of the corresponding
    # operations.
    # For any given bit, X & 1 = X
    # For any given bit, X | 0 = X
    andmask = 1
    ormask = 0
    for line in lines:
        if rematch("mask.*", line):
            # Updating the masks.
            andmask = 1
            ormask = 0

            # Go through all of the characters in the mask.
            for x in rematch("mask = (.*)", line).group(1):
                # First, binary left shift the andmask and ormask by one. This moves all
                # the bits over to the left by 1, leaving a 0 at the least-significant
                # bit (LSB).
                andmask = andmask << 1
                ormask = ormask << 1
                if x != "0":
                    # Either X or 1, we need to preserve the value, so set the andmask
                    # LSB to 1, which is the identity. If it is 0, then we let it stay
                    # because we want it to override the existing value.
                    andmask |= 1
                if x == "1":
                    # If it's a 1, then set the ormask to 1, so that it overrides it. In
                    # all other casse, we just leave the ormask as is since it is
                    # already the identity.
                    ormask |= 1
        else:
            # Destructure the memory location and apply the andmask and ormask to the
            # value before setting it.
            loc, val = map(int, rematch(r"mem\[(\d+)\] = (\d+)", line).groups())
            mem[loc] = val & andmask | ormask

    return sum(mem.values())


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = [16073107098]
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 6386593869035

########################################################################################
print("\nPart 2:")


def part2():
    """
    In this one, I converted to use stringly typed masks instead of the crazy bithacking
    that I did in Part 1.
    """
    mem = {}
    max_count_x = 0
    # this is just here to make my linter happy because it doesn't know that curmask is
    # going to be set on the first iteration of the loop.
    curmask = ""

    for line in lines:
        if rematch("mask.*", line):
            curmask = rematch("mask = (.*)", line).group(1)
        else:
            loc, val = map(int, rematch(r"mem\[(\d+)\] = (\d+)", line).groups())

            # Pad the memory access location so that it is the same size as the curmask.
            # This allows me to zip and not loose values.
            access = pbits(loc, len(curmask))

            # Compute  the result bits as a string (this allows us to have the Xs).
            result_bits = ""
            for access_loc_bit, curmask_bit in sizezip(access, curmask):
                if curmask_bit == "0":
                    result_bits += access_loc_bit
                elif curmask_bit == "1":
                    result_bits += "1"
                else:
                    result_bits += "X"

            # Compute all of the bit combos with itertools.product. This gives all of
            # the "permutations with replacement" of 0 and 1 of size N where N is the
            # number of Xs in the result.
            num_xs = result_bits.count("X")
            max_count_x = max(max_count_x, num_xs)
            for bit_combo in it.product("01", repeat=num_xs):
                # Compute the actual memory location to store the value to by going
                # through all of the bits in the result and if it's an X, using the
                # corresponding value in the bit_combo instead of X.
                real_loc = ""
                combo_idx = 0
                for b in result_bits:
                    if b in "01":
                        real_loc += b
                    else:
                        real_loc += bit_combo[combo_idx]
                        combo_idx += 1

                # Interpret it as binary
                mem[real_loc] = val

    print(
        "Max number of Xs in any given string: {} so only ever {} tuples out of\n"
        "the call to it.product".format(max_count_x, 2 ** max_count_x)
    )
    return sum(mem.values())


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 4288986482164
