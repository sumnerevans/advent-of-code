#! /usr/bin/env python3

import heapq
import re
import string
import sys
import time
from copy import deepcopy
from collections import defaultdict
from typing import List, Match, Optional, Set, Tuple

test = False
debug = False
for arg in sys.argv:
    if arg == "--test":
        test = True
    if arg == "--debug":
        debug = True


def rematch(pattern: str, string: str) -> Optional[Match]:
    return re.fullmatch(pattern, string)


# Input parsing
input_start = time.time()

lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
STEP_DEPENDENCIES = defaultdict(set)
STEP_SUBSEQUENTS = defaultdict(set)
STEPS = set()
for line in lines:
    step, dep = rematch(
        "Step (.) must be finished before step (.) can begin.", line
    ).groups()
    STEPS.add(step)
    STEPS.add(dep)
    STEP_DEPENDENCIES[dep].add(step)
    STEP_SUBSEQUENTS[step].add(dep)
STARTS = sorted(STEPS - set(STEP_DEPENDENCIES.keys()))

input_end = time.time()

# Shared
########################################################################################
shared_start = time.time()

# Visualize the graph
if debug:
    import graphviz

    g = graphviz.Digraph()
    for k, v in STEP_SUBSEQUENTS.items():
        for x in v:
            g.edge(k, x)

    g.view()

shared_end = time.time()

# Part 1
########################################################################################
print(f"\n{'=' * 30}\n")
print("Part 1:")


def part1() -> str:
    """
    I'm solving Part 1 using a BFS-like algorithm. I maintain a *frontier*, effectively
    the set of elements that can be performed next. The rules state if there are
    multiple jobs that can be perfomred at once, the one that is lexicographicaly first
    should be performed. To accomplish this, I'm storing the frontier in a heap so that
    the lexicographicaly first element is always what gets popped of the heap.

    I'm pretty sure some sort of topological sort would also do the trick here.
    """
    frontier = deepcopy(STARTS)
    heapq.heapify(frontier)
    satisfied = set()
    s = ""
    while frontier:
        current = heapq.heappop(frontier)

        # If it's already been satisfied, skip.
        if current in satisfied:
            continue

        # Check to see if all of the current job's dependencies have been satisfied.
        sat = True
        for dep in STEP_DEPENDENCIES[current]:
            if dep not in satisfied:
                sat = False
                break
        if not sat:
            continue

        # Set the current job to satisfied, and add it to the ordering of the steps.
        satisfied.add(current)
        s += current

        # Add all of the jobs that depend on this job to the frontier. (It is fine if
        # they are not fully satisfied because of the sat check above.)
        for sub in STEP_SUBSEQUENTS[current]:
            heapq.heappush(frontier, sub)

    assert len(STEPS) == len(s)
    return s


part1_start = time.time()
ans_part1 = part1()
part1_end = time.time()
print(ans_part1)

if test:
    assert ans_part1 == "CABDFE", ans_part1

# Store the attempts that failed here.
tries = ["BCEGHAIJDKMNOLPRSTUFQVWXYZ"]
print("Tries Part 1:", tries)
assert ans_part1 not in tries, "Same as an incorrect answer!"


# Regression Test
assert test or ans_part1 == "BHMOTUFLCPQKWINZVRXAJDSYEG"

# Part 2
########################################################################################
print("\nPart 2:")


def part2() -> int:
    """
    I'm doing Part 2 using a discrete event simulation (DES). I'm assuming there's a way
    to do this using a topological sort as well, but I wanted to implement a DES.

    The basic idea of a DES is that you keep a priority queue of "events". Each event is
    a *discrete event* and mutates the state of the world in some way. In my case, the
    state of the world consists of how many workers are available; the set of jobs that
    are unstarted, started, and satisfied; and the time of the last completed job.
    """
    # Calculate the time it will take for each job to complete. For the full problem,
    # the time is 60 + (numeric letter of the alphabet, starting at 1)
    BASE_TIME = 60 if not test else 0
    WORKERS = 6 if not test else 2
    job_to_time = {c: BASE_TIME + ord(c) - ord("A") + 1 for c in string.ascii_uppercase}

    # World state
    T = 0
    unstarted: Set[str] = set(ans_part1)
    satisfied: Set[str] = set()
    workers_available: int = 0
    started: Set[str] = set()

    # Create the event queue. The queue contains tuples of (time, action, ID) where time
    # is the time at which the event occurs (note that this is the primary sort key in
    # the priority queue), action is the action type, and ID is an optional arbitrary ID
    # (used for the JOB DONE event).

    # We start by populating the queue with an inital set of events: one event for each
    # worker becoming available at time = 0.
    Q: List[Tuple[int, str, str]] = [
        (0, "WORKER AVAILABLE", "") for _ in range(WORKERS)
    ]

    # Loop through all of the events.
    while Q:
        t, action, id_ = heapq.heappop(Q) # extract the next event

        # Handle the different actions
        if action == "JOB DONE":
            started.remove(id_)  # remove from the set of jobs currently being performed
            satisfied.add(id_)  # add to the set of satisfied/completed jobs
            T = max(T, t)  # update the max time
        elif action == "WORKER AVAILABLE":
            # A worker has become available, increase the number of available workers.
            workers_available += 1
        elif action == "WORKER START":
            if id_ in started:
                # Skip if already being worked on.
                continue

            # Start work on the job.
            started.add(id_)
            unstarted.remove(id_)
            workers_available -= 1  # the worker is no longer available

            # Look up how long it will be until the job is completed. At that time, the
            # job will be done and the worker will become available. Add these events to
            # the queue.
            heapq.heappush(Q, (t + job_to_time[id_], "JOB DONE", id_))
            heapq.heappush(Q, (t + job_to_time[id_], "WORKER AVAILABLE", ""))

        # Then, check if we can have a worker start on a job.
        if workers_available > 0 and unstarted:
            for r in unstarted:
                # Can we actually do this job?
                issat = True
                for dep in STEP_DEPENDENCIES[r]:
                    if dep not in satisfied:
                        issat = False
                        break
                if issat:
                    heapq.heappush(Q, (t, "WORKER START", r))
                    break

    return T


part2_start = time.time()
ans_part2 = part2()
part2_end = time.time()
print(ans_part2)

# Store the attempts that failed here.
tries2 = [137]
print("Tries Part 2:", tries2)
assert ans_part2 not in tries2, "Same as an incorrect answer!"

# Regression Test
assert test or ans_part2 == 877

if debug:
    input_parsing = input_end - input_start
    shared = shared_end - shared_start
    part1_time = part1_end - part1_start
    part2_time = part2_end - part2_start
    print()
    print("DEBUG:")
    print(f"Input parsing: {input_parsing * 1000}ms")
    print(f"Shared: {shared * 1000}ms")
    print(f"Part 1: {part1_time * 1000}ms")
    print(f"Part 2: {part2_time * 1000}ms")
    print(f"TOTAL: {(input_parsing + shared + part1_time + part2_time) * 1000}ms")
