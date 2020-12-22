#! /usr/bin/env python3

import sys
import time
from copy import deepcopy
from typing import List, Tuple

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


# Input parsing
input_start = time.time()
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]

DECKP1 = []
DECKP2 = []

p2 = False
for line in lines:
    if line.startswith("Player"):
        continue
    if line == "":
        p2 = True
        continue
    if not p2:
        DECKP1.append(int(line))
    else:
        DECKP2.append(int(line))

input_end = time.time()

# Part 1
########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    """
    I decided to use lists for this instead of a queue, because I'm really unfamiliar
    with the stdlib for queues in Python, so it is faster for me to think about lists.
    Also, using a queue in Part 2 would have been a disaster.
    """
    dp1 = deepcopy(DECKP1)
    dp2 = deepcopy(DECKP2)

    # Loop until one player has all the cards.
    tot = len(dp1) + len(dp2)
    while len(dp1) < tot and len(dp2) < tot:
        # Pull of the top of each deck. This is where having pattern matching that isn't
        # terrible would be nice. Or having a Queue in the stdlib that isn't impossible
        # to remember how to use.
        c1, *dp1r = dp1
        c2, *dp2r = dp2

        # Determine who has won, and set their decks accordingly.
        if c1 < c2:
            dp1 = dp1r
            dp2 = dp2r + [c2, c1]
        elif c2 < c1:
            dp1 = dp1r + [c1, c2]
            dp2 = dp2r

    # Reverse so that the lower indexes are associated with the cards at the bottom of
    # the deck (note we are guaranteed at this point than only one of `dp1` or `dp2` has
    # anything in it, so we can just add them together to get the winning deck).
    ans = 0
    for i, x in enumerate(reversed(dp1 + dp2)):
        ans += (i + 1) * x

    return ans


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 35397

# Part 2
########################################################################################
print("\nPart 2:")


def play_game(deck1, deck2, depth=0) -> Tuple[int, Tuple[int, ...]]:
    dp1 = tuple(deck1)
    dp2 = tuple(deck2)
    seen = set()

    tot = len(dp1) + len(dp2)
    while len(dp1) < tot and len(dp2) < tot:
        # Detect if the state has been seen before.
        if (dp1, dp2) in seen:
            return 1, dp1
        seen.add((dp1, dp2))

        c1, *dp1r = dp1
        c2, *dp2r = dp2

        # Determine how we should decide this round. If there are enough cards to play a
        # subgame, then call this function recursively. Otherwise, we just determine it
        # like normal.
        p1wins = False
        if len(dp1r) >= c1 and len(dp2r) >= c2:
            # Recursively call play_game to determine who wins the subgame.
            p1wins = play_game(dp1r[:c1], dp2r[:c2], depth + 1)[0] == 1
        else:
            p1wins = c1 > c2

        if p1wins:
            dp1 = tuple(dp1r) + (c1, c2)
            dp2 = tuple(dp2r)
        else:
            dp1 = tuple(dp1r)
            dp2 = tuple(dp2r) + (c2, c1)

    if len(dp1) > 0:
        return 1, dp1
    else:
        return 2, dp2


def part2() -> int:
    _, winnerdeck = play_game(DECKP1, DECKP2)

    ans = 0
    for i, x in enumerate(reversed(winnerdeck)):
        ans += (i + 1) * x
    return ans


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = [30976, 36271]
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 31120

if debug:
    input_parsing = input_end - input_start
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + part1_time + part2_time) * 1000}ms")
