import sys
sys.path.append('..')

from aoc.input import read_input

_lines = read_input(True)
pos = 50

part1 = 0
part2 = 0
for _line in _lines:
    modifier = 1 if _line[0] == 'R' else -1
    number = int(_line[1:])
    step = modifier * (number % 100)
    if number >= 100:
        part2 += number // 100
    pos += step
    if pos > 100:
        part2 += 1
    elif pos < 0 and pos > step:
        part2 += 1
    pos %= 100
    if pos == 0:
        part1 += 1
        part2 += 1

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
