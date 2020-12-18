#! /usr/bin/env python3
"""
This is a really instructive problem. In general, when writing an evaluator a language
(which you can consider these equations to be a language), you do it in three steps:

1. Tokenize: takes a string of characters and turns it into a list of *tokens* which are
   a list (or stream) of primitive entities in the language. In our case, the things we
   care about are operators: +, *, (, and ) and operands (integers). Another term you
   may hear for this concept is "lexing".

2. Parse: takes a list (or stream) of tokens and turns it into an AST (see below).

3. Evaluate: take a parsed AST and evaluate it.

For today, I only implemented a tokenizer and then combined the parsing with the
evaluation step by implicitly navigating the tree using recursion, blood, sweat, and
tears. In all honesty, though, this is a decent approach because there is no real need
to encode the order of operations in a tree, and the syntax is very simple.

One nice thing about the first part that makes it a bit easier to do the implicit
traversal is that there is no order of operations except for parentheses.

What is an AST?
===============

An AST is an Abstract Syntax Tree. It is a tree representing the computation that needs
to be performed. I did not use an AST, but this is an explanation of what it is.

If you have the following computation: 1 + (2 * 3), then the tree would look something
like this:
                         (+)
                        /   \
                      (1)   (*)
                            / \
                          (2) (3)

I did not use one of these to solve tonight, but if I were doing this for a real project
or job, I would use ASTs since they are much more maintainable and it would be a lot
easier to expand upon the syntax if we had an AST to work with.

One major advantage to parsing into an AST is that we can use the same evaluation
function to evaluate both part 1 and part 2. We only need to change the parser.
"""

import sys
from typing import List, Tuple

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


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def compute(tokens, i) -> Tuple[int, int]:
    """
    Parameters:
    tokens: is the list of tokens
    i: the index to start computing at

    Returns:
    A tuple of the computation result up to the next end parentheses, and the index at
    which we finished computing.
    """
    # This is a really dumb way of implicitly navigating the AST. These variables
    # basically keep track of the operation node.
    ismul = False
    isadd = False

    # This accumulates the computation at a level of the equation.
    x = 0

    while i < len(tokens):
        t = tokens[i]
        if isinstance(t, int) or t == "(":
            # If this is an open-parentheses, recursively call the compute function to
            # compute the value inside the parentheses.
            if t == "(":
                t, i = compute(tokens, i + 1)

            # Perform the necessary operation on x
            if ismul:
                # This is the case if we are in a situation like this:
                #    4 * 3
                #        ^
                #        i
                x *= t
                ismul = False
            elif isadd:
                x += t
                isadd = False
            else:
                x = t

        elif t == ")":
            return x, i
        elif t == "*":
            ismul = True
        elif t == "+":
            isadd = True

        i += 1

    return x, i


def part1() -> int:
    return sum(compute(e, 0)[0] for e in eqns)


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
        """
        Perform addition on all of the terms that need to be added and then do the
        multiplication.

        This isn't the cleanest solution, but it was effective.
        """
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
        if isinstance(t, int) or t in "+*":
            terms.append(t)
        elif t == "(":
            t, i = compute2(tokens, i + 1)
            terms.append(t)

        elif t == ")":
            return addmul(terms), i

        i += 1

    return addmul(terms), i


def part2() -> int:
    return sum(compute2(e, 0)[0] for e in eqns)


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = []
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 472171581333710
