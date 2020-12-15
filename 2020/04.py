#! /usr/bin/env python3

import re
import sys


# Utilities
def rematch(pattern, string):
    return re.fullmatch(pattern, string)


# Input parsing

lines = [l.strip() for l in sys.stdin.readlines()]
passports = []
current = {}
for line in lines:
    if line == '':
        passports.append(current)
        current = {}
    for field in line.split():
        k, v = field.split(':')
        current[k] = v

passports.append(current)

########################################################################################
print('Part 1:')

fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}


def part1():
    v = 0
    for p in passports:
        missing = fields - set(p.keys())
        if missing in ({'cid'}, set()):
            v += 1

    return v


ans_part1 = part1()
print(ans_part1)

# Regression Test
assert ans_part1 == 264

########################################################################################
print('\nPart 2:')


def part2():
    v = 0
    for p in passports:
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if (not rematch(r'\d{4}', p.get('byr', ''))
                or not (1920 <= int(p.get('byr', '')) <= 2002)):
            continue

        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if (not rematch(r'\d{4}', p.get('iyr', ''))
                or not (2010 <= int(p.get('iyr', '')) <= 2020)):
            continue

        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if (not rematch(r'\d{4}', p.get('eyr', ''))
                or not (2020 <= int(p.get('eyr', '')) <= 2030)):
            continue

        # hgt (Height) - a number followed by either cm or in:
        #     If cm, the number must be at least 150 and at most 193.
        #     If in, the number must be at least 59 and at most 76.
        hm = rematch(r'(\d+)(cm|in)', p.get('hgt', ''))
        if not hm:
            continue
        height = int(hm.group(1))
        if hm.group(2) == 'cm':
            if not (150 <= height <= 193):
                continue
        else:
            if not (59 <= height <= 76):
                continue

        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        if not rematch(r'#[0-9a-f]{6}', p.get('hcl', '')):
            continue

        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        ecls = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
        if p.get('ecl', '') not in ecls:
            continue

        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        if not rematch(r'[0-9]{9}', p.get('pid', '')):
            continue

        # cid (Country ID) - ignored, missing or not.

        v += 1

    return v


ans_part2 = part2()
print(ans_part2)

# Regression Test
assert ans_part2 == 224
