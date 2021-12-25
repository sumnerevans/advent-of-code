#! /usr/bin/env python3
"""
Download the JSON from:

https://adventofcode.com/YYYY/leaderboard/private/view/XXXXXX.json

where YYYY is the year, and XXXXXX is the leaderboard ID.

Pass the file as the first argument.
"""

import json
import sys
from collections import defaultdict

with open(sys.argv[1]) as f:
    leaderboard = json.load(f).get("members")

rankings = defaultdict(list)

for k, v in leaderboard.items():
    if v.get("stars") == 50:  # Consider only people who completed all of the problems.
        name = v.get("name")
        if name is None:
            name = f"(anonymous user #{k})"
        for day, completion_times in v.get("completion_day_level").items():
            day = int(day)
            for part, val in completion_times.items():
                part = int(part)
                rankings[(day, part)].append((int(val["get_star_ts"]), name))

user_cumulative_scores = defaultdict(int)
user_scores_per_day = defaultdict(list)

for (day, part), v in sorted(rankings.items()):
    for rank, (_, name) in enumerate(sorted(v), start=1):
        if day != 1:
            user_cumulative_scores[name] += len(rankings) - rank
        user_scores_per_day[name].append(rank)

max_name = max(map(len, user_cumulative_scores.keys()))

print("Name".ljust(max_name + 2), "Total", *(f"  {d+1:02} " for d in range(25)))
print(" " * (max_name + 2), "Part:", *(" 1  2" for _ in range(25)))
print("=" * (max_name + 2), "=" * 5, *("=====" for _ in range(25)))


def colorize(rank):
    GOLD = "\033[1;32m"
    SILVER = "\033[1;33m"
    BRONZE = "\033[1;31m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"
    if rank == 1:
        return GOLD + BOLD + UNDERLINE + str(rank) + ENDC
    elif rank == 2:
        return SILVER + BOLD + UNDERLINE + str(rank) + ENDC
    elif rank == 3:
        return BRONZE + BOLD + UNDERLINE + str(rank) + ENDC
    else:
        return str(rank)


for name, score in sorted(
    user_cumulative_scores.items(), key=lambda kv: kv[1], reverse=True
):
    print(
        name.ljust(max_name + 2),
        str(score).rjust(5),
        "",
        "  ".join((colorize(dr) for dr in user_scores_per_day[name])),
    )
