from copy import copy

from aoc.coord2d.point import Point
from aoc.input import read_input


def turn(point: Point, right: bool, degrees: int, around: Point = Point(0, 0)) -> Point:
    translated = point - around
    degrees %= 360
    if degrees == 0:
        return point
    if degrees == 180:
        return translated * -1 + around
    if degrees == 270:
        right = not right
    if right:
        return Point(-translated.y, translated.x) + around
    return Point(translated.y, -translated.x) + around


def move_ship(position: Point, direction: Point, lines: list[str]) -> Point:
    for line in lines:
        instruction = line[0]
        distance = int(line[1:])
        if instruction == 'N':
            position += Point(0, -1) * distance
        elif instruction == 'S':
            position += Point(0, 1) * distance
        elif instruction == 'E':
            position += Point(1, 0) * distance
        elif instruction == 'W':
            position += Point(-1, 0) * distance
        elif instruction == 'F':
            position += direction * distance
        elif instruction == 'R':
            direction = turn(direction, True, distance)
        elif instruction == 'L':
            direction = turn(direction, False, distance)
        else:
            raise ValueError(instruction)
    return position


def move_ship2(position: Point, waypoint: Point, lines: list[str]) -> Point:
    for line in lines:
        instruction = line[0]
        distance = int(line[1:])
        if instruction == 'N':
            waypoint += Point(0, -1) * distance
        elif instruction == 'S':
            waypoint += Point(0, 1) * distance
        elif instruction == 'E':
            waypoint += Point(1, 0) * distance
        elif instruction == 'W':
            waypoint += Point(-1, 0) * distance
        elif instruction == 'F':
            movement = (waypoint - position) * distance
            position += movement
            waypoint += movement
        elif instruction == 'R':
            waypoint = turn(waypoint, True, distance, position)
        elif instruction == 'L':
            waypoint = turn(waypoint, False, distance, position)
        else:
            raise ValueError(instruction)
    return position


_lines = read_input()
end = move_ship(Point(0, 0), Point(1, 0), _lines)
print(f'Part 1: {end.manhattan_distance(Point(0, 0))}')
end = move_ship2(Point(0, 0), Point(10, -1), _lines)
print(f'Part 2: {end.manhattan_distance(Point(0, 0))}')
