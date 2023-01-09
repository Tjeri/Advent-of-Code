from __future__ import annotations

from typing import Generator

from .point import HyperPoint


class HyperRect:
    top_left: HyperPoint
    bottom_right: HyperPoint

    def __init__(self, top_left: HyperPoint, bottom_right: HyperPoint) -> None:
        if top_left.dimensions != bottom_right.dimensions:
            raise ValueError('Top left and bottom right have different dimensions.')
        self.top_left = top_left
        self.bottom_right = bottom_right

    @classmethod
    def from_size(cls, top_left: HyperPoint, *sizes: int) -> HyperRect:
        if top_left.dimensions != len(sizes):
            raise ValueError('Top left Point and sizes have different dimensions.')
        return cls(top_left, top_left + HyperPoint(*sizes))

    @property
    def dimensions(self) -> int:
        return self.top_left.dimensions

    def size(self, dimension: int) -> int:
        return self.bottom_right[dimension] - self.top_left[dimension]

    @property
    def all_points(self) -> Generator[HyperPoint, None, None]:
        yield from self.__all_points_intern([], self.dimensions - 1)

    def update(self, point: HyperPoint) -> None:
        for dimension in range(self.dimensions):
            if point[dimension] < self.top_left[dimension]:
                self.top_left[dimension] = point[dimension]
            if point[dimension] > self.bottom_right[dimension]:
                self.bottom_right[dimension] = point[dimension]

    def __str__(self) -> str:
        return f'HyperRect({self.top_left} | {self.bottom_right})'

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: HyperRect) -> bool:
        if not isinstance(other, HyperRect):
            raise ValueError('Can only use 2 RectXD for this function.')
        if self.dimensions != other.dimensions:
            raise ValueError('Rects need to have same dimensions.')
        return self.top_left == other.top_left and self.bottom_right == other.bottom_right

    def __hash__(self) -> int:
        return hash(str(self))

    def __all_points_intern(self, coords: list[int], dimension: int) -> Generator[HyperPoint, None, None]:
        top_left = self.top_left[dimension]
        bottom_right = self.bottom_right[dimension]
        if dimension == 0:
            for coord in range(top_left, bottom_right + 1):
                yield HyperPoint(*reversed(coords + [coord]))
            return
        for coord in range(top_left, bottom_right + 1):
            yield from self.__all_points_intern(coords + [coord], dimension - 1)


class HyperSquare(HyperRect):
    def __init__(self, top_left: HyperPoint, bottom_right: HyperPoint) -> None:
        super().__init__(top_left, bottom_right)
        size = super().size(0)
        for dimension in range(1, self.dimensions):
            if super().size != size:
                raise ValueError('HyperSquares need to be square.')

    @classmethod
    def from_size(cls, top_left: HyperPoint, size: int) -> HyperSquare:
        return cls(top_left, top_left + HyperPoint(*[size for _ in range(top_left.dimensions)]))

    @property
    def size(self) -> int:
        return super().size(0)
