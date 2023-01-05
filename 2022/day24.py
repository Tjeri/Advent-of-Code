from dataclasses import dataclass
from enum import Enum

from aoc.coord2d.point import Point


class Direction(Enum):
    N = '^'
    E = '>'
    S = 'v'
    W = '<'

    @property
    def movement(self) -> Point:
        if self is D.N:
            return Point(0, -1)
        if self is D.E:
            return Point(1, 0)
        if self is D.S:
            return Point(0, 1)
        if self is D.W:
            return Point(-1, 0)
        raise ValueError


D = Direction


@dataclass
class Blizzard:
    start: Point
    direction: Direction

    def position(self, time: int) -> Point:
        return (self.start + self.direction.movement * time) % Point(width, height)


width: int = 0
height: int = 0
blizzards: list[Blizzard] = list()
_start: Point = Point(-1, -1)
_end: Point = Point(-1, -1)
with open('../data/2022/day24.txt') as file:
    for _y, _line in enumerate(file.readlines()):
        for _x, _char in enumerate(_line.strip()):
            if _y == 0 and _char == '.':
                _start = Point(_x - 1, -1)
                break
            if _char == '.':
                _end = Point(_x - 1, _y - 1)
                continue
            if _char == '#':
                continue
            blizzards.append(Blizzard(Point(_x - 1, _y - 1), Direction(_char)))
    width = _x - 1
    height = _y - 1


def get_blizzard_positions(time: int) -> set[Point]:
    return {blizzard.position(time) for blizzard in blizzards}


def move(start: Point, end: Point, start_time: int) -> int:
    def is_oob(point: Point) -> bool:
        if point.x < 0 or point.x >= width:
            return True
        if point.y < 0 or point.y >= height:
            return point not in (start, end)
        return False

    positions = {start}
    minute = start_time

    while positions and end not in positions:
        minute += 1
        current_blizzards = get_blizzard_positions(minute)
        next_positions = set()
        for position in positions:
            for neighbor in [position] + position.get_direct_neighbors():
                if not is_oob(neighbor) and neighbor not in current_blizzards:
                    next_positions.add(neighbor)
        positions = next_positions
    return minute


move_1 = move(_start, _end, 0)
print(f'Part 1: {move_1}')
move_2 = move(_end, _start, move_1)
move_3 = move(_start, _end, move_2)
print(f'Part 2: {move_3}')
