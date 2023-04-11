from aoc.coord2d.point import Point
from aoc.input import read_input


def get_direction(char: str) -> Point:
    if char == 'U':
        return Point(0, -1)
    if char == 'R':
        return Point(1, 0)
    if char == 'D':
        return Point(0, 1)
    if char == 'L':
        return Point(-1, 0)
    raise ValueError(f'Invalid direction: {char}')


def parse_path(_line: str) -> list[Point]:
    result = []
    pos = Point(0, 0)
    for step in _line.split(','):
        direction = get_direction(step[0])
        steps = int(step[1:])
        for i in range(1, steps + 1):
            result.append(pos + direction * i)
        pos += direction * steps
    return result


_lines = read_input()
_path1 = parse_path(_lines[0])
_path2 = parse_path(_lines[1])

_intersections = set(_path1).intersection(_path2)
print(f'Part 1: {min(_point.manhattan_distance(Point(0, 0)) for _point in _intersections)}')
print(f'Part 2: {2 + min(_path1.index(_intersection) + _path2.index(_intersection) for _intersection in _intersections)}')
