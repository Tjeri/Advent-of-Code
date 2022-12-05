from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


def range_overlap(range1, range2):
    return range(max(range1.start, range2.start), min(range1.stop, range2.stop))


@dataclass
class Cube:
    x: range
    y: range
    z: range

    @property
    def size(self) -> int:
        return len(self.x) * len(self.y) * len(self.z)

    def overlap(self, other: Cube) -> Optional[Cube]:
        overlap_x = range_overlap(self.x, other.x)
        overlap_y = range_overlap(self.y, other.y)
        overlap_z = range_overlap(self.z, other.z)
        if len(overlap_x) and len(overlap_y) and len(overlap_z):
            return Cube(overlap_x, overlap_y, overlap_z)
        return None

    def split(self, middle: Cube) -> list[Cube]:
        split = []
        # above middle Cube
        split.append(Cube(
            range(self.x.start, self.x.stop),
            range(self.y.start, self.y.stop),
            range(self.z.start, middle.z.start)
        ))
        # below middle Cube
        split.append(Cube(
            range(self.x.start, self.x.stop),
            range(self.y.start, self.y.stop),
            range(middle.z.stop, self.z.stop)
        ))
        # front of middle cube
        split.append(Cube(
            range(self.x.start, self.x.stop),
            range(self.y.start, middle.y.start),
            range(middle.z.start, middle.z.stop)
        ))
        # back of middle cube
        split.append(Cube(
            range(self.x.start, self.x.stop),
            range(middle.y.stop, self.y.stop),
            range(middle.z.start, middle.z.stop)
        ))
        # left of middle Cube
        split.append(Cube(
            range(self.x.start, middle.x.start),
            range(middle.y.start, middle.y.stop),
            range(middle.z.start, middle.z.stop)
        ))
        # right of middle Cube
        split.append(Cube(
            range(middle.x.stop, self.x.stop),
            range(middle.y.start, middle.y.stop),
            range(middle.z.start, middle.z.stop)
        ))
        return [cube for cube in split if cube.size > 0]


file_name = '../data/2021/day22.txt'
with open(file_name) as file:
    data = file.readlines()

pattern = re.compile(
    r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'
)
cubes: list[tuple[Cube, bool]] = []
for line in data:
    matches = re.match(pattern, line)
    groups = matches.groups()
    cubes.append((Cube(
        range(int(groups[1]), int(groups[2]) + 1),
        range(int(groups[3]), int(groups[4]) + 1),
        range(int(groups[5]), int(groups[6]) + 1)
    ), groups[0] == 'on'))

part1_range = range(-50, 51)
part1_base = Cube(part1_range, part1_range, part1_range)


def calculate_on(is_part1: bool) -> list[Cube]:
    on: list[Optional[Cube]] = []
    for cube, switch_on in cubes:
        if is_part1:
            cube = part1_base.overlap(cube)
            if cube is None:
                continue
        for i, _cube in enumerate(on):
            if _cube is None:
                continue
            overlap = cube.overlap(_cube)
            if overlap is None:
                continue
            on[i] = None
            on += _cube.split(overlap)
        if switch_on:
            on.append(cube)
    return [cube for cube in on if cube is not None]


part1 = sum([cube.size for cube in calculate_on(True)])
print(f'Part 1: {part1}')

part2 = sum([cube.size for cube in calculate_on(False)])
print(f'Part 2: {part2}')
