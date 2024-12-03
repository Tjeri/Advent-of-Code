import sys
sys.path.insert(0, '../aoc')

from aoc.input import read_input

_lines = read_input(True)
left = []
right = []
for line in _lines:
    _left, _right = line.split()
    left.append(int(_left))
    right.append(int(_right))
left.sort()
right.sort()
print('Part 1:', sum(map(lambda t: abs(t[0] - t[1]), zip(left, right))))

from collections import Counter
counter = Counter(right)
print('Part 2:', sum(map(lambda l: l * counter[l], left)))
