import sys
sys.path.insert(0, '../aoc')

from itertools import combinations
from aoc.input import read_input

_lines = read_input(True)
height = len(_lines)
width = len(_lines[0])
nodes: dict[str, list[tuple[int, int]]] = dict()
for y, line in enumerate(_lines):
    for x, c in enumerate(line):
        if c == '.':
            continue
        nodes.setdefault(c, []).append((x, y))

antinodes: set[tuple[int, int]] = set()
for _nodes in nodes.values():
    for ((x1, y1), (x2, y2)) in combinations(_nodes, 2):
        dx = x1 - x2
        dy = y1 - y2
        x3 = x1 + dx
        y3 = y1 + dy
        x4 = x2 - dx
        y4 = y2 - dy
        if 0 <= x3 < width and 0 <= y3 < height:
            antinodes.add((x3, y3))
        if 0 <= x4 < width and 0 <= y4 < height:
            antinodes.add((x4, y4))
print('Part 1:', len(antinodes))

antinodes = set()
for _nodes in nodes.values():
    for ((x1, y1), (x2, y2)) in combinations(_nodes, 2):
        dx = x1 - x2
        dy = y1 - y2
        x3 = x1
        y3 = y1
        while 0 <= x3 < width and 0 <= y3 < height:
            antinodes.add((x3, y3))
            x3 += dx
            y3 += dy
        x3 = x1
        y3 = y1
        while 0 <= x3 < width and 0 <= y3 < height:
            antinodes.add((x3, y3))
            x3 -= dx
            y3 -= dy
print('Part 2:', len(antinodes))
