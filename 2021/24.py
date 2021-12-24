#! /usr/bin/env python3

import re
import sys
import time
import z3
from typing import List, Match, Optional, Tuple

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "inputs/24.txt"
TESTFILENAME = "inputs/24.test.txt"
for arg in sys.argv:
    if arg == "--notest":
        TEST = False
    if arg == "--debug":
        DEBUG = True
    if arg == "--stdin":
        STDIN = True


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Utilities
def rematch(pattern: str, s: str) -> Optional[Match]:
    return re.fullmatch(pattern, s)


print(f"\n{'=' * 30}\n")

# Read the input
if STDIN:
    input_lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        input_lines: List[str] = [l.strip() for l in f.readlines()]

# Try and read in the test file.
try:
    with open(TESTFILENAME) as f:
        test_lines: List[str] = [l.strip() for l in f.readlines()]
except Exception:
    test_lines = []


# Shared
########################################################################################
def islit(s: str) -> bool:
    if not isinstance(s, str):
        return False
    return rematch(r"[\d-]+", s) is not None


def get_solver(lines: List[str]) -> Tuple[z3.Optimize, List]:
    solver = z3.Optimize()

    curstate = [z3.Int(f"{a}0") for a in "wxyz"]
    solver.add(*(x == 0 for x in curstate))
    cur_nums = [0, 0, 0, 0]

    digit_num = 1
    digit_ints = []
    instrs = [tuple(line.split()) for line in lines]
    for instr in instrs:
        dst_idx = "wxyz".index(instr[1])
        cur_nums[dst_idx] += 1
        new_sym = z3.Int(instr[1] + str(cur_nums[dst_idx]))

        if instr[0] == "inp":
            curstate[dst_idx] = new_sym
            new_digit = z3.Int(f"d{digit_num}")
            solver.add(new_digit == new_sym)
            solver.add(z3.And(1 <= new_digit, new_digit <= 9))
            digit_ints.append(new_digit)
            digit_num += 1
        else:
            if islit(instr[2]):
                src = int(instr[2])
            else:
                src_idx = "wxyz".index(instr[2])
                src = curstate[src_idx]

            if instr[0] == "add":
                solver.add(new_sym == curstate[dst_idx] + src)
            elif instr[0] == "mul":
                solver.add(new_sym == curstate[dst_idx] * src)
            elif instr[0] == "div":
                solver.add(new_sym == curstate[dst_idx] / src)
            elif instr[0] == "mod":
                solver.add(new_sym == curstate[dst_idx] % src)
            elif instr[0] == "eql":
                solver.add(z3.Implies(curstate[dst_idx] == src, new_sym == 1))
                solver.add(z3.Implies(curstate[dst_idx] != src, new_sym == 0))
            else:
                assert False

            curstate[dst_idx] = new_sym

    solver.add(curstate[3] == 0)
    return solver, digit_ints


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    solver, digit_ints = get_solver(lines)
    solver.maximize(z3.Sum(digit_ints))
    assert solver.check()
    model = solver.model()
    optimal = []
    for x in digit_ints:
        optimal.append(model[x])
    return int("".join(map(str, optimal)))


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 84
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part1 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part1} != {expected}{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part1)
        print()

part1_start = time.time()
print("Running input...")
ans_part1 = part1(input_lines)
part1_end = time.time()
print("Result:", ans_part1)

tries = [
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 59996912981939
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    solver, digit_ints = get_solver(lines)
    solver.minimize(z3.Sum(digit_ints))
    assert solver.check()
    model = solver.model()
    optimal = []
    for x in digit_ints:
        optimal.append(model[x])
    return int("".join(map(str, optimal)))


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 21
        if expected is None:
            print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
        elif test_ans_part2 == expected:
            print(f"{bcolors.OKGREEN}PASS{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}FAIL{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Result: {test_ans_part2} != {expected}{bcolors.ENDC}")
            assert False

        print("Result:", test_ans_part2)
        print()

part2_start = time.time()
print("Running input...")
ans_part2 = part2(input_lines)
part2_end = time.time()
print("Result:", ans_part2)

tries2 = [
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 17241911811915
if expected is not None:
    assert ans_part2 == expected

if DEBUG:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
