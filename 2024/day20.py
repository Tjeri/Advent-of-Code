from aoc.coord2d.point import Point
from aoc.input import read_input


def parse_map(lines: list[str]) -> list[Point]:
    points: set[Point] = set()
    start, end = None, None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                start = Point(x, y)
            elif char == 'E':
                end = Point(x, y)
                points.add(end)
            elif char == '.':
                points.add(Point(x, y))
    result = [start]
    while result[-1] != end:
        for neighbor in result[-1].get_direct_neighbors():
            if neighbor in points:
                result.append(neighbor)
                points.remove(neighbor)
                continue
    return result


def find_cheats(path: list[Point], max_dist: int, min_save: int) -> int:
    save_index = min_save + 2
    found = 0
    for i, point in enumerate(path[:-save_index]):
        for diff_index, other in enumerate(path[i+save_index:]):
            dist = point.manhattan_distance(other)
            save = diff_index + save_index - dist
            if dist <= max_dist and save >= min_save:
                found += 1
    return found

_lines = read_input(True)
_path = parse_map(_lines)
print('Part 1:', find_cheats(_path, 2, 100))
print('Part 2:', find_cheats(_path, 20, 100))
