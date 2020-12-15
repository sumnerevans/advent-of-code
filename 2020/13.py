#! /usr/bin/env python3

import math
import sys

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Constants
INF = float("inf")

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

    c = s
    while True:
        for b in busses:
            if c % b == 0:
                return b * (c - s)
        c += 1


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
    """
    This was my first attempt. It is a brute-force algorithm, which clearly doesn't work
    because the input is to big. It does solve the samples, though.
    """
    busses = []
    gaps = [0]
    for b in lines[1].split(","):
        if b == "x":
            gaps[-1] += 1
            continue
        else:
            gaps.append(1)
            busses.append(int(b))

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
    """
    I don't claim any copyright on this. I copied it from the internet somewhere.

    Extended Greatest Common Divisor Algorithm.

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
    """
    I don't claim any copyright on this. I copied it from the internet somewhere.

    Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, _ = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def arrow_alignment(red_len, green_len, advantage):
    # I don't claim any copyright on this. I copied it from the internet somewhere.
    print("aa", "r:", red_len, "g:", green_len, "a:", advantage)
    """Where the arrows first align, where green starts shifted by advantage"""
    period, phase = combine_phased_rotations(
        red_len, 0, green_len, -advantage % green_len
    )
    return -phase % period


def part2_2():
    """
    This was my second attempt. It's slightly more intelligent as it uses the smallest
    and largest bus IDs to calculate a larger step.

    This would have worked if I also had the additional insight that I needed to then
    use that to bootstrap finding how each subsequent bus lines up by iterating until I
    got to a point where another bus lined up and then use that as a step.
    """
    busses = []
    gaps = [0]
    for b in lines[1].split(","):
        if b == "x":
            gaps[-1] += 1
            continue
        else:
            gaps.append(1)
            busses.append(int(b))

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

    indexes = sorted([min_bus_i, max_bus_i])
    i = arrow_alignment(
        red_len=busses[indexes[0]],
        green_len=busses[indexes[1]],
        advantage=sum(gaps[indexes[0] : indexes[1] + 1]),
    )
    jmp = lcm([busses[indexes[0]], busses[indexes[1]]])
    i = arrow_alignment(red_len=busses[0], green_len=busses[1], advantage=gaps[1],)
    jmp = lcm([busses[0], busses[1]])

    assert jmp != 0

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
    """
    Third attempt. This one I tried to implement the Chinese Remainder Theorem by hand.
    I failed.
    """
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
    """
    I claim no copyright on this function. I copied it from the internet.
    """
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    """
    I claim no copyright on this function. I copied it from the internet.
    """
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
    """
    Final attempt at part 2. At this point I had struggled through enough that I
    understood what I needed to do with the Chinese Remainder Theorem. I copied an
    implementation of it (above) and then just created the necessary arrays for it.

    One key is the ``indicies.append(-i)`` line. It needs to be negative because index
    in question happens ``i`` before the period of ``b``.
    """
    busses = []
    indicies = []
    for i, b in enumerate(lines[1].split(",")):
        if b != "x":
            busses.append(int(b))
            indicies.append(-i)
    n = busses
    a = indicies
    return chinese_remainder(n, a)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 867295486378319
