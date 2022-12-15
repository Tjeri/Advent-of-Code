from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import Generator


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def range_to(self, end: Point) -> Generator[Point, None, None]:
        x_step = end.x - self.x
        if x_step == 0:
            x_step = 1
        x_step = x_step // abs(x_step)
        y_step = end.y - self.y
        if y_step == 0:
            y_step = 1
        y_step = y_step // abs(y_step)
        for y in range(self.y, end.y + y_step, y_step):
            for x in range(self.x, end.x + x_step, x_step):
                yield Point(x, y)

    @staticmethod
    def from_coord_str(coords: str) -> Point:
        x, y = coords.split(',')
        return Point(int(x), int(y))


class Map:
    spawn: Point
    blocked: set[Point]
    lowest_blocked_y: int = 0
    resting_sand: int = 0

    def __init__(self, spawn: Point) -> None:
        self.spawn = spawn
        self.blocked = set()

    def __copy__(self) -> Map:
        result = Map(self.spawn)
        result.blocked = copy(self.blocked)
        result.lowest_blocked_y = self.lowest_blocked_y
        result.resting_sand = self.resting_sand
        return result

    def add_line(self, start: Point, end: Point) -> None:
        for point in start.range_to(end):
            self.blocked.add(point)
            if point.y > self.lowest_blocked_y:
                self.lowest_blocked_y = point.y

    def is_blocked(self, point: Point, has_ground: bool) -> bool:
        if point in self.blocked:
            return True
        if has_ground:
            return point.y == self.lowest_blocked_y + 2
        return False

    def simulate(self, has_ground: bool) -> None:
        while self.spawn not in self.blocked and self.spawn_sand_unit(has_ground):
            pass

    def spawn_sand_unit(self, has_ground: bool) -> bool:
        sand = self.spawn
        while has_ground or sand.y < self.lowest_blocked_y:
            if not self.is_blocked(new_point := Point(sand.x, sand.y + 1), has_ground):
                sand = new_point
            elif not self.is_blocked(new_point := Point(sand.x - 1, sand.y + 1), has_ground):
                sand = new_point
            elif not self.is_blocked(new_point := Point(sand.x + 1, sand.y + 1), has_ground):
                sand = new_point
            else:
                self.blocked.add(sand)
                self.resting_sand += 1
                return True
        return False


cave_1 = Map(Point(500, 0))
with open('../data/2022/day14.txt') as file:
    for line in file.readlines():
        line = line.strip()
        _points = list(map(Point.from_coord_str, line.split(' -> ')))
        for i in range(1, len(_points)):
            cave_1.add_line(_points[i - 1], _points[i])
cave_2 = copy(cave_1)

cave_1.simulate(False)
print(f'Part 1: {cave_1.resting_sand}')
cave_2.simulate(True)
print(f'Part 1: {cave_2.resting_sand}')
