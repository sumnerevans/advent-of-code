#! /usr/bin/env python3

import re
from collections import defaultdict
from datetime import datetime, timedelta
from itertools import combinations
from typing import Dict, List, Tuple

from dateutil import parser

line_re = re.compile('\[(.*)\] (.*)')
events = set()
with open('4.txt') as f:
    for line in f:
        time, event = line_re.match(line).groups()
        dt = parser.parse(time)
        events.add((dt, event))

events = sorted(events)

amount_asleep = defaultdict(int)
asleep_minutes = defaultdict(lambda: defaultdict(int))

current_guard = None
asleep_time = None
for time, desc in events:
    if desc.startswith('Guard'):
        current_guard = int(desc.split()[1][1:])
    elif desc == 'falls asleep':
        asleep_time = time
    elif desc == 'wakes up':
        amount_asleep[current_guard] += ((time - asleep_time).seconds // 60)
        current = asleep_time.minute
        while current < time.minute:
            asleep_minutes[current_guard][current] += 1
            current += 1

print('Part 1:')

most_asleep = max(amount_asleep.items(), key=lambda i: i[1])[0]
print('most asleep', most_asleep)

most_asleep_minute = max(
    asleep_minutes[most_asleep].items(), key=lambda i: i[1])[0]
print('most asleep minute', most_asleep_minute)

print(most_asleep * most_asleep_minute)

print('Part 2:')

max_asleep = 0
max_asleep_guard = None
max_asleep_min = None
for g, mins in asleep_minutes.items():
    for m, amount in mins.items():
        if amount > max_asleep:
            max_asleep_guard = g
            max_asleep_min = m
            max_asleep = amount

print(max_asleep_guard, max_asleep_min)
print(max_asleep_guard * max_asleep_min)
