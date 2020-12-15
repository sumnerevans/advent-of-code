#! /usr/bin/env python3

import copy
import sys

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Constants
COMPASS_GRID_DIRS = [  # Tuples of (delta_row, delta_col)
    (-1, 0),  # above
    (1, 0),  # below
    (0, -1),  # left
    (0, 1),  # right
]
DIAG_GRID_DIRS = [  # Tuples of (delta_row, delta_col)
    (-1, -1),  # top-left
    (-1, 1),  # top-right
    (1, -1),  # bottom-left
    (1, 1),  # bottom-right
]
GRID_DIRS = COMPASS_GRID_DIRS + DIAG_GRID_DIRS


# Utilities
def grid_adjs(row, col, max_row, max_col, dirs=GRID_DIRS):
    # Iterate through all of the directions and return all of the (row, col) tuples
    # representing the adjacent cells.
    for dy, dx in dirs:
        if 0 <= row + dy < max_row and 0 <= col + dx < max_col:
            yield row + dy, col + dx


# Input parsing
lines = [[x for x in l.strip()] for l in sys.stdin.readlines()]
C = len(lines[0])
R = len(lines)

########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1():
    prev = copy.deepcopy(lines)
    while True:
        new = copy.deepcopy(prev)
        for r in range(len(lines)):
            for c in range(len(lines[0])):
                if prev[r][c] in "L#":
                    # This cell is a seat that is either occupied or not.
                    # Count the number of occupied adjacent seats.
                    num_o = 0
                    for a_r, a_c in grid_adjs(r, c, R, C):
                        if prev[a_r][a_c] == "#":
                            num_o += 1

                    if num_o == 0:
                        # Nobody in adjacent seats, occupy.
                        new[r][c] = "#"
                    if num_o >= 4:
                        # 4+ occupied adjacent seats. LEAVE!
                        new[r][c] = "L"

        # Check to see if everything is equal. If it is, then we are at steady state.
        if prev == new:
            # Return the count of all of the occupied seats (marked with '#')
            return "".join("".join(p) for p in prev).count("#")

        prev = new


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 2424

########################################################################################
print("\nPart 2:")


def rays(r, c):
    def step(dy, dx):
        # Step once to make sure you don't return the current cell.
        a = r + dy
        b = c + dx
        while a >= 0 and b >= 0 and a < R and b < C:
            yield a, b
            a += dy
            b += dx

    # yield from == JavaScript yield*
    # This yields all of the elements of the generator individually.
    yield from (step(dy, dx) for (dy, dx) in GRID_DIRS)


def part2():
    prev = copy.deepcopy(lines)
    while True:
        new = copy.deepcopy(prev)
        for r in range(len(lines)):
            for c in range(len(lines[0])):
                if prev[r][c] in "L#":
                    num_o = 0
                    for ray in rays(r, c):
                        for r_r, r_c in ray:
                            if prev[r_r][r_c] in "L#":
                                if prev[r_r][r_c] == "#":
                                    num_o += 1
                                break

                    if num_o == 0:
                        new[r][c] = "#"
                    if num_o >= 5:
                        new[r][c] = "L"

        # Check to see if everything is equal. If it is, then we are at steady state.
        if prev == new:
            return "".join("".join(p) for p in prev).count("#")

        prev = new


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 2208
