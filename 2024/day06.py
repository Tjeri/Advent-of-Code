import sys
sys.path.insert(0, '../aoc')

from aoc.input import read_input
from enum import Enum

class Direction(Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)

    def next(self):
        if self == Direction.North:
            return Direction.East
        elif self == Direction.East:
            return Direction.South
        elif self == Direction.South:
            return Direction.West
        elif self == Direction.West:
            return Direction.North

_lines = read_input(True)
height = len(_lines)
width = len(_lines[0])
walls = set()
for y, line in enumerate(_lines):
    for x, c in enumerate(line):
        if c == '#':
            walls.add((x, y))
        elif c == '^':
            guard = (x, y)

def find_visited_or_loop(extra_walls):
    g = guard
    visited = set()
    visited.add(g)
    vd = dict()
    gd = Direction.North
    obstacles = 0
    while True:
        _next = (g[0] + gd.value[0], g[1] + gd.value[1])
        if _next in walls or _next in extra_walls:
            gd = gd.next()
            continue
        if _next[0] < 0 or _next[1] < 0 or _next[0] >= width or _next[1] >= height:
            break
        g = _next
        if gd in vd.setdefault(g, set()):
            return set()
        visited.add(g)
        vd[g].add(gd)
    return visited

_visited = find_visited_or_loop(set())
print('Part 1', len(_visited))

loops = 0
for _v in _visited:
    if _v == guard:
        continue
    _vv = find_visited_or_loop({_v})
    if len(_vv) == 0:
        loops += 1
print('Part 2', loops)
