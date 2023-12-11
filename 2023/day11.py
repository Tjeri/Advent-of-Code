from aoc.coord2d.point import Point
from aoc.input import read_input


def get_x_offsets(lines: list[str]) -> dict[int, int]:
    x_offsets = {}
    offset = 0
    for x in range(len(lines[0])):
        for y, line in enumerate(lines):
            if line[x] == '#':
                x_offsets[x] = offset
                break
        else:
            offset += 1
    return x_offsets


def get_y_offsets(lines: list[str]) -> dict[int, int]:
    y_offsets = {}
    offset = 0
    for y, line in enumerate(lines):
        if '#' not in line:
            offset += 1
        else:
            y_offsets[y] = offset
    return y_offsets


def parse_coords(lines: list[str], offset_size: int = 1) -> list[Point]:
    x_offsets = get_x_offsets(lines)
    y_offsets = get_y_offsets(lines)
    result = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                result.append(Point(x + offset_size * x_offsets[x], y + offset_size * y_offsets[y]))
    return result


def calc_distances(galaxies: list[Point]) -> int:
    result = 0
    for i, galaxy1 in enumerate(galaxies[:-1]):
        for galaxy2 in galaxies[i + 1:]:
            result += galaxy1.manhattan_distance(galaxy2)
    return result


_lines = read_input(True)
print(f'Part 1: {calc_distances(parse_coords(_lines))}')
print(f'Part 2: {calc_distances(parse_coords(_lines, 999_999))}')
