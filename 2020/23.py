#! /usr/bin/env python3

import sys
import time
from copy import deepcopy
from typing import List

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


# Input parsing
input_start = time.time()
with open("inputs/23.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]

CUPS = [int(x) for x in lines[0]]
MIN_CUP, MAX_CUP = min(CUPS), max(CUPS)

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

# (<>)

shared_end = time.time()

# Part 1
########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    ITERS = 10 if test else 100

    cups = deepcopy(CUPS)

    for _ in range(ITERS):
        # Get the current cup, pick up the next three, and leave the rest.
        current = cups[0]
        picked = cups[1:4]
        cups = cups[4:]

        # Calculate the destination. Wrap-around if it gets less than the min cup label.
        destination = current - 1
        if destination < MIN_CUP:
            destination = MAX_CUP
        while destination in picked:  # the destination cannot be in the picked IDs
            destination -= 1
            if destination < MIN_CUP:
                destination = MAX_CUP

        # Find the destination index and the it splits the cups list at that index, and
        # then inserts the picked part of the list in-between, and then appends current
        # to the end (this is so the element *after* current is the one that gets chosen
        # as the current on the next round).
        idx = cups.index(destination)
        cups = cups[: idx + 1] + picked + cups[idx + 1 :] + [current]

    # Wrap-around to get the 1 at the front of the list.
    while cups[0] != 1:
        cups = cups[1:] + [cups[0]]

    # Calculate the number representing the order. Exclude the 1.
    num_str = "".join(map(str, cups[1:]))
    return int(num_str)


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 82573496

# Part 2
########################################################################################
print("\nPart 2:")


def part2():
    """
    The first key insight is that there are three operations for each iteration that all
    need to be constant time.

    1. Remove the three elements to the right of current.
    2. Finding the destination element.
    3. Inserting the three picked elements once the destination is found.

    At first I attempted to implement all of this using a dequeue (double-ended queue)
    because it can do both (1) and (3) in O(1) time. However, this doesn't work because,
    (2) is still O(n), which isn't good enough.

    The second key insight is that the three above properties can be achieved via a
    linked list, *if you can find implement a way to find the destination element in
    constant time*. This can be accomplished if you have a mapping of label to node.

    My solution uses an implicit linked-list (implemented using a dictionary) that
    allows me to accomplish the same thing conceptually, without an explicit extra
    mapping.
    """
    MAX_2 = 1_000_000
    cups = deepcopy(CUPS) + [i for i in range(MAX_CUP + 1, MAX_2 + 1)]

    # Initialize the "linked list" with the initial "pointers" from each cup to the next
    # one.
    linked_list = {}  # cup_label -> cup_label
    for x, y in zip(cups, cups[1:]):
        linked_list[x] = y
    linked_list[cups[-1]] = cups[0]  # wrap-around from the end to the beginning

    # The current cup is whatever is at the head of the cups linked list.
    current = cups[0]

    for i in range(10_000_000):
        if debug and i % 10_000 == 0:
            print(i)

        # Because each node of the linked list is in the dictionary, we can actually
        # find the element within the linked list by just looking it up in the
        # dictionary.

        # Here, we get the element that the current element points to.
        # For example, here let's say our linked list looks like this:
        #   1 -> 5 -> 6 -> 7 -> 9 -> 4 -> 8 -> 2 -> 3
        # If "current" is 5, then
        picked1 = linked_list[current]  # will give 6
        picked2 = linked_list[picked1]  # thus this will give 7
        picked3 = linked_list[picked2]  # and this will give 9
        first_not_picked = linked_list[picked3]  # and this will give 4
        picked = (picked1, picked2, picked3)

        # First, remove the next 3 by bypassing them with a pointer change
        linked_list[current] = first_not_picked
        #   1 -> 5 -.  6 -> 7 -> 9 -> 4 -> 8 -> 2 -> 3
        #           |                 ^
        #           '-----------------'

        # Compute the destination node (same logic as part 1)
        destination = current - 1
        if destination < MIN_CUP:
            destination = MAX_2
        while destination in picked:
            destination -= 1
            if destination < MIN_CUP:
                destination = MAX_2

        # Find the element after the destination. In the example case, the destination
        # is going to be 4. We need to splice in the picked elements back into the list
        # right after the destination. The first step is to point the end of the picked
        # list at the node that the destination points to.
        linked_list[picked3] = linked_list[destination]
        #   1 -> 5 -.  6 -> 7 -> 9 -.  4 -> 8 -> 2 -> 3
        #           |               |  ^    ^
        #           '---------------+--'    |
        #                           '-------'

        # The next step in spiciling in the list is to point the destination at the
        # beginning of the picked list.
        linked_list[destination] = picked1
        #   1 -> 5 -.  6 -> 7 -> 9 -.  4 -.  8 -> 2 -> 3
        #           |  ^            |  ^  |  ^
        #           |  |            |  |  |  |
        #           '--+------------+--'  |  |
        #              |            '-----+--'
        #              '------------------'

        # If we unravel this, then we get:
        #   1 -> 5 -> 4 -> 6 -> 7 -> 9 -> 8 -> 2 -> 3

        # Finally, all we do is set the new current node to the node that is directly to
        # the right of the current node. It is guaranteed that this will be the first
        # node that wasn't spliced out.
        current = first_not_picked

    print(linked_list[1], linked_list[linked_list[1]])
    return linked_list[1] * linked_list[linked_list[1]]


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = [188944417922, 149245887792]
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 11498506800

if debug:
    input_parsing = input_end - input_start
    shared = shared_end - shared_start
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Shared: {shared * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + shared + part1_time + part2_time) * 1000}ms")
