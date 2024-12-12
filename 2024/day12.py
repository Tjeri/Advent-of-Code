from aoc.coord2d.point import Point
from aoc.input import read_input


def calc_region(point: Point, seen: set[Point] | None = None) -> tuple[int, set[tuple[Point, Point]]]:
    if seen is None:
        seen = {point}
    else:
        seen.add(point)
    ptype = plots[point]
    area = 1
    perimeter: set[tuple[Point, Point]] = set()
    for neighbor in point.get_direct_neighbors():
        if neighbor in seen:
            continue
        if neighbor in plots and plots[neighbor] == ptype:
            _area, _perimeter = calc_region(neighbor, seen)
            area += _area
            perimeter.update(_perimeter)
        else:
            perimeter.add((neighbor, neighbor - point))
    plots.pop(point)
    return area, perimeter


def calc_sides(perimeter: set[tuple[Point, Point]]) -> int:
    sides = 0
    while perimeter:
        connected = [perimeter.pop()]
        while connected:
            side, direction = connected.pop(0)
            found = []
            for point, _direction in perimeter:
                if point in connected or direction != _direction:
                    continue
                if point.manhattan_distance(side) == 1:
                    found.append((point, _direction))
            connected += found
            perimeter.difference_update(found)
        sides += 1
    return sides


_lines = read_input(True)
width, height = len(_lines), len(_lines[0])
plots = {}
for y, line in enumerate(_lines):
    for x, char in enumerate(line):
        plots[Point(x, y)] = char

part1 = 0
part2 = 0
for y in range(height):
    for x in range(width):
        pos = Point(x, y)
        if pos in plots:
            a, p = calc_region(pos)
            part1 += a * len(p)
            part2 += a * calc_sides(p)
print('Part 1:', part1)
print('Part 2:', part2)
