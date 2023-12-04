import math

from aoc.coord2d.point import Point
from aoc.input import read_input


def parse_asteroid_positions(region: list[str]) -> set[Point]:
    result = set()
    for y, line in enumerate(region):
        for x, entity in enumerate(line):
            if entity == '#':
                result.add(Point(x, y))
    return result


def normalize(vector: Point) -> Point:
    _min = min(abs(vector.x), abs(vector.y))
    if _min == 0:
        div = max(abs(vector.x), abs(vector.y))
        return Point(vector.x // div, vector.y // div)
    _min_len = 1
    while _min_len < _min:
        div = _min / _min_len
        x, rest = divmod(vector.x, div)
        if rest != 0:
            _min_len += 1
            continue
        y, rest = divmod(vector.y, div)
        if rest != 0:
            _min_len += 1
            continue
        return Point(int(x), int(y))
    return vector


def get_angle(vector: Point) -> float:
    return (math.atan2(vector.y, vector.x) * 180 / math.pi + 90) % 360


def has_line_of_sight(start: Point, end: Point, obstacles: set[Point]) -> bool:
    vector = normalize(end - start)
    current = start + vector
    while current != end:
        if current in obstacles:
            return False
        current += vector
    return True


def get_visible_asteroids(asteroid: Point, asteroids: set[Point]) -> set[Point]:
    return {other for other in asteroids if asteroid != other and has_line_of_sight(asteroid, other, asteroids)}


def count_visible_asteroids(asteroid: Point, asteroids: set[Point]) -> int:
    return len(get_visible_asteroids(asteroid, asteroids))


def find_best_monitoring_station(asteroids: set[Point]) -> tuple[Point, int]:
    best = 0
    station = Point(0, 0)
    for asteroid in asteroids:
        visible = count_visible_asteroids(asteroid, asteroids)
        if visible > best:
            best = visible
            station = asteroid
    return station, best


def vaporize(station: Point, original_asteroids: set[Point]) -> list[Point]:
    asteroids = original_asteroids.copy()
    asteroids.remove(station)
    result = []

    while len(asteroids):
        visible = sorted(get_visible_asteroids(station, asteroids), key=lambda _other: get_angle(_other - station))
        for other in visible:
            asteroids.remove(other)
            result.append(other)

    return result


_lines = read_input()
_asteroids = parse_asteroid_positions(_lines)

_station, part1 = find_best_monitoring_station(_asteroids)
print(f'Part 1: {part1}')
part2 = vaporize(_station, _asteroids)[199]
print(f'Part 2: {part2.x * 100 + part2.y}')
