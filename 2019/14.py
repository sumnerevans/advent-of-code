#! /usr/bin/env python3

import math
import os
import queue
from graphviz import Digraph
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools
from functools import partial

equation_graph = defaultdict(list)
eq_re = re.compile(r"(.*?) => (.*)")
factor_re = re.compile(r"\s?(\d+) (.*)")

num_of_el_required = defaultdict(int)
num_of_el_required["FUEL"] = 1

num_of_el_produced = defaultdict(int)

debug = False


def parse_factor(f):
    n, element = factor_re.match(f).groups()
    return int(n), element


def visualize_graph(filename):
    def format_node(key):
        return f"{key}-{num_of_el_produced[key]}-{num_of_el_required[key]}"

    g = Digraph("G", filename=filename, format="png")
    g.attr("node", shape="circle")
    g.attr(rankdir="RL")
    for k, v in equation_graph.items():
        for out in v:
            g.edge(
                format_node(k), format_node(out[0]), label=f"{out[1]} -> {out[2]}",
            )

    g.render()


# Read in the graph.
with open("14.txt") as f:
    for line in f:
        lhs, rhs = eq_re.match(line).groups()
        c2, rhs = parse_factor(rhs)
        for c1, el in (parse_factor(f) for f in lhs.split(",")):
            equation_graph[rhs].append((el, c1, c2))


def needs_more_production():
    return [
        (el, n) for el, n in num_of_el_required.items() if num_of_el_produced[el] < n
    ]


needs_more = needs_more_production()
i = 0
while len(needs_more) > 0:
    if debug:
        visualize_graph(f"/tmp/14.{i}")
        i += 1

    el, n = needs_more[0]
    for ingredient, in_amount, out_amount in equation_graph[el]:
        num_of_el_required[ingredient] += n / out_amount * in_amount

    num_of_el_produced[el] += n

    needs_more = needs_more_production()

if debug:
    visualize_graph(f"/tmp/14.{i}")

print("Part 1:")
print(num_of_el_produced["ORE"])

print("Part 2:")
