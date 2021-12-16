#! /usr/bin/env python3

import functools as ft
import operator
import sys
import time
from typing import Iterable, List, Tuple, Union

test = True
debug = False
stdin = False
INFILENAME = "inputs/16.txt"
TESTFILENAME = "inputs/16.test.txt"
for arg in sys.argv:
    if arg == "--notest":
        test = False
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


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
def bitstrtoint(s: Union[str, List[int], List[str], List[bool]]) -> int:
    if isinstance(s, list):
        if isinstance(s[0], bool):
            s = list(map(int, s))

        s = "".join(map(str, s))
    return int(s, 2)


def pbits(num: int, pad: int = 32) -> str:
    """Return the bits of `num` in binary with the given padding."""
    return bin(num)[2:].zfill(pad)


def prod(it: Iterable):
    return ft.reduce(operator.mul, it, 1)


print(f"\n{'=' * 30}\n")

# Read the input
if stdin:
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


def parse_packet(
    bits: List[int], packets_to_process: int = 2 ** 200
) -> Tuple[int, int, List[int]]:
    version_sum = 0
    bit_pointer = 0
    packets_processed = 0

    version = None
    type_ = None

    values = []

    while (
        bit_pointer < len(bits)
        and packets_processed < packets_to_process
        and any(bits[bit_pointer:])
    ):
        if version is None:
            version = bitstrtoint(bits[bit_pointer : bit_pointer + 3])
            version_sum += version
            bit_pointer += 3
        elif type_ is None:
            type_ = bitstrtoint((bits[bit_pointer : bit_pointer + 3]))
            bit_pointer += 3
        else:
            # We have parsed the version and type, move on to parse the packet based on
            # the rules.
            if type_ == 4:
                # This is a literal. You have to parse chunks of 5 bits until you get a
                # chunk with a 0 in the leftmost position, then you should stop
                # iterating. Then combine all of the 4-bit chunks together to get the
                # actual number.
                int_bits = []
                more = True
                while more:
                    more = bits[bit_pointer]
                    int_bits.extend(bits[bit_pointer + 1 : bit_pointer + 5])
                    bit_pointer += 5

                values.append(bitstrtoint(int_bits))
                version = None
                type_ = None
                packets_processed += 1
            else:
                # This is an operator. We need to parse out how large the subpacket is.
                length_type_id = bits[bit_pointer]
                if length_type_id == 0:
                    # The next 15 bits tell us how many bits are in the subpackets.
                    bits_in_subpackets = bitstrtoint(
                        bits[bit_pointer + 1 : bit_pointer + 16]
                    )
                    bit_pointer += 16
                    _, vs, rec_values = parse_packet(
                        bits[bit_pointer : bit_pointer + bits_in_subpackets]
                    )
                    bit_pointer += bits_in_subpackets
                else:
                    # The next 11 bits tell us how many subpackets there are.
                    subpackets = bitstrtoint(bits[bit_pointer + 1 : bit_pointer + 12])
                    bit_pointer += 12
                    inc, vs, rec_values = parse_packet(bits[bit_pointer:], subpackets)
                    bit_pointer += inc
                version_sum += vs

                values.append(
                    {
                        0: sum,
                        1: prod,
                        2: min,
                        3: max,
                        5: lambda rv: int(rv[0] > rv[1]),
                        6: lambda rv: int(rv[0] < rv[1]),
                        7: lambda rv: int(rv[0] == rv[1]),
                    }[type_](rec_values)
                )

                version = None
                type_ = None
                packets_processed += 1

    return bit_pointer, version_sum, values


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str]) -> int:
    bits = []
    for c in lines[0]:
        bits.extend(map(int, pbits(int(c, 16), 4)))

    _, version_sum, _ = parse_packet(bits)
    return version_sum


# Run test on part 1
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines)
        expected = 13
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

tries = [653, 142, 683]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 843
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str]) -> int:
    bits = []
    for c in lines[0]:
        bits.extend(map(int, pbits(int(c, 16), 4)))

    _, _, values = parse_packet(bits)
    assert len(values) == 1
    return values[0]


# Run test on part 2
if test:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines)
        expected = 1
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
    5390823646050
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 5390807940351
if expected is not None:
    assert ans_part2 == expected

if debug:
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(part1_time + part2_time) * 1000}ms")
