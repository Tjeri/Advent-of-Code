from __future__ import annotations

from enum import Enum

from aoc.coord2d.point import Point
from aoc.input import read_input


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3

    @property
    def move(self) -> Point:
        if self is Direction.North:
            return Point(0, -1)
        if self is Direction.East:
            return Point(1, 0)
        if self is Direction.South:
            return Point(0, 1)
        if self is Direction.West:
            return Point(-1, 0)
        raise ValueError

    def mirror(self, which: str) -> Direction:
        if which == '/':
            if self is Direction.North:
                return Direction.East
            if self is Direction.East:
                return Direction.North
            if self is Direction.South:
                return Direction.West
            if self is Direction.West:
                return Direction.South
            raise ValueError
        if self is Direction.North:
            return Direction.West
        if self is Direction.East:
            return Direction.South
        if self is Direction.South:
            return Direction.East
        if self is Direction.West:
            return Direction.North
        raise ValueError


def count_energized(tiles: list[str], start_pos: Point, start_direction: Direction) -> int:
    beams = [(start_pos, start_direction)]
    history = set()
    while beams:
        beam = beams.pop(0)
        if beam in history:
            continue
        pos, direction = beam
        if pos.x < 0 or pos.x >= len(tiles[0]) or pos.y < 0 or pos.y >= len(tiles):
            continue
        history.add(beam)
        tile = tiles[pos.y][pos.x]
        if tile == '.':
            beams.append((pos + direction.move, direction))
        elif tile in ('/', '\\'):
            new_direction = direction.mirror(tile)
            beams.append((pos + new_direction.move, new_direction))
        elif tile == '|':
            if direction in (Direction.East, Direction.West):
                beams.append((pos + Direction.North.move, Direction.North))
                beams.append((pos + Direction.South.move, Direction.South))
            else:
                beams.append((pos + direction.move, direction))
        elif tile == '-':
            if direction in (Direction.North, Direction.South):
                beams.append((pos + Direction.East.move, Direction.East))
                beams.append((pos + Direction.West.move, Direction.West))
            else:
                beams.append((pos + direction.move, direction))
        else:
            raise ValueError
    return len({pos for pos, direction in history})


def get_best(tiles: list[str]) -> int:
    best = 0
    for x in range(len(tiles[0])):
        best = max(best, count_energized(tiles, Point(x, 0), Direction.South))
        best = max(best, count_energized(tiles, Point(x, len(tiles) - 1), Direction.North))
    for y in range(len(tiles)):
        best = max(best, count_energized(tiles, Point(0, y), Direction.East))
        best = max(best, count_energized(tiles, Point(len(tiles[0]) - 1, y), Direction.West))
    return best


_lines = read_input(True)
print(f'Part 1: {count_energized(_lines, Point(0, 0), Direction.East)}')
print(f'Part 2: {get_best(_lines)}')
