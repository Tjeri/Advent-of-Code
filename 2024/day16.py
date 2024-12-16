from typing import Callable

from aoc.coord2d.point import Point
from aoc.input import read_input
from aoc.pathfinding2.a_star import dijkstra, dijkstra_all_shortest_paths

T = tuple[Point, Point]


def parse_map(lines: list[str]) -> tuple[Point, Point, set[Point]]:
    start = None
    end = None
    positions = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                start = Point(x, y)
                positions.add(start)
            elif char == 'E':
                end = Point(x, y)
                positions.add(end)
            elif char == '.':
                positions.add(Point(x, y))
    if not start or not end:
        raise ValueError('Start or End missing')
    return start, end, positions


def create_neighbors_function(positions: set[Point]) -> Callable[[T], dict[T, float]]:
    def neighbors(node: T) -> dict[T, float]:
        position, direction = node
        result = {}
        if position + direction in positions:
            result[(position + direction, direction)] = 1
        turn_right = Point(direction.y, direction.x)
        turn_left = -turn_right
        if position + turn_right in positions:
            result[(position, turn_right)] = 1000
        if position + turn_left in positions:
            result[(position, turn_left)] = 1000
        return result

    return neighbors


def part1(lines: list[str]) -> float:
    start, end, positions = parse_map(lines)
    return dijkstra((start, Point(1, 0)), lambda node: node[0] == end, create_neighbors_function(positions))[0]


def part2(lines: list[str]) -> int:
    start, end, positions = parse_map(lines)
    _, paths = dijkstra_all_shortest_paths((start, Point(1, 0)), lambda node: node[0] == end, create_neighbors_function(positions))
    positions = set()
    for path in paths:
        for position, direction in path:
            positions.add(position)
    return len(positions)


_lines = read_input(True)
print('Part 1:', part1(_lines))
print('Part 2:', part2(_lines))
