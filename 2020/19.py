#! /usr/bin/env python3

import functools as ft
import itertools as it
import heapq
import math
import operator
import os
import re
import sys
from copy import deepcopy
from collections import defaultdict
from enum import IntEnum
from typing import (
    Dict,
    Generator,
    Iterable,
    List,
    Match,
    Optional,
    Sized,
    Tuple,
    TypeVar,
    Union,
)

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


# Input parsing
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]

RULES = {}
strs = []
endrules = False

for line in lines:
    if line == "":
        endrules = True
        continue

    if not endrules:
        n, r = rematch(r"(\d+): (.*)", line).groups()
        ors = r.split(" | ")
        rule = []
        for x in ors:
            if '"' in x:
                rule.append(x[1])
            else:
                rule.append(tuple(map(int, x.split())))

        if isinstance(rule[0], str):
            RULES[int(n)] = rule[0]
        else:
            RULES[int(n)] = tuple(rule)
    else:
        strs.append(line)

print(RULES)

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    ans = 0

    def convert(rn) -> str:
        parts = []
        for r in RULES[rn]:
            if isinstance(r, str):
                parts.append(r)
            else:
                parts.append("".join(convert(x) for x in r))
        return "(" + "|".join(parts) + ")"

    regex = convert(0)
    for s in strs:
        if rematch(regex, s):
            ans += 1

    return ans


# ans_part1 = part1()
# print(ans_part1)

# # Store the attempts that failed here.
# tries = []
# print("Tries Part 1:", tries)
# assert ans_part1 not in tries, "Same as an incorrect answer!"


# # Regression Test
# assert test or ans_part1 == 198

########################################################################################
print("\nPart 2:")

# These are the new rules.
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31

RULES[8] = ((42,), (42, 8))
RULES[11] = ((42, 31), (42, 11, 31))


# def seq_matches(s, rns) -> Tuple[bool, int]:
#     print("seq", s, rns)
#     for rn in rns:
#         if isinstance(rn, str):
#             return s[0] == rn, 0
#         for r in rules[rn]:
#             m, i = or_matches(s, r)
#             print(m, i)


# def or_matches(s, rns) -> Tuple[bool, int]:
#     print("or", s, rns)
#     for rn in rns:
#         print(rules[rn])
#         print("ohea", rn, rules[rn])
#         m, i = seq_matches(s, rules[rn])
#         print(m, i)
#         print(rule)


def matchrule_broken(s, n, d=0):
    if len(s) == 0:
        return False, 0

    indent = " " * d
    if d == 10:
        ohea

    print(indent, "mr", s, n)
    or_rule = rules[n]
    if isinstance(or_rule, str):
        print(indent, "here", s[0], or_rule)
        return s[0] == or_rule, 1

    for seq in or_rule:
        i = 0
        works = True
        for r in seq:
            m, inc = matchrule(s[i:], r, d=d + 1)
            if not m:
                works = False
                break
            i += inc

        if works:
            print(indent, "2")
            return True, i

    print(indent, "1")
    return False, 0


def matchrule2(s: str, rn: int, d=0) -> Tuple[bool, Iterable[int]]:
    if len(s) == 0:
        return False, (0,)

    indent = " " * d
    if d == 10:
        ohea

    head, *tail = rules[rn]
    print(head, tail)

    for opt in head:
        print("oheaoheaohea")
        print(opt)
        print(matchrule(s, opt, d=d + 1))

    m, incs = matchrule(s, head, d=d + 1)
    if not m:
        return False, (0,)
    print(m, incs)

    ohea

    print(indent, "mr", s, n)
    or_rule = rules[n]
    if isinstance(or_rule, str):
        return s[0] == or_rule, (1,)

    increments = []
    anyworks = False
    for seq in or_rule:
        i = 0
        m, incs = matchrule(s[i:], seq[0], d=d + 1)
        print(m, incs)

        for inc in incs:
            m2, incs2 = matchrule(s[i + inc :], seq[1:], d=d + 1)

            # if works:
            #     print(indent, "2")
            #     increments.append(i)
            #     anyworks= True

    print(indent, "1")
    return anyworks, increments


# def matchorrule(s: str, rule_num: int, d=0) -> Tuple[bool, Iterable[int]]:
# print('mr', s, rule)
# if len(s) == 0:
#     return False, (0,)

# if isinstance(rule, str):
#     return s[0] == rule, (1,)

# increments = {0}
# for option in RULES[rule]:
#     opt_i = 0
#     while opt_i < len(option):
#         for inc in increments:
#             m, incs = matchorrule(s[inc:], option[opt_i], d=d + 1)
#         print(m, incs)
#         increments = increments.union(incs)
#         opt_i += 1

EPSILON = "EPSILON"


G = defaultdict(set)
for rn in RULES:
    for opt in RULES[rn]:
        G[(rn, "s")].add(((opt, "s"), EPSILON))

        prev = (opt, "s")
        for i, v in enumerate(opt):
            if isinstance(v, str):
                G[prev].add(((opt, "e"), v))
            else:
                G[prev].add(((v, "s"), EPSILON))
                G[(v, "e")].add(((opt, i + 1), EPSILON))
                prev = (opt, i + 1)

        G[(opt, i + 1)].add(((opt, "e"), EPSILON))
        G[(opt, "e")].add(((rn, "e"), EPSILON))

# for k, v in G.items():
#     print(k, "->", v)


def nfa_accepts(S: str):
    Q = [((0, "s"), S)]
    i = 0
    while len(Q):
        # print("START")
        # print(Q)
        current, *Q = Q
        node, lookingfor = current
        print(node, lookingfor)
        if lookingfor == "" and node == (0, "e"):
            return True

        for next_node, transition in G[node]:
            # print(next_node, transition, lookingfor)
            if transition == EPSILON:
                Q.append((next_node, lookingfor))
            else:
                if len(lookingfor) > 0 and lookingfor[0] == transition:
                    Q.append((next_node, lookingfor[1:]))

        # print(Q)

        if i > 100_000:
            return False
        i += 1

    return False


# import graphviz
# filename = "/tmp/aoc19.gv"
# g = graphviz.Digraph("G", filename=filename, format="png")
# g.attr("node", shape="circle")
# g.attr(rankdir="RL")

# for k, v in G.items():
#     for other, edgeval in v:
#         g.edge(str(k), str(other), label=edgeval)


# g.render()

# ohea


def part2() -> int:
    ans = 0

    matched = []
    for s in strs:
        # print("snothreasnotherao", matchrule(s, 0))
        print("check", s)
        if nfa_accepts(s):
            matched.append(s)
            ans += 1
            print("MATCH")
        else:
            print("NO MATCH")

    print("MATCHED")
    print("\n".join(matched))
    return ans


ans_part2 = part2()
print("=" * 100)
print(ans_part2)

# Store the attempts that failed here.
tries2 = [236]
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
# assert test or ans_part2 == (<>)
