from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Generator, Optional


def sin(degrees: int) -> int:
    if degrees % 90 != 0:
        raise AttributeError('This sin can only handle 90° intervals.')
    if degrees == 90:
        return 1
    if degrees == 270:
        return -1
    return 0


def cos(degrees: int) -> int:
    if degrees % 90 != 0:
        raise AttributeError('This cos can only handle 90° intervals.')
    degrees = degrees % 360
    if degrees == 0:
        return 1
    if degrees == 180:
        return -1
    return 0


def create_rotation_matrix(x: int, y: int, z: int) -> list[list[int]]:
    alpha = z
    beta = y
    gamma = x
    return [
        [
            cos(alpha) * cos(beta),
            cos(alpha) * sin(beta) * sin(gamma) - sin(alpha) * cos(gamma),
            cos(alpha) * sin(beta) * cos(gamma) + sin(alpha) * sin(gamma)
        ],
        [
            sin(alpha) * cos(beta),
            sin(alpha) * sin(beta) * sin(gamma) + cos(alpha) * cos(gamma),
            sin(alpha) * sin(beta) * cos(gamma) - cos(alpha) * sin(gamma)
        ],
        [
            -sin(beta),
            cos(beta) * sin(gamma),
            cos(beta) * cos(gamma)
        ]
    ]


angles = [0, 90, 180, 270]


def rotations() -> Generator[tuple[int, int, int], None, None]:
    for x in angles:
        for y in angles:
            for z in angles:
                yield x, y, z


def rotation_matrices() -> Generator[list[list[int]], None, None]:
    for x, y, z in rotations():
        yield create_rotation_matrix(x, y, z)


@dataclass
class Beacon:
    x: int
    y: int
    z: int

    def __hash__(self) -> int:
        return hash(f'[{self.x}, {self.y}, {self.z}')

    def __add__(self, other: Any) -> Beacon:
        if not isinstance(other, Beacon):
            raise ValueError
        return Beacon(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Any) -> Beacon:
        if not isinstance(other, Beacon):
            raise ValueError
        return Beacon(self.x - other.x, self.y - other.y, self.z - other.z)

    def rotated(self, rotation: list[list[int]]) -> Beacon:
        return Beacon(
            self.x * rotation[0][0] + self.y * rotation[0][1] + self.z * rotation[0][2],
            self.x * rotation[1][0] + self.y * rotation[1][1] + self.z * rotation[1][2],
            self.x * rotation[2][0] + self.y * rotation[2][1] + self.z * rotation[2][2],
        )


class Scanner:
    scanner_id: int
    pos: Beacon
    beacons: list[Beacon]

    def __init__(self, scanner_id: int) -> None:
        self.scanner_id = scanner_id
        self.pos = Beacon(0, 0, 0)
        self.beacons = []

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Scanner):
            return False
        return self.scanner_id == other.scanner_id

    def rotated(self, rotation: list[list[int]]) -> Scanner:
        result = Scanner(self.scanner_id)
        for beacon in self.beacons:
            result.beacons.append(beacon.rotated(rotation))
        return result

    def transformed(self, diff: Beacon) -> Scanner:
        result = Scanner(self.scanner_id)
        for beacon in self.beacons:
            result.beacons.append(beacon + diff)
        result.pos = diff
        return result


file_name = '../data/2021/day19.txt'
need_overlap = 12
scanners = []
fill_scanner: Optional[Scanner] = None
with open(file_name) as file:
    for line in file.readlines():
        match re.split('[ ,]', line.strip()):
            case '---', 'scanner', _scanner_id, '---':
                if fill_scanner is not None:
                    scanners.append(fill_scanner)
                fill_scanner = Scanner(_scanner_id)
            case _x, _y, _z:
                fill_scanner.beacons.append(Beacon(int(_x), int(_y), int(_z)))
scanners.append(fill_scanner)


def find_match(s1: Scanner, s2: Scanner) -> Optional[Scanner]:
    for rotation in rotation_matrices():
        rotated = s2.rotated(rotation)
        for i in range(len(s1.beacons) - need_overlap):
            for j in range(len(rotated.beacons) - need_overlap):
                diff = s1.beacons[i] - rotated.beacons[j]
                transformed = rotated.transformed(diff)
                count = 0
                for beacon in s1.beacons:
                    if beacon in transformed.beacons:
                        count += 1
                if count >= need_overlap:
                    return transformed


done_scanners = [scanners[0]]
scanners = scanners[1:]
while len(scanners):
    for done_scanner in done_scanners:
        remove = []
        for _scanner in scanners:
            transformed_scanner = find_match(done_scanner, _scanner)
            if transformed_scanner is not None:
                remove.append(_scanner)
                done_scanners.append(transformed_scanner)
        for _scanner in remove:
            scanners.remove(_scanner)

all_beacons = set()
for _scanner in done_scanners:
    all_beacons |= set(_scanner.beacons)

max_dist = 0
for _i in range(len(done_scanners) - 1):
    for _j in range(_i + 1, len(done_scanners)):
        bdist = done_scanners[_i].pos - done_scanners[_j].pos
        dist = abs(bdist.x) + abs(bdist.y) + abs(bdist.z)
        if dist > max_dist:
            max_dist = dist

part1 = len(all_beacons)
print(f'Part 1: {part1}')
part2 = max_dist
print(f'Part 2: {part2}')
