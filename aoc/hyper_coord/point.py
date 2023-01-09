from __future__ import annotations

from typing import Generator


class HyperPoint:
    coords: list[int]

    def __init__(self, *coords: int) -> None:
        self.coords = list(coords)

    @classmethod
    def create_uniform(cls, coord: int, dimensions: int) -> HyperPoint:
        return HyperPoint(*[coord for _ in range(dimensions)])

    @staticmethod
    def from_coord_str(coord_str: str) -> HyperPoint:
        return HyperPoint(*coord_str.split(','))

    @property
    def dimensions(self) -> int:
        return len(self.coords)

    @property
    def all_neighbors(self) -> Generator[HyperPoint, None, None]:
        yield from self.__all_neighbors_intern([], self.dimensions - 1)

    def __str__(self) -> str:
        return f'[{"/".join([str(coord) for coord in self.coords])}]'

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: HyperPoint) -> HyperPoint:
        self.__check(other)
        return HyperPoint(*map(lambda t: t[0] + t[1], zip(self.coords, other.coords)))

    def __iadd__(self, other: HyperPoint) -> HyperPoint:
        self.__check(other)
        for i in range(self.dimensions):
            self.coords[i] += other.coords[i]
        return self

    def __sub__(self, other: HyperPoint) -> HyperPoint:
        return HyperPoint(*map(lambda t: t[0] - t[1], zip(self.coords, other.coords)))

    def __isub__(self, other: HyperPoint) -> HyperPoint:
        self.__check(other)
        for i in range(self.dimensions):
            self.coords[i] -= other.coords[i]
        return self

    def __copy__(self) -> HyperPoint:
        return HyperPoint(*self.coords)

    def __eq__(self, other: HyperPoint) -> bool:
        self.__check(other)
        for i in range(self.dimensions):
            if self.coords[i] != other.coords[i]:
                return False
        return True

    def __hash__(self) -> int:
        return hash(str(self))

    def __getitem__(self, item: int) -> int:
        return self.coords[item]

    def __setitem__(self, key: int, value: int) -> None:
        self.coords[key] = value

    def __check(self, other: HyperPoint) -> None:
        if not isinstance(other, HyperPoint):
            raise ValueError('Can only use 2 PointXDs for this function.')
        if self.dimensions != other.dimensions:
            raise ValueError('Points need to have same dimensions.')

    def __all_neighbors_intern(self, coords: list[int], dimension: int) -> Generator[HyperPoint, None, None]:
        self_coord = self.coords[dimension]
        if dimension == 0:
            for coord in range(self_coord - 1, self_coord + 2):
                point = HyperPoint(*reversed(coords + [coord]))
                if point != self:
                    yield point
            return
        for coord in range(self_coord - 1, self_coord + 2):
            yield from self.__all_neighbors_intern(coords + [coord], dimension - 1)
