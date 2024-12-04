import sys
sys.path.insert(0, '../aoc')

from aoc.input import read_input

def find_x(x, y):
    if _lines[y][x] != 'X':
        return 0
    found = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if find_mas(x, y, dx, dy):
                found += 1
    return found

def find_mas(x, y, dx, dy):
    if x + 3 * dx < 0 or x + 3 * dx >= len(_lines[0]) or y + 3 * dy < 0 or y + 3 * dy >= len(_lines):
        return False
    return _lines[y + dy][x + dx] == 'M' and _lines[y + 2 * dy][x + 2 * dx] == 'A' and _lines[y + 3 * dy][x + 3 * dx] == 'S'

def find_a(x, y):
    if _lines[y][x] != 'A':
        return 0
    tl = get(x - 1, y - 1)
    br = get(x + 1, y + 1)
    if tl == 'M' and br == 'S' or tl == 'S' and br == 'M':
        tr = get(x + 1, y - 1)
        bl = get(x - 1, y + 1)
        if tr == 'M' and bl == 'S' or tr == 'S' and bl == 'M':
            return 1
    return 0

def get(x, y):
    if y < 0 or x < 0 or y >= len(_lines) or x >= len(_lines[0]):
        return None
    return _lines[y][x]

_lines = read_input(True)

part1 = 0
for _y in range(len(_lines)):
    for _x in range(len(_lines[0])):
        part1 += find_x(_x, _y)
print('Part 1:', part1)

part2 = 0

for _y in range(len(_lines)):
    for _x in range(len(_lines[0])):
        part2 += find_a(_x, _y)

print('Part 2:', part2)
