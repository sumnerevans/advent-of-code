#! /usr/bin/env python3

import re
import sys
from typing import List, Match, Optional

test = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--test":
        test = True


# Utilities
def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


# Input parsing
with open("inputs/19.txt") as f:
    lines: List[str] = [l.strip() for l in f.readlines()]


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


########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> int:
    """
    This is the grossest way to solve this, but I think it's one of the best ways
    because of the nice properties of the input.

    Basically, I'm constructing a regular expression from the grammar (which luckily
    already is regular for Part 1).

    I originally tried to do this intelligently with another recursive descent parser,
    but that failed miserably. I finally realized that you can just do this stupid
    method of constructing a regex and converted to that.
    """

    ans = 0

    def convert(rn) -> str:
        """
        This function converts a rule number to a regex. It uses the ``for`` loop to
        deal with the OR cases, and then joins them with "|"s. For each of the sequence
        rules, it calls itself recursively to generate a regex for the sub-rule.
        """
        parts = []
        for r in RULES[rn]:
            if isinstance(r, str):
                return r
            else:
                parts.append("".join(convert(x) for x in r))
        return "(" + "|".join(parts) + ")"

    regex = convert(0)
    for s in strs:
        if rematch(regex, s):
            ans += 1

    return ans


ans_part1 = part1()
print(ans_part1)

# Store the attempts that failed here.
tries = []
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == 198

########################################################################################
print("\nPart 2:")


def part2() -> int:
    """
    This is exactly the same as Part 1, except for there's special handling for rules 8
    and 11.

    The new Rule 8 is:

        8: 42 | 42 8

    This encodes a Kleene star in regex. It could be written as:

        (42)(42)*

        or

        (42)+

    (obviously replace 42 with the full expansion of the regex for 42).

    The new Rule 11 is:

        11: 42 31 | 42 11 31

    This is impossible to represent cleanly with a regular expression. The reason for
    this is that with a regular expression, you cannot maintain a stack (which is
    basically what this rule is). This causes the language represented by this grammar
    to no longer be regular, and therefore not encodable in a regular expression.

    Note that if you have a 42 there always must be a 31 on the other side. For example,
    the following is valid:

        42 42 31 31

    whereas:

        42 31 31

    would not be because there are too many 31s. This is impossible to represent with a
    regular expression and I would have needed to implement a push-down automata[1] that
    recognized the newly-created context-free grammar[2] instead.

    Note, the problem encoded by this rule is the *parentheses matching problem* which
    is basically "can you tell if a string of parentheses has all matching parentheses".
    Conceptually, whenever you see an opening parentheses, you add a token to your stack
    (meaning you are expecting a closing parentheses) and whenever you see a close
    parentheses, then you remove a token from the stack. I want to emphasize that this
    is not possible (in the general case) with regular expressions as famously pointed
    out by this StackOverflow post[3].

    The key insight for Rule 11 is twofold. First, rule 11 is only used on the RHS of
    the grammar once, meaning that once you enter into rule 11, you never exit it.
    Secondly, the inputs are *not* arbitrarily large, there is a specific set of inputs
    that you need to handle of which no input is more than ~100 characters. This means
    that you can just construct ~10 regular expressions with varrying numbers of
    nestings of the 42, 31 rule-pair and see if any of them match on every given input.

    ************************************************************************************

    Overall, I did not like this problem basically at all because cheezing it was the
    fastest way to an answer on both parts. I literally realized it was a regular
    language about 2 seconds in to reading the description on Part 1, but then I didn't
    think that just constructing the regular expression would actually work.

    Similarly, for Part 2, although there was text saying that you only have to solve
    for the specific case, I literally had no idea how *not* to solve for the general
    case for a *very* long time.

    Obviously, my opinion of the problem is tainted by the fact tha I did very poorly on
    the leaderboard (1931/4038), but I also think that it's unfortunate that it didn't
    actually force anybody to learn anything new.

    I spent probably 45 minutes trying to do part 1 "correctly", and then another 4.5
    hours trying to do part 2 "correctly" with a variety of methods.

    [1]: https://en.wikipedia.org/wiki/Pushdown_automaton
    [2]: https://en.wikipedia.org/wiki/Context-free_grammar
    [3]: https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags
    """

    def convert(rn, n11s) -> str:
        """
        This function converts a rule number to a regex. It uses the ``for`` loop to
        deal with the OR cases, and then joins them with "|"s. For each of the sequence
        rules, it calls itself recursively to generate a regex for the sub-rule.
        """
        parts = []
        if rn == 8:
            return "(" + convert(42, n11s) + ")" + "+"
        elif rn == 11:
            if n11s == 0:
                return "(" + convert(42, n11s) + convert(31, n11s) + ")"
            return (
                "(("
                + convert(42, n11s)
                + convert(31, n11s)
                + ")|("
                + convert(42, n11s)
                + convert(11, n11s - 1)
                + convert(31, n11s)
                + "))"
            )

        for r in RULES[rn]:
            if isinstance(r, str):
                return r
            else:
                parts.append("".join(convert(x, n11s) for x in r))
        return "(" + "|".join(parts) + ")"

    regexes = [convert(0, i) for i in range(10)]
    ans = 0
    for s in strs:
        for regex in regexes:
            if rematch(regex, s):
                ans += 1
                break

    return ans


ans_part2 = part2()
print(ans_part2)

# Store the attempts that failed here.
tries2 = [236]
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 372
