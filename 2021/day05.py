from dataclasses import dataclass

from aoc.coord2d.point import Point


@dataclass
class Line:
    start: Point
    end: Point

    def __init__(self, raw: str) -> None:
        parts = raw.split(' -> ')
        self.start = Point(*[int(x) for x in parts[0].split(',')])
        self.end = Point(*[int(x) for x in parts[1].split(',')])

    def _calc_step_x(self) -> int:
        step = self.end.x - self.start.x
        return int(step / abs(step))

    def _calc_step_y(self) -> int:
        step = self.end.y - self.start.y
        return int(step / abs(step))

    @property
    def covered_points(self) -> list[Point]:
        covered = list()
        covered.append(self.start)
        if self.start.x == self.end.x:
            step = self._calc_step_y()
            for y in range(self.start.y + step, self.end.y, int(step)):
                covered.append(Point(self.start.x, y))
        elif self.start.y == self.end.y:
            step = self._calc_step_x()
            for x in range(self.start.x + step, self.end.x, step):
                covered.append(Point(x, self.start.y))
        else:
            step_x = self._calc_step_x()
            step_y = self._calc_step_y()
            for i in range(1, abs(self.start.x - self.end.x)):
                covered.append(Point(self.start.x + i * step_x, self.start.y + i * step_y))
        covered.append(self.end)
        return covered

    def is_straight(self):
        return self.start.x == self.end.x or self.start.y == self.end.y


result = set()
covered_points = set()
with open('../data/2021/day05.txt') as file:
    for _line in file.readlines():
        line = Line(_line)
        if not line.is_straight():
            continue
        for point in line.covered_points:
            if point in covered_points:
                result.add(point)
            else:
                covered_points.add(point)

print(f'Part 1: {len(result)}')

result = set()
covered_points = set()
with open('../data/2021/day05.txt') as file:
    for _line in file.readlines():
        line = Line(_line)
        for point in line.covered_points:
            if point in covered_points:
                result.add(point)
            else:
                covered_points.add(point)

print(f'Part 2: {len(result)}')
