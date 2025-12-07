import sys
sys.path.append('..')

from aoc.input import read_input

_lines = read_input(True)
_ranges = _lines[0].split(',')

part1 = 0
part2 = 0
for _range in _ranges:
    start, end = map(int, _range.split('-'))
    for i in range(start, end + 1):
        number = str(i)
        if len(number) % 2 == 0:
            mid = len(number) // 2
            if number[:mid] == number[mid:]:
                part1 += i
        for j in range(1, len(number) // 2 + 1):
            if len(number) % j == 0:
                ref = number[:j]
                for k in range(j, len(number), j):
                    if number[k:k+j] != ref:
                        break
                else:
                    part2 += i
                    break

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
