from typing import Callable

from parse import parse

from aoc.coord2d.point import Point
from aoc.input import read_input

pattern = '{} {:d} (#{})'
directions = {
    'R': Point(1, 0), 'D': Point(0, 1), 'L': Point(-1, 0), 'U': Point(0, -1),
    '0': Point(1, 0), '1': Point(0, 1), '2': Point(-1, 0), '3': Point(0, -1)
}


def parse_line(line: str) -> tuple[str, int]:
    direction, distance, _ = parse(pattern, line).fixed
    return direction, distance


def parse_line2(line: str) -> tuple[str, int]:
    _, _, _hex = parse(pattern, line).fixed
    return _hex[5], int(_hex[:5], 16)


def parse_edges(lines: list[str], parsing: Callable[[str], tuple[str, int]]) -> list[Point]:
    position = Point(0, 0)
    trench = [position]
    for direction_str, distance in [parsing(line) for line in lines]:
        position = position + directions[direction_str] * distance
        trench.append(position)
    return trench


def total_area(points: list[Point]) -> int:
    outer = 1
    for i in range(len(points) - 1):
        diff = points[i + 1] - points[i]
        outer += (abs(diff.x) + abs(diff.y)) / 2
    return int(outer) + shoelace(points)


def shoelace(points: list[Point]) -> int:
    area = 0
    for i in range(len(points) - 1):
        area += points[i].cross_product(points[i + 1])
    return area // 2


_lines = read_input(False)
print(f'Part 1: {total_area(parse_edges(_lines, parse_line))}')
print(f'Part 2: {total_area(parse_edges(_lines, parse_line2))}')
