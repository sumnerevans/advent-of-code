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

# Constants
INF = float("inf")
COMPASS_GRID_DIRS = [  # Tuples of (delta_row, delta_col)
    (0, 1),  # right
    (1, 0),  # below
    (0, -1),  # left
    (-1, 0),  # above
]
DIAG_GRID_DIRS = [  # Tuples of (delta_row, delta_col)
    (-1, -1),  # top-left
    (-1, 1),  # top-right
    (1, -1),  # bottom-left
    (1, 1),  # bottom-right
]
GRID_DIRS = COMPASS_GRID_DIRS + DIAG_GRID_DIRS


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


def cache():  # Python 3.9 compat
    return ft.lru_cache(maxsize=None)


def grid_adjs(row, col, max_row, max_col, dirs=GRID_DIRS):
    # Iterate through all of the directions and return all of the (row, col) tuples
    # representing the adjacent cells.
    for dy, dx in dirs:
        if 0 <= row + dy < max_row and 0 <= col + dx < max_col:
            yield row + dy, col + dx


def rot(x, y, deg, origin=(0, 0)):
    theta = deg * math.pi / 180
    x2 = round((x - origin[0]) * math.cos(theta) - (y - origin[1]) * math.sin(theta))
    y2 = round((x - origin[0]) * math.sin(theta) + (y - origin[1]) * math.cos(theta))
    return (x2 + origin[0], y2 + origin[1])


def manhattan(x1, y1, x2=0, y2=0):
    return abs(x2 - x1) + abs(y2 - y1)


# Crazy Machine
class OC(IntEnum):
    jmp = 0  # jump relative to PC+1
    acc = 1  # update accumulator
    nop = 2  # do nothing
    trm = 3  # terminate program


# Change if you add instructions
assert len(OC) == 4


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


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    s = int(lines[0])
    busses = []
    for b in lines[1].split(","):
        if b == "x":
            continue

        busses.append(int(b))

    print(s)
    c = s
    while True:
        print(s, [s // b for b in busses])
        for b in busses:
            if c % b == 0:
                return b * (c - s)
        c += 1

    print(busses)


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 3882

########################################################################################
print("\nPart 2:")

from functools import reduce  # Python version 3.x


def lcm(denominators):
    print("lcm", denominators)
    return reduce(lambda a, b: a * b // math.gcd(a, b), denominators)


def seqgcd(d):
    return reduce(lambda a, b: math.gcd(a, b), d)


def part2_old():
    busses = []
    gaps = [0]
    for b in lines[1].split(","):
        if b == "x":
            gaps[-1] += 1
            continue
        else:
            gaps.append(1)
            busses.append(int(b))

    mb = 0
    mi = 0
    for i, b in enumerate(busses):
        if b > mb:
            mb = b
            mi = i

    A = sum(gaps)
    i = busses[0]
    k = 0
    while True:
        if k % 100000 == 0:
            print(i)
        ok = True
        for j, b in enumerate(busses[1:]):
            if i % b != b - sum(gaps[: j + 2]):
                ok = False
                break
        if ok:
            return i

        k += 1
        i += busses[0]


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def arrow_alignment(red_len, green_len, advantage):
    print("aa", "r:", red_len, "g:", green_len, "a:", advantage)
    """Where the arrows first align, where green starts shifted by advantage"""
    period, phase = combine_phased_rotations(
        red_len, 0, green_len, -advantage % green_len
    )
    return -phase % period


def part2_2():
    print(lines[1].split(","))
    busses = []
    gaps = [0]
    for b in lines[1].split(","):
        if b == "x":
            gaps[-1] += 1
            continue
        else:
            gaps.append(1)
            busses.append(int(b))

    # print(busses, gaps)

    # print(seqgcd([b + gaps[i] for i, b in enumerate(busses)]))
    # print("gcd", seqgcd(busses))
    # print("lcm", lcm([busses[0], busses[1]]), gaps[0], gaps[1])
    # K = lcm([busses[0], busses[-1]])
    # print("ohea", K)

    max_bus = 0
    min_bus = INF
    max_bus_i = 0
    min_bus_i = 0
    for i, b in enumerate(busses):
        if b > max_bus:
            max_bus = b
            max_bus_i = i
        if b < min_bus:
            min_bus = b
            min_bus_i = i

    print("max", max_bus, max_bus_i)
    print("min", min_bus, min_bus_i)

    mb_off = sum(gaps[: max_bus_i + 1])
    offsets = [sum(gaps[: k + 2]) for k in range(len(busses) - 1)]
    print(offsets)
    print("ohea", mb_off)
    print("max_bus_i", max_bus_i)
    indexes = sorted([min_bus_i, max_bus_i])
    print(",", indexes)
    print(gaps)
    print(sum(gaps[indexes[0] : indexes[1] + 1]))
    i = arrow_alignment(
        red_len=busses[indexes[0]],
        green_len=busses[indexes[1]],
        advantage=sum(gaps[indexes[0] : indexes[1] + 1]),
    )
    # i = arrow_alignment(red_len=9, green_len=15, advantage=3)
    # ohea
    # print("lcm", lcm(offsets))
    jmp = lcm([busses[indexes[0]], busses[indexes[1]]])
    print(i, jmp)

    print("&" * 30)
    i = arrow_alignment(red_len=busses[0], green_len=busses[1], advantage=gaps[1],)
    # i = arrow_alignment(red_len=9, green_len=15, advantage=3)
    # ohea
    # print("lcm", lcm(offsets))
    jmp = lcm([busses[0], busses[1]])
    print(i, jmp)
    _, s, t = extended_gcd(busses[0], busses[1])
    z = ()

    print()

    # %jmp
    ohea
    # for o in offsets:
    #     print(">>>>", lcm([o, busses[0]]))
    print("jmp", jmp)
    assert jmp != 0

    A = sum(gaps)
    print("gap", A)
    # i = busses[0]
    # i = 1
    k = 0
    while True:
        if k % 100000 == 0:
            print(i)
            if k == 1:
                break
        ok = True
        for j, b in enumerate(busses):
            if i % b != b - sum(gaps[: j + 1]):
                ok = False
                break
        if ok:
            print("ITERS:", k)
            return i

        k += 1
        i += jmp


def part2_3():
    print(lines[1].split(","))
    busses = []
    gaps = [0]
    for b in lines[1].split(","):
        if b == "x":
            gaps[-1] += 1
            continue
        else:
            gaps.append(1)
            busses.append(int(b))

    N = reduce(lambda a, b: a * b, busses, 1)
    print(N)
    zs = []
    x = 0
    for i, b in enumerate(busses):
        y_i = N // b
        # (1/y_i) % sum(gaps[:i+1])
        z_i = extended_gcd(gaps[i - 1], gaps[i])
        print(z_i)
        x += sum(gaps[: i + 1]) * y_i * z_i
        print(x)
    return x


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part2():
    print(lines[1].split(","))
    busses = []
    indicies = []
    for i, b in enumerate(lines[1].split(",")):
        if b != "x":
            busses.append(int(b))
            indicies.append(-i)
    n = busses
    a = indicies
    print(chinese_remainder(n, a))


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 867295486378319
