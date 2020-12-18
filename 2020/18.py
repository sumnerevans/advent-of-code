#! /usr/bin/env python3

import sys
from typing import List, TypeVar

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Type variables
K = TypeVar("K")


# Input parsing
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]


def tokenize(l):
    tokens = []
    for c in l:
        if c in " ":
            continue
        elif c in "()+*":
            tokens.append(c)
        else:
            tokens.append(int(c))
    return tokens


eqns = [tokenize(l) for l in lines]


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def compute(tokens, i):
    ismul = False
    isadd = False

    x = None

    while i < len(tokens):
        t = tokens[i]
        if isinstance(t, int):
            if ismul:
                x *= t
                ismul = False
            elif isadd:
                x += t
                isadd = False
            else:
                x = t
        elif t == "(":
            y, i = compute(tokens, i + 1)
            if ismul:
                x *= y
                ismul = False
            elif isadd:
                x += y
                isadd = False
            else:
                x = y

        elif t == ")":
            return x, i
        elif t == "*":
            ismul = True
        elif t == "+":
            isadd = True

        i += 1

    return x, i


def part1() -> int:
    ans = 0

    for e in eqns:
        ans += compute(e, 0)[0]

    return ans


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 9535936849815

########################################################################################
print("\nPart 2:")


def compute2(tokens, i):
    def addmul(terms):
        while len(terms) > 1:
            if any(t == "+" for t in terms):
                for i in range(len(terms)):
                    if terms[i] == "+":
                        new = terms[i - 1] + terms[i + 1]
                        terms = terms[: i - 1] + [new] + terms[i + 2 :]
                        break
            else:
                for i in range(len(terms)):
                    if terms[i] == "*":
                        new = terms[i - 1] * terms[i + 1]
                        terms = terms[: i - 1] + [new] + terms[i + 2 :]
                        break
                else:
                    break
        return terms[0]

    terms = []
    while i < len(tokens):
        t = tokens[i]
        if isinstance(t, int):
            terms.append(t)
        elif t == "(":
            t, i = compute2(tokens, i + 1)
            terms.append(t)

        elif t == ")":
            return addmul(terms), i
        elif t in "+*":
            terms.append(t)

        i += 1

    return addmul(terms), i


def part2() -> int:
    ans = 0
    for e in eqns:
        ans += compute2(e, 0)[0]

    return ans


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 472171581333710
