#! /usr/bin/env python3

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

scores = defaultdict(int)

for day, v in sorted(rankings.items()):
    for rank, (_, name) in enumerate(sorted(v, reverse=True), start=1):
        scores[name] += rank

max_name = max(map(len, scores.keys()))

for name, score in sorted(scores.items(), key=lambda kv: kv[1], reverse=True):
    print(name.ljust(max_name + 2), score)
