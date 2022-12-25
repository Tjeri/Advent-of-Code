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

    def __mul__(self, times: int) -> Point:
        return Point(times * self.x, times * self.y)

    def __imul__(self, times: int) -> Point:
        self.x *= times
        self.y *= times
        return self

    def __mod__(self, other: Point) -> Point:
        return Point(self.x % other.x, self.y % other.y)

    def __imod__(self, other: Point) -> Point:
        self.x %= other.x
        self.y %= other.y
        return self

    def __copy__(self) -> Point:
        return Point(self.x, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def manhattan_distance(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def get_neighbors(self) -> list[Point]:
        return [self + Point(0, -1), self + Point(1, 0), self + Point(0, 1), self + Point(-1, 0)]
