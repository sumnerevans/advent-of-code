#! /usr/bin/env python

with open('1.txt') as f:
    sequence = [int(line) for line in f]

print('Part 1:')
print(sum(sequence))

print('Part 2:')
frequency = 0
seen = set([0])
i = 0
while True:
    frequency += sequence[i % len(sequence)]
    if frequency in seen:
        print(frequency)
        break

    seen.add(frequency)
    i += 1
