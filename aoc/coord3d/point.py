from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Point3D:
    x: int = 0
    y: int = 0
    z: int = 0

    @staticmethod
    def from_coord_str(coord_str: str) -> Point3D:
        x, y, z = coord_str.split(',')
        return Point3D(int(x), int(y), int(z))

    def __add__(self, other: Point3D) -> Point3D:
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other: Point3D) -> Point3D:
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: Point3D) -> Point3D:
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __isub__(self, other: Point3D) -> Point3D:
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __copy__(self) -> Point3D:
        return Point3D(self.x, self.y, self.z)

    def __hash__(self) -> int:
        return hash(f'{self.x}/{self.y}/{self.z}')

    def get_all_neighbors(self) -> list[Point3D]:
        neighbors = []
        for z in range(self.z - 1, self.z + 2):
            for y in range(self.y - 1, self.y + 2):
                for x in range(self.x - 1, self.x + 2):
                    neighbors.append(Point3D(x, y, z))
        neighbors.remove(self)
        return neighbors
