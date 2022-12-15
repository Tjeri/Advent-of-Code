from __future__ import annotations

from dataclasses import dataclass
from typing import Generator


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @property
    def tuning_frequency(self) -> int:
        return 4_000_000 * self.x + self.y

    def distance(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def range_to(self, end: Point) -> Generator[Point, None, None]:
        x_step = end.x - self.x
        if x_step == 0:
            x_step = 1
        x_step = x_step // abs(x_step)
        y_step = end.y - self.y
        if y_step == 0:
            y_step = 1
        y_step = y_step // abs(y_step)
        for y in range(self.y, end.y + y_step, y_step):
            for x in range(self.x, end.x + x_step, x_step):
                yield Point(x, y)


@dataclass
class Sensor:
    position: Point
    beacon: Point

    @staticmethod
    def from_line(line: str) -> Sensor:
        start = line.index('x=', 10) + 2
        end = line.index(',', start)
        sensor_x = int(line[start:end])
        start = line.index('y=', end) + 2
        end = line.index(':', start)
        sensor_y = int(line[start:end])
        start = line.index('x=', end) + 2
        end = line.index(',', start)
        beacon_x = int(line[start:end])
        start = line.index('y=', end) + 2
        beacon_y = int(line[start:])
        return Sensor(Point(sensor_x, sensor_y), Point(beacon_x, beacon_y))

    def get_row_range(self, y: int, _min: int | None = None, _max: int | None = None) -> range | None:
        distance_to_beacon = self.position.distance(self.beacon)
        distance_to_y = abs(self.position.y - y)
        if distance_to_y > distance_to_beacon:
            return None
        x_distance = distance_to_beacon - distance_to_y
        start_x = self.position.x - x_distance
        if _min and _min > start_x:
            start_x = _min
        end_x = self.position.x + x_distance
        if _max and _max < end_x:
            end_x = _max
        return range(start_x, end_x + 1)

    def get_row_information(self, y: int, _min: int, _max: int) -> tuple[set[int], set[int]]:
        distance_to_beacon = self.position.distance(self.beacon)
        distance_to_y = abs(self.position.y - y)
        if distance_to_y > distance_to_beacon:
            return set(), set()
        x_distance = distance_to_beacon - distance_to_y
        beacons = {self.beacon.x} if self.beacon.y == y else set()
        impossible = set(range(max(self.position.x - x_distance, _min), min(self.position.x + x_distance, _max) + 1))
        impossible -= beacons
        return beacons, impossible


def get_sorted_ranges(y: int, _min: int | None = None, _max: int | None = None) -> list[range]:
    ranges: list[range] = []
    for sensor in sensors:
        if _range := sensor.get_row_range(y, _min, _max):
            ranges.append(_range)
    ranges.sort(key=lambda x: (x.start, x.stop))
    return ranges


def calculate_part_1(y: int) -> int:
    ranges = get_sorted_ranges(y)
    _min, _max = ranges[0].start, ranges[0].stop
    occupied = 0
    for _range in ranges:
        if _range.start <= _max:
            _max = max(_max, _range.stop)
        else:
            occupied += len(range(_min, _max))
            _min, _max = _range.start, _range.stop
    occupied += len(range(_min, _max))
    occupied -= len({sensor.beacon.x for sensor in sensors if sensor.beacon.y == y})
    return occupied


def calculate_part_2(_min_coord: int, _max_coord: int) -> int:
    for y in range(_min_coord, _max_coord + 1):
        ranges = get_sorted_ranges(y, _min_coord, _max_coord)
        _min, _max = ranges[0].start, ranges[0].stop
        if _min > _min_coord:
            return Point(_min_coord, y).tuning_frequency
        for _range in ranges:
            if _range.start <= _max:
                _max = max(_max, _range.stop)
            else:
                return Point(_max, y).tuning_frequency
        if _max - 1 < _max_coord:
            return Point(_max_coord, y).tuning_frequency
    raise ValueError


sensors: list[Sensor] = list()
with open('../data/2022/day15.txt') as file:
    for _line in file.readlines():
        sensors.append(Sensor.from_line(_line))

print(f'Part 1: {calculate_part_1(2_000_000)}')
print(f'Part 2: {calculate_part_2(0, 4_000_000)}')
