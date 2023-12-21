import numpy as np

from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input


def parse_map(lines: list[str]) -> tuple[Point, set[Point], Rect]:
    size = Rect(Point(0, 0), Point(0, 0))
    start = None
    plots = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            point = Point(x, y)
            size.update(point)
            if char == 'S':
                start = point
                plots.add(start)
            elif char == '.':
                plots.add(point)
    return start, plots, size


def count_plots(start: Point, plots: set[Point], size: Rect, max_steps: int = -1, wrap: bool = False) -> int:
    steps = 0
    mod = Point(size.width, size.height)
    if not wrap:
        start = start % mod
    done = {start}
    reachable = {start} if max_steps % 2 == 0 else set()
    to_check = [start]
    while to_check and steps < max_steps:
        steps += 1
        new_check = []
        for check in to_check:
            neighbors = check.get_direct_neighbors()
            for neighbor in neighbors:
                neighbor_mod = neighbor % mod if wrap else neighbor
                if neighbor not in done and neighbor_mod in plots:
                    done.add(neighbor)
                    new_check.append(neighbor)
        to_check = new_check
        if steps % 2 == max_steps % 2:
            reachable.update(to_check)
    return len(reachable)


def part2(start: Point, plots: set[Point], size: Rect, steps: int) -> int:
    x = [0, 1, 2]
    y = [count_plots(start, plots, size, i * size.width + size.middle.x, wrap=True) for i in x]
    target = (steps - size.middle.x) // size.width
    poly = np.rint(np.polynomial.polynomial.polyfit(x, y, 2))
    return int(sum(poly[i] * target ** i for i in x))


_lines = read_input(True)
_start, _plots, _size = parse_map(_lines)

print(f'Part 1: {count_plots(_start, _plots, _size, 64)}')
print(f'Part 2: {part2(_start, _plots, _size, 26_501_365)}')
