from __future__ import annotations

from enum import Enum

from aoc.input import read_input
from aoc.utils.list import flatten


class Tile(Enum):
    Empty = 0
    Move = 1
    Fixed = 2

    @staticmethod
    def parse(char: str) -> Tile:
        if char == '.':
            return Tile.Empty
        if char == 'O':
            return Tile.Move
        return Tile.Fixed

    def __str__(self) -> str:
        if self is Tile.Empty:
            return '.'
        elif self is Tile.Move:
            return 'O'
        return '#'


Map = list[list[Tile]]


def convert(lines: list[str]) -> Map:
    return [[Tile.parse(char) for char in line] for line in lines]


def move_north(lines: Map) -> Map:
    for x in range(len(lines[0])):
        free_spaces = 0
        for y in range(len(lines)):
            if lines[y][x] == Tile.Empty:
                free_spaces += 1
            elif lines[y][x] == Tile.Fixed:
                free_spaces = 0
            else:
                lines[y][x] = Tile.Empty
                lines[y - free_spaces][x] = Tile.Move
    return lines


def move_west(lines: Map) -> Map:
    for y in range(len(lines)):
        free_spaces = 0
        for x in range(len(lines[0])):
            if lines[y][x] == Tile.Empty:
                free_spaces += 1
            elif lines[y][x] == Tile.Fixed:
                free_spaces = 0
            else:
                lines[y][x] = Tile.Empty
                lines[y][x - free_spaces] = Tile.Move
    return lines


def move_south(lines: Map) -> Map:
    for x in range(len(lines[0])):
        free_spaces = 0
        for y in range(len(lines) - 1, -1, -1):
            if lines[y][x] == Tile.Empty:
                free_spaces += 1
            elif lines[y][x] == Tile.Fixed:
                free_spaces = 0
            else:
                lines[y][x] = Tile.Empty
                lines[y + free_spaces][x] = Tile.Move
    return lines


def move_east(lines: Map) -> Map:
    for y in range(len(lines)):
        free_spaces = 0
        for x in range(len(lines[0]) - 1, -1, -1):
            if lines[y][x] == Tile.Empty:
                free_spaces += 1
            elif lines[y][x] == Tile.Fixed:
                free_spaces = 0
            else:
                lines[y][x] = Tile.Empty
                lines[y][x + free_spaces] = Tile.Move
    return lines


def cycle(lines: Map) -> Map:
    lines = move_north(lines)
    lines = move_west(lines)
    lines = move_south(lines)
    lines = move_east(lines)
    return lines


def make_key(lines: Map) -> str:
    return ''.join(str(tile.value) for tile in flatten(lines))


def calc_load(lines: Map) -> int:
    height = len(lines)
    load = 0
    for y in range(height):
        for x in range(len(lines[0])):
            if lines[y][x] == Tile.Move:
                load += height - y
    return load


def part1(lines: list[str]) -> int:
    height = len(lines)
    load = 0
    for x in range(len(lines[0])):
        free_spaces = 0
        for y in range(height):
            if lines[y][x] == '.':
                free_spaces += 1
            elif lines[y][x] == '#':
                free_spaces = 0
            else:
                load += height - y + free_spaces
    return load


def part2(lines: list[str]) -> int:
    lines = convert(lines)
    cycles = 0
    history: dict[str, int] = {}
    while cycles < 1_000_000_000:
        lines = cycle(lines)
        cycles += 1
        key = make_key(lines)
        if key in history:
            missing = 1_000_000_000 - cycles
            diff = cycles - history[key]
            cycles += (missing // diff) * diff
        else:
            history[key] = cycles
    return calc_load(lines)


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 1: {part2(_lines)}')
