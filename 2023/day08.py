from itertools import cycle
from math import lcm

from parse import parse

from aoc.input import read_input

map_direction = {'R': 1, 'L': 0}
map_pattern = '{} = ({}, {})'


def parse_directions(lines: list[str]) -> cycle:
    return cycle([map_direction[direction] for direction in lines[0]])


def parse_map(lines: list[str]) -> dict[str, tuple[str, str]]:
    result = dict()
    for line in lines[2:]:
        node, left, right = parse(map_pattern, line)
        result[node] = (left, right)
    return result


def find_end(start: str, mapping: dict[str, tuple[str, str]], directions: cycle) -> int:
    steps = 0
    position = start
    while not position.endswith('Z'):
        steps += 1
        position = mapping[position][next(directions)]
    return steps


def part2(mapping: dict[str, tuple[str, str]], directions: cycle) -> int:
    cycles = [find_end(key, mapping, directions) for key in mapping.keys() if key.endswith('A')]
    return lcm(*cycles)


_lines = read_input(True)
_mapping = parse_map(_lines)
print(f'Part 1: {find_end("AAA", _mapping, parse_directions(_lines))}')
print(f'Part 2: {part2(_mapping, parse_directions(_lines))}')
