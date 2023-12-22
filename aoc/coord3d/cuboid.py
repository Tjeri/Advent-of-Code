from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

from .point import Point3D
from ..coord2d.point import Point


@dataclass
class Cuboid:
    top_left: Point3D
    bottom_right: Point3D

    @classmethod
    def from_size(cls, top_left: Point3D, width: int, height: int, depth: int) -> Cuboid:
        return cls(top_left, top_left + Point3D(width, height, -depth))

    @property
    def width(self) -> int:
        return self.bottom_right.x - self.top_left.x + 1

    @property
    def height(self) -> int:
        return self.bottom_right.y - self.top_left.y + 1

    @property
    def depth(self) -> int:
        return self.top_left.z - self.bottom_right.z + 1

    @property
    def all_points(self) -> Generator[Point3D, None, None]:
        for z in range(self.top_left.z, self.bottom_right.z - 1, -1):
            for y in range(self.top_left.y, self.bottom_right.y + 1):
                for x in range(self.top_left.x, self.bottom_right.x + 1):
                    yield Point3D(x, y, z)

    @property
    def all_points_2d(self) -> Generator[Point, None, None]:
        for y in range(self.top_left.y, self.bottom_right.y + 1):
            for x in range(self.top_left.x, self.bottom_right.x + 1):
                yield Point(x, y)

    def update(self, point: Point3D) -> None:
        if point.x < self.top_left.x:
            self.top_left.x = point.x
        if point.y < self.top_left.y:
            self.top_left.y = point.y
        if point.z > self.top_left.z:
            self.top_left.z = point.z
        if point.x > self.bottom_right.x:
            self.bottom_right.x = point.x
        if point.y > self.bottom_right.y:
            self.bottom_right.y = point.y
        if point.z < self.bottom_right.z:
            self.bottom_right.z = point.z


@dataclass
class Cube(Cuboid):
    def __post_init__(self) -> None:
        if self.width != self.height:
            raise ValueError('Cubes need to be square.')

    @classmethod
    def from_size(cls, top_left: Point3D, size: int) -> Cube:
        return cls(top_left, top_left + Point3D(size, size, -size))

    @property
    def size(self) -> int:
        return self.width
