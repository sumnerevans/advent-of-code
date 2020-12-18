#! /usr/bin/env python3
"""
This is a really instructive problem. A few terms:

* Tokenizer: takes a string of characters and turns it into a list of *tokens* which are
  a list (or stream) of primitive entities in the language. In our case, the things we
  care about are operators: +, *, (, and ) and operands (integers).

* Parser: takes a list (or stream) of tokens and turns it into an AST (see below).

* Evaluator: take a parsed AST and evaluate it.

An AST is an Abstract Syntax Tree. It is a tree representing the computation that
needs to be performed. I did not intially use an AST, but this is an explanation of
what it is.
If you have the following computation: 1 + (2 * 3), then the tree would look something
like this:
                         (+)
                        /   \
                      (1)   (*)
                            / \
                          (2) (3)

I originally did not use one of these, but this solution uses an AST. ASTs are much more
maintainable and it would be a lot easier to expand upon the syntax if we had an AST to
work with.

One major advantage to parsing into an AST is that we can use the same evaluation
function to evaluate both part 1 and part 2. We only need to change the parser.
"""

import sys
from typing import List, Tuple, TypeVar

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True

# Input parsing
lines: List[str] = [l.strip() for l in sys.stdin.readlines()]


def tokenize(l):
    tokens = []
    # Iterating character-by-character because the numbers are only one digit.
    for c in l:
        if c in " ":
            continue
        elif c in "()+*":
            tokens.append(c)
        else:
            tokens.append(int(c))
    return tokens


eqns = [tokenize(l) for l in lines]


def evaluate(tree):
    print("e", tree)
    if isinstance(tree, int):
        return tree
    elif tree[0] == "+":
        return evaluate(tree[1]) + evaluate(tree[2])
    elif tree[0] == "*":
        return evaluate(tree[1]) * evaluate(tree[2])


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    def parse(tokens, i, left=0):
        print("parse", tokens, i, left)
        """
        Returns a tree represented as nested tuples. For example, the above example::

            1 + (2 * 3)

        would be represented as::

            ('+', 1, ('*', 2, 3))
        """
        op = None
        while i < len(tokens):
            if isinstance(tokens[i], int):
                if op is not None:
                    return parse(tokens, i + 1, left=(op, left, tokens[i]))
                left = tokens[i]
            elif tokens[i] in "*+":
                op = tokens[i]
            elif tokens[i] == "(":
                if op is not None:
                    return (op, left, parse(tokens, i + 1))
                return parse(tokens, i + 1)
            elif tokens[i] == ")":
                return left

            i += 1

        return left

    print(parse([2, "*", "(", 4, "*", 5, ")", "+", 3], 0))
    assert parse([2, "*", "(", 4, "*", 5, ")", "+", 3], 0) == (
        "*",
        2,
        ("+", ("*", 4, 5), 3),
    )

    ans = 0

    for e in eqns:
        ans += evaluate(parse(e, 0))

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


def part2() -> int:
    ans = 0

    # (<>)

    return ans


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 472171581333710
