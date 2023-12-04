from __future__ import annotations

from dataclasses import dataclass

from .point import Point


@dataclass
class Rect:
    top_left: Point
    bottom_right: Point

    @classmethod
    def from_size(cls, top_left: Point, width: int, height: int) -> Rect:
        return cls(top_left, top_left + Point(width, height))

    @property
    def width(self) -> int:
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> int:
        return self.bottom_right.y - self.top_left.y

    @property
    def middle(self) -> Point:
        return self.top_left + Point(self.width // 2, self.height // 2)

    def update(self, point: Point) -> None:
        if point.x < self.top_left.x:
            self.top_left.x = point.x
        if point.y < self.top_left.y:
            self.top_left.y = point.y
        if point.x > self.bottom_right.x:
            self.bottom_right.x = point.x
        if point.y > self.bottom_right.y:
            self.bottom_right.y = point.y

    def __contains__(self, item: Point) -> bool:
        return self.top_left.x <= item.x <= self.bottom_right.x and self.top_left.y <= item.y <= self.bottom_right.y


@dataclass
class Square(Rect):
    def __post_init__(self) -> None:
        if self.width != self.height:
            raise ValueError('Squares need to be square.')

    @classmethod
    def from_size(cls, top_left: Point, size: int) -> Square:
        return cls(top_left, top_left + Point(size, size))

    @property
    def size(self) -> int:
        return self.width
