from __future__ import annotations

from enum import Enum

from aoc.input import read_input
from aoc.pathfinding.flooding import flood
from aoc.utils.list import flatten


class Direction(Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)

    @property
    def opposite(self) -> Direction:
        if self is Direction.North:
            return Direction.South
        if self is Direction.South:
            return Direction.North
        if self is Direction.East:
            return Direction.West
        if self is Direction.West:
            return Direction.East
        raise ValueError('Unknown Direction.')

    def __radd__(self, other: tuple[int, int]) -> tuple[int, int]:
        return other[0] + self.value[0], other[1] + self.value[1]


pipe_map = {
    '|': (Direction.North, Direction.South),
    '-': (Direction.East, Direction.West),
    'L': (Direction.North, Direction.East),
    'J': (Direction.North, Direction.West),
    '7': (Direction.South, Direction.West),
    'F': (Direction.South, Direction.East),
    '.': ()
}


def find_start(lines: list[str] | list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                return x, y
    raise ValueError('No starting position found.')


def get_start_direction(lines: list[str] | list[list[str]], x: int, y: int, distance: int = 1) -> Direction:
    if Direction.South in pipe_map[lines[y - distance][x]]:
        return Direction.North
    elif Direction.North in pipe_map[lines[y + distance][x]]:
        return Direction.South
    elif Direction.West in pipe_map[lines[y][x + distance]]:
        return Direction.East
    else:
        raise ValueError('Start only connected to 1 pipe.')


def part1(lines: list[str]) -> int:
    start_x, start_y = find_start(lines)
    direction = get_start_direction(lines, start_x, start_y)
    x, y = (start_x, start_y) + direction
    steps = 1
    while x != start_x or y != start_y:
        step = pipe_map[lines[y][x]]
        if direction.opposite == step[0]:
            direction = step[1]
        else:
            direction = step[0]
        x, y = (x, y) + direction
        steps += 1
    return steps // 2


def part2(lines: list[str]) -> int:
    lines = [flatten([['*', char] for char in line] + ['*']) for line in lines]
    lines = flatten([[['*'] * len(line), line] for line in lines])
    start_x, start_y = find_start(lines)
    direction = get_start_direction(lines, start_x, start_y, 2)
    lines[start_y][start_x] = '#'
    x, y = (start_x, start_y) + direction
    lines[y][x] = '#'
    x, y = (x, y) + direction
    while x != start_x or y != start_y:
        step = pipe_map[lines[y][x]]
        lines[y][x] = '#'
        if direction.opposite == step[0]:
            direction = step[1]
        else:
            direction = step[0]
        x, y = (x, y) + direction
        lines[y][x] = '#'
        x, y = (x, y) + direction

    check = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            check.append((x, y))

    flood(lines, {'#'}, '0')

    result = 0
    for line in lines:
        for char in line:
            if char not in ('#', '0', '*'):
                result += 1
    return result


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 2: {part2(_lines)}')
