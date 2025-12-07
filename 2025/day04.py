import sys
sys.path.append('..')

from aoc.coord2d.point import Point
from aoc.input import read_input

_lines = read_input(True)
_lines = [list(iter(_line)) for _line in _lines]

def count_replace_neighbors(lines: list[list[str]]) -> int:
    accessable = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '@':
                continue
            pos = Point(x, y)
            neighbors = 0
            for neighbor in pos.get_all_neighbors():
                if neighbor.x >= 0 and neighbor.y >= 0 and neighbor.x < len(line) and neighbor.y < len(lines) and lines[neighbor.y][neighbor.x] == '@':
                    neighbors += 1
            if neighbors < 4:
                accessable.append(pos)
    for pos in accessable:
        lines[pos.y][pos.x] = '.'
    return len(accessable)


part1 = count_replace_neighbors(_lines)

print(f'Part 1: {part1}')

part2 = part1
while True:
    replaced = count_replace_neighbors(_lines)
    if replaced == 0:
        break
    part2 += replaced

print(f'Part 2: {part2}')

