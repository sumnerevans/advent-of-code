#! /usr/bin/env python3

import os
import re
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple
import itertools
from functools import partial


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dx = 0
        self.dy = 0
        self.dz = 0

    def __repr__(self):
        return f'<Moon x={self.x}, y={self.y}, z={self.z}, dx={self.dx}, dy={self.dy}, dz={self.dz}>'

    def potential_energy(self):
        return sum(map(abs, (self.x, self.y, self.z)))

    def kinnetic_energy(self):
        return sum(map(abs, (self.dx, self.dy, self.dz)))

    def total_energy(self):
        return self.potential_energy() * self.kinnetic_energy()

    def to_tuple(self):
        return (self.x, self.y, self.z, self.dx, self.dy, self.dz)


class World:
    def __init__(self, moons):
        self.moons = list(moons)

    def _accels(self, a, b):
        if a < b:
            return (+1, -1)
        elif a == b:
            return (0, 0)
        elif a > b:
            return (-1, +1)

    def step(self):
        # Apply gravity.
        for m1, m2 in itertools.combinations(self.moons, r=2):
            ax = self._accels(m1.x, m2.x)
            ay = self._accels(m1.y, m2.y)
            az = self._accels(m1.z, m2.z)

            m1.dx, m2.dx = m1.dx + ax[0], m2.dx + ax[1]
            m1.dy, m2.dy = m1.dy + ay[0], m2.dy + ay[1]
            m1.dz, m2.dz = m1.dz + az[0], m2.dz + az[1]

        # Apply velocity
        for m in self.moons:
            m.x += m.dx
            m.y += m.dy
            m.z += m.dz

    def total_energy(self):
        return sum(map(Moon.total_energy, self.moons))

    def to_tuple(self):
        return tuple(map(Moon.to_tuple, self.moons))

    def __repr__(self):
        return f'<World moons={self.moons}>'


pos_re = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')

with open('12.txt') as f:
    world = World(Moon(*map(int, pos_re.match(line).groups())) for line in f)

print('Part 1:')

for _ in range(1000):
    world.step()

print(world.total_energy())

print('Part 2:')

with open('12.txt') as f:
    world = World(Moon(*map(int, pos_re.match(line).groups())) for line in f)

seen_states = set()
i = 0
while True:
    if i % 100000 == 0:
        print(i)
    current_state = world.to_tuple()
    if current_state in seen_states:
        print('Steps:', i)
        break

    seen_states.add(current_state)

    world.step()
    i += 1
