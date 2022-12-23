from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point:
    x: int = 0
    y: int = 0

    @staticmethod
    def from_coord_str(coord_str: str) -> Point:
        x, y = coord_str.split(',')
        return Point(int(x), int(y))

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Point) -> Point:
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Point) -> Point:
        self.x -= other.x
        self.y -= other.y
        return self

    def __copy__(self) -> Point:
        return Point(self.x, self.y)

    def __hash__(self) -> int:
        return hash(f'{self.x}/{self.y}')

    def manhattan_distance(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)
