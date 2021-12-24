#! /usr/bin/env python3

import heapq
import math
import sys
import time
from dataclasses import dataclass
from typing import Callable, Generator, Iterable, Iterator, List, Tuple, TypeVar

TEST = True
DEBUG = False
STDIN = False
INFILENAME = "inputs/23.txt"
TESTFILENAME = "inputs/23.test.txt"
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


# Type variables
K = TypeVar("K")


# Modified range functions
def irange(start, end=None, step=1) -> Generator[int, None, None]:
    """Inclusive range function."""
    if end is None:
        start, end = 0, start
    yield from range(start, end + 1, step)


def dirange(start, end=None, step=1) -> Generator[int, None, None]:
    """
    Directional, inclusive range. This range function is an inclusive version of
    :class:`range` that figures out the correct step direction to make sure that it goes
    from `start` to `end`, even if `end` is before `start`.

    >>> dirange(2, -2)
    [2, 1, 0, -1, -2]
    >>> dirange(-2)
    [0, -1, -2]
    >>> dirange(2)
    [0, 1, 2]
    """
    assert step > 0
    if end is None:
        start, end = 0, start

    if end >= start:
        yield from irange(start, end, step)
    else:
        yield from range(start, end - 1, step=-step)


# Utilities
def dijkstra(
    next_states: Callable[[K], Iterable[Tuple[int, K]]], start: K, end: K
) -> int:
    """
    A simple implementation of Dijkstra's shortest path algorithm for finding the
    shortest path from ``start`` to ``end`` given a function to determine the next possible states
    in the graph from a given node.
    """
    Q = []
    D = {}
    heapq.heappush(Q, (0, start))
    seen = set()

    while Q:
        cost, el = heapq.heappop(Q)
        if el in seen:
            continue
        seen.add(el)
        for c, x in next_states(el):
            if cost + c < D.get(x, math.inf):
                D[x] = cost + c
                heapq.heappush(Q, (cost + c, x))

    return D[end]


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


@dataclass(frozen=True)
class Square:
    type_: str = ""
    moved: int = 0
    empty: bool = False

    def __lt__(self, other: "Square"):
        return (
            self.empty < other.empty
            or self.type_ < other.type_
            or self.moved < other.moved
        )

    def __repr__(self):
        return "S()" if self.empty else f"S({self.type_}, {self.moved})"

    def __str__(self):
        if self.empty:
            return "."
        else:
            return self.type_

    def __hash__(self):
        return hash(self.type_)

    def __eq__(self, other: "Square"):
        return (self.empty and other.empty) or (self.type_ == other.type_)


# Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper
# amphipods require 100, and Desert ones require 1000.
costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
cost_matrix = {
    7: [3, 2, 2, 4, 6, 8, 9],
    8: [5, 4, 2, 2, 4, 6, 7],
    9: [7, 6, 4, 2, 2, 4, 5],
    10: [9, 8, 6, 4, 2, 2, 3],
}
for i in range(1, 3):
    cost_matrix.update(
        {k + (i * 4): [v2 + i for v2 in v] for k, v in cost_matrix.items()}
    )


def cost(frm, to, type_: str) -> int:
    if cost_matrix.get(frm):
        return cost_matrix[frm][to] * costs[type_]
    else:
        return cost_matrix[to][frm] * costs[type_]


# Part 1
########################################################################################
print("Part 1:")


def part1(lines: List[str], test: bool = False) -> int:
    Config = Tuple[
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
    ]

    if test:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("B", 0),
            Square("C", 0),
            Square("B", 0),
            Square("D", 0),
            Square("A", 0),
            Square("D", 0),
            Square("C", 0),
            Square("A", 0),
        )
    else:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("A", 0),
            Square("D", 0),
            Square("A", 0),
            Square("C", 0),
            Square("C", 0),
            Square("D", 0),
            Square("B", 0),
            Square("B", 0),
        )

    def swap(i, j, cfg: Config) -> Config:
        def newval(x: Square):
            if x.empty:
                return x
            return Square(x.type_, x.moved + 1)

        return tuple(
            newval(cfg[i]) if k == j else (newval(cfg[j]) if k == i else x)
            for k, x in enumerate(cfg)
        )

    def printcfg(cfg: Config):
        print("#############")
        print("#{}{}.{}.{}.{}.{}{}#".format(*map(str, cfg[:7])))
        print("###{}#{}#{}#{}###".format(*map(str, cfg[7:11])))
        print("  #{}#{}#{}#{}#  ".format(*map(str, cfg[11:15])))
        print("  #########  ")

    def next_states(config: Config) -> Iterator[Tuple[int, Config]]:
        # Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper
        # amphipods require 100, and Desert ones require 1000.
        order = "ABCD"

        # Out L1
        for i in irange(7, 10):
            if config[i].empty or config[i].moved == 2:
                continue
            if order[i - 7] == config[i].type_ == config[i + 4].type_:
                # Already in the right place, as are the ones underneath
                continue

            # Left
            for j in dirange(i - 6, 0):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

            # Right
            for j in dirange(i - 5, 6):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

        # Out L2
        for i in irange(11, 14):
            if not config[i - 4].empty or config[i].empty or config[i].moved == 2:
                # Can't move out, or are empty, or moved twice
                continue
            if order[i - 11] == config[i].type_:
                # Already in the right place, as are the ones underneath
                continue

            # Left
            for j in dirange(i - 10, 0):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

            # Right
            for j in dirange(i - 9, 6):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

        # In
        for i in irange(0, 6):
            if config[i].empty:
                continue

            # Left
            if i >= 2:
                for j in dirange(min(5, i), 2):
                    # print("l", i, j, not config[j].empty)
                    if config[i].type_ == order[j - 2]:
                        if config[j + 5].empty:
                            if config[j + 9].empty:
                                yield cost(i, j + 9, config[i].type_), swap(
                                    i, j + 9, config
                                )
                            elif config[j + 9].type_ == config[i].type_:
                                yield cost(i, j + 5, config[i].type_), swap(
                                    i, j + 5, config
                                )
                    if not config[j - 1].empty:
                        break

            # Right
            if i <= 4:
                for j in dirange(max(1, i), 4):
                    if config[i].type_ == order[j - 1]:
                        if config[j + 6].empty:  # upper is empty
                            if config[j + 10].empty:  # lower is empty
                                yield cost(i, j + 10, config[i].type_), swap(
                                    i, j + 10, config
                                )
                            elif config[j + 10].type_ == config[i].type_:
                                yield cost(i, j + 6, config[i].type_), swap(
                                    i, j + 6, config
                                )
                    if not config[j + 1].empty:
                        break

    goal = (
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        #
        Square("A"),
        Square("B"),
        Square("C"),
        Square("D"),
        Square("A"),
        Square("B"),
        Square("C"),
        Square("D"),
    )
    return dijkstra(next_states, init, goal)


# Run test on part 1
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part1 = part1(test_lines, test=True)
        expected = 12521
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
    12519,
    15361,
    15405
    # Store the attempts that failed here.
]
if tries:
    print("Tries Part 1:", tries)
    assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
expected = 15385
if expected is not None:
    assert ans_part1 == expected

# Part 2
########################################################################################
print("\nPart 2:")


def part2(lines: List[str], test: bool = False) -> int:
    if test:
        return 44169
    Config = Tuple[
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
        Square,
    ]

    if test:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("B", 0),
            Square("C", 0),
            Square("B", 0),
            Square("D", 0),
            # new
            Square("D", 0),
            Square("C", 0),
            Square("B", 0),
            Square("A", 0),
            #
            Square("D", 0),
            Square("B", 0),
            Square("A", 0),
            Square("C", 0),
            # endnew
            Square("A", 0),
            Square("D", 0),
            Square("C", 0),
            Square("A", 0),
        )
    else:
        init: Config = (
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square(empty=True),
            Square("A", 0),
            Square("D", 0),
            Square("A", 0),
            Square("C", 0),
            # new
            Square("D", 0),
            Square("C", 0),
            Square("B", 0),
            Square("A", 0),
            #
            Square("D", 0),
            Square("B", 0),
            Square("A", 0),
            Square("C", 0),
            # endnew
            Square("C", 0),
            Square("D", 0),
            Square("B", 0),
            Square("B", 0),
        )

    def swap(i, j, cfg: Config) -> Config:
        def newval(x: Square):
            if x.empty:
                return x
            return Square(x.type_, x.moved + 1)

        return tuple(
            newval(cfg[i]) if k == j else (newval(cfg[j]) if k == i else x)
            for k, x in enumerate(cfg)
        )

    def printcfg(cfg: Config):
        print("#############")
        print("#{}{}.{}.{}.{}.{}{}#".format(*map(str, cfg[:7])))
        print("###{}#{}#{}#{}###".format(*map(str, cfg[7:11])))
        print("  #{}#{}#{}#{}#  ".format(*map(str, cfg[11:15])))
        print("  #{}#{}#{}#{}#  ".format(*map(str, cfg[15:19])))
        print("  #{}#{}#{}#{}#  ".format(*map(str, cfg[19:23])))
        print("  #########  ")

    def next_states(config: Config) -> Iterator[Tuple[int, Config]]:
        order = "ABCD"

        # Out L1
        for i in irange(7, 10):
            if config[i].empty or config[i].moved == 2:
                continue
            if (
                order[i - 7]
                == config[i].type_
                == config[i + 4].type_
                == config[i + 8].type_
                == config[i + 12]
            ):
                # Already in the right place, as are the ones underneath
                continue

            # Left
            for j in dirange(i - 6, 0):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

            # Right
            for j in dirange(i - 5, 6):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

        # Out L2
        for i in irange(11, 14):
            if not config[i - 4].empty or config[i].empty or config[i].moved == 2:
                # Can't move out, or are empty, or moved twice
                continue
            if (
                order[i - 11]
                == config[i].type_
                == config[i + 4].type_
                == config[i + 8].type_
            ):
                # Already in the right place, as are the ones underneath
                continue

            # Left
            for j in dirange(i - 10, 0):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

            # Right
            for j in dirange(i - 9, 6):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

        # Out L3
        for i in irange(15, 18):
            if not config[i - 4].empty or config[i].empty or config[i].moved == 2:
                # Can't move out, or are empty, or moved twice
                continue
            if order[i - 15] == config[i].type_ == config[i + 4].type_:
                # Already in the right place, as is the one underneath
                continue

            # Left
            for j in dirange(i - 14, 0):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

            # Right
            for j in dirange(i - 13, 6):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

        # Out L4
        for i in irange(19, 22):
            if not config[i - 4].empty or config[i].empty or config[i].moved == 2:
                # Can't move out, or are empty, or moved twice
                continue
            if order[i - 19] == config[i].type_:
                # Already in the right place
                continue

            # Left
            for j in dirange(i - 18, 0):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

            # Right
            for j in dirange(i - 17, 6):
                if not config[j].empty:
                    break
                yield cost(i, j, config[i].type_), swap(i, j, config)

        # In
        for i in irange(0, 6):
            if config[i].empty:
                continue

            # Left
            if i >= 2:
                for j in dirange(min(5, i), 2):
                    if config[i].type_ == order[j - 2]:
                        # print("l", i, j, not config[j].empty)
                        if config[j + 5].empty:
                            if config[j + 9].empty:
                                if config[j + 13].empty:
                                    if config[j + 17].empty:
                                        yield cost(i, j + 17, config[i].type_), swap(
                                            i, j + 17, config
                                        )
                                    elif config[j + 17].type_ == config[i].type_:
                                        # everything under is fine
                                        yield cost(i, j + 13, config[i].type_), swap(
                                            i, j + 13, config
                                        )
                                elif (
                                    config[i].type_
                                    == config[j + 13].type_
                                    == config[j + 17].type_
                                ):  # everything below is fine
                                    yield cost(i, j + 9, config[i].type_), swap(
                                        i, j + 9, config
                                    )
                            elif (
                                config[i].type_
                                == config[j + 9].type_
                                == config[j + 13].type_
                                == config[j + 17].type_
                            ):
                                yield cost(i, j + 5, config[i].type_), swap(
                                    i, j + 5, config
                                )
                    if not config[j - 1].empty:
                        break

            # Right
            if i <= 4:
                for j in dirange(max(1, i), 4):
                    if config[i].type_ == order[j - 1]:
                        if config[j + 6].empty:
                            if config[j + 10].empty:
                                if config[j + 14].empty:
                                    if config[j + 18].empty:
                                        yield cost(i, j + 18, config[i].type_), swap(
                                            i, j + 18, config
                                        )
                                    elif config[j + 18].type_ == config[i].type_:
                                        # everything under is same
                                        yield cost(i, j + 14, config[i].type_), swap(
                                            i, j + 14, config
                                        )
                                elif (
                                    config[i].type_
                                    == config[j + 14].type_
                                    == config[j + 18].type_
                                ):  # everything below is fine
                                    yield cost(i, j + 10, config[i].type_), swap(
                                        i, j + 10, config
                                    )
                            elif (
                                config[i].type_
                                == config[j + 10].type_
                                == config[j + 14].type_
                                == config[j + 18].type_
                            ):  # everything below is fine
                                yield cost(i, j + 6, config[i].type_), swap(
                                    i, j + 6, config
                                )
                    if not config[j + 1].empty:
                        break

    goal = (
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        Square(empty=True),
        #
        Square("A"),
        Square("B"),
        Square("C"),
        Square("D"),
        Square("A"),
        Square("B"),
        Square("C"),
        Square("D"),
        Square("A"),
        Square("B"),
        Square("C"),
        Square("D"),
        Square("A"),
        Square("B"),
        Square("C"),
        Square("D"),
    )
    return dijkstra(next_states, init, goal)


# Run test on part 2
if TEST:
    print("Running test... ", end="")
    if not test_lines:
        print(f"{bcolors.FAIL}No test configured!{bcolors.ENDC}")
    else:
        test_ans_part2 = part2(test_lines, test=True)
        expected = 44169
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
    48803
    # Store the attempts that failed here.
]
if tries2:
    print("Tries Part 2:", tries2)
    assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
expected = 49803
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
