import sys
sys.path.insert(0, '../aoc')

from aoc.input import read_input

def check_possible(t: int, eq: list[int]) -> bool:
    if len(eq) == 1:
        return t == eq[0]
    if check_possible(t, [eq[0] * eq[1]] + eq[2:]):
        return True
    return check_possible(t, [eq[0] + eq[1]] + eq[2:])

def check_possible2(t: int, eq: list[int]) -> bool:
    if len(eq) == 1:
        return t == eq[0]
    if check_possible2(t, [eq[0] * eq[1]] + eq[2:]):
        return True
    if check_possible2(t, [eq[0] + eq[1]] + eq[2:]):
        return True
    return check_possible2(t, [int(str(eq[0]) + str(eq[1]))] + eq[2:])

_lines = read_input(False)

part1 = 0
for line in _lines:
    test, equation = line.split(':')
    if check_possible(int(test), list(map(int, equation.strip().split(' ')))):
        part1 += int(test)
print('Part 1:', part1)

part2 = 0
for line in _lines:
    test, equation = line.split(':')
    if check_possible2(int(test), list(map(int, equation.strip().split(' ')))):
        part2 += int(test)
print('Part 2:', part2)
