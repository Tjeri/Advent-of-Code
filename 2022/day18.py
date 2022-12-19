from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __hash__(self) -> int:
        return hash(f'{self.x}/{self.y}/{self.z}')

    def adjacent_points(self) -> list[Point]:
        return [
            Point(self.x - 1, self.y, self.z),
            Point(self.x + 1, self.y, self.z),
            Point(self.x, self.y - 1, self.z),
            Point(self.x, self.y + 1, self.z),
            Point(self.x, self.y, self.z - 1),
            Point(self.x, self.y, self.z + 1),
        ]

    def take(self, func: Callable[[int, int], int], other: Point) -> None:
        self.x = func(self.x, other.x)
        self.y = func(self.y, other.y)
        self.z = func(self.z, other.z)

    def take_min(self, other: Point) -> None:
        self.take(min, other)

    def take_max(self, other: Point) -> None:
        self.take(max, other)

    @staticmethod
    def from_coord_str(coords: str) -> Point:
        x, y, z = coords.split(',')
        return Point(int(x), int(y), int(z))


def find_surface_area(point: Point) -> int:
    for neighbor in point.adjacent_points():
        reaches_surface(neighbor)
    return len([neighbor for neighbor in point.adjacent_points() if reaches_surface(neighbor)])


def reaches_surface(point: Point, history: set[Point] | None = None) -> bool:
    if point in points:
        return False
    if point.x < min_point.x or point.y < min_point.y or point.z < min_point.z \
            or point.x > max_point.x or point.y > max_point.y or point.z > max_point.z:
        return True
    if point in saved_surface_info:
        return saved_surface_info[point]
    if history is None:
        history = set()
    for neighbor in point.adjacent_points():
        if neighbor in history:
            continue
        if reaches_surface(neighbor, history | {point}):
            saved_surface_info[point] = True
            return True
    saved_surface_info[point] = False
    return False


points: set[Point] = set()
min_point: Point = Point(100, 100, 100)
max_point: Point = Point(0, 0, 0)
saved_surface_info: dict[Point, bool] = dict()
with open('../data/2022/day18.txt') as file:
    for line in file.readlines():
        _point = Point.from_coord_str(line.strip())
        min_point.take_min(_point)
        max_point.take_max(_point)
        points.add(_point)

surface1 = 6 * len(points) - sum([len([p for p in point.adjacent_points() if p in points]) for point in points])
print(f'Part 1: {surface1}')

surface2 = sum(find_surface_area(point) for point in points)
print(f'Part 2: {surface2}')
