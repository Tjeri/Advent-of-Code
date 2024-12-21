from functools import cache

from aoc.coord2d.point import Point
from aoc.pathfinding2.a_star import dijkstra_all_shortest_paths
from aoc.input import read_input

keymap = {
    '7': Point(0, 0),
    '8': Point(1, 0),
    '9': Point(2, 0),
    '4': Point(0, 1),
    '5': Point(1, 1),
    '6': Point(2, 1),
    '1': Point(0, 2),
    '2': Point(1, 2),
    '3': Point(2, 2),
    '0': Point(1, 3),
    '^': Point(1, 3),
    'A': Point(2, 3),
    '<': Point(0, 4),
    'v': Point(1, 4),
    '>': Point(2, 4)
}
direction_to_str = {
    Point(1, 0): '>',
    Point(0, 1): 'v',
    Point(-1, 0): '<',
    Point(0, -1): '^'
}


def path_to_sequence(path: list[Point]) -> str:
    steps: list[str] = []
    last = path[0]
    for point in path[1:]:
        steps.append(direction_to_str[point - last])
        last = point
    return ''.join(steps) + 'A'


@cache
def find_paths(start: str, goal: str) -> list[str]:
    def get_neighbors(point: Point) -> dict[Point, int]:
        return {neighbor: 1 for neighbor in point.get_direct_neighbors() if neighbor in keymap.values()}

    if start == goal:
        return ['A']
    goal_point = keymap[goal]
    paths = dijkstra_all_shortest_paths(keymap[start], lambda x: x == goal_point, get_neighbors)[1]
    return list(map(path_to_sequence, paths))


@cache
def navigate(sequence: str, which: int, amount: int) -> int:
    result = 0
    last = 'A'
    for char in sequence:
        paths = find_paths(last, char)
        best = -1
        for path in paths:
            if which < amount:
                length = navigate(path, which + 1, amount)
            else:
                length = len(path)
            if best == -1 or length < best:
                best = length
        result += best
        last = char
    return result


_lines = read_input(True)
part1 = 0
part2 = 0
for _line in _lines:
    numeric_code = int(_line[:-1])
    part1 += navigate(_line, 0, 2) * numeric_code
    part2 += navigate(_line, 0, 25) * numeric_code
print('Part 1:', part1)
print('Part 2:', part2)
