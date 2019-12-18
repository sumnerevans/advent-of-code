#! /usr/bin/env python3

import os
import re
from collections import defaultdict
from typing import Dict, List, Tuple
import itertools


def chunk(iterable, n):
    if n < 1:
        raise Exception('not allowed')
    itertype = type(iterable) if type(iterable) in (list, set, tuple) else list

    container = []
    for x in iterable:
        container.append(x)
        if len(container) == n:
            yield itertype(container)
            container = []

    if len(container) > 0:
        yield itertype(container)


# (width, height)
dimensions = (25, 6)
with open('8.txt') as f:
    picture = map(int, f.read().strip())
    layers = list(chunk(picture, n=dimensions[0] * dimensions[1]))

print('Part 1:')

min_zero_layer = min(
    (layer.count(0), layer) for i, layer in enumerate(layers))[1]

print(min_zero_layer.count(1) * min_zero_layer.count(2))

print('Part 2:')

resulting_picture = layers[0]
for layer in layers[1:]:
    for i, (result_pixel,
            layer_pix) in enumerate(zip(
                resulting_picture,
                layer,
            )):
        if result_pixel != 2:
            continue

        resulting_picture[i] = layer_pix

pixel_char_map = {0: 'X', 1: ' '}
for line in chunk(resulting_picture, dimensions[0]):
    print(''.join(map(lambda c: pixel_char_map[c], line)))
