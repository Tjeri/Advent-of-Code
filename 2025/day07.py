import sys
sys.path.append('..')

from aoc.input import read_input
from aoc.coord2d.point import Point

_lines = read_input(False)

start = None
splitters = set()
for y, line in enumerate(_lines):
    for x, char in enumerate(line):
        if char == 'S':
            start = Point(x, y)
        elif char == '^':
            splitters.add(Point(x, y))

beams = {start,}
splitters_used = set()
while beams:
    pos = beams.pop() + Point(0, 1)
    if pos in splitters:
        beams.add(pos + Point(1, 0))
        beams.add(pos + Point(-1, 0))
        splitters_used.add(pos)
    elif pos.y < len(_lines):
        beams.add(pos)
print(f'Part 1: {len(splitters_used)}')

positions = {start: 1}
particles = [start]
split = 1
while particles:
    particle = particles.pop()
    amount = positions[particle]
    pos = particle + Point(0, 1)
    if pos in splitters:
        print('split at ' , pos , ' with ' , amount)
        split += amount
        _next = pos + Point(1, 0)
        if _next not in positions:
            particles.append(_next)
        positions[_next] = positions.get(_next, 0) + amount

        _next = pos + Point(-1, 0)
        if _next not in positions:
            particles.append(_next)
        positions[_next] = positions.get(_next, 0) + amount
    elif pos.y < len(_lines):
        particles.append(pos)
        positions[pos] = amount
print(f'Part 2: {split}')
print(positions)
