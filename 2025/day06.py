import sys
sys.path.append('..')

from aoc.input import read_input
from functools import reduce
import operator

_lines = read_input(True, strip_whitespace=False)
_numbers = [list(map(int, [_num for _num in _line.split(' ') if _num])) for _line in _lines[:-1]]
_symbols = [_symbol for _symbol in _lines[-1].split(' ') if _symbol]

part1 = 0
for i, _symbol in enumerate(_symbols):
    if _symbol == '+':
        part1 += sum(_num[i] for _num in _numbers)
    elif _symbol == '*':
        part1 += reduce(operator.mul, (_num[i] for _num in _numbers))

print(f'Part 1: {part1}')

part2 = 0
problem = 0
op = operator.add
for i in range(len(_lines[0])):
    num = reduce(operator.add, (_line[i] for _line in _lines[:-1]))
    if not num.strip():
        part2 += problem
        problem = 0
        op = operator.add
        continue
    problem = op(problem, int(num))
    if i >= len(_lines[-1]):
        continue
    _op = _lines[-1][i]
    if _op == '+':
        op = operator.add
    elif _op == '*':
        op = operator.mul
part2 += problem
print(f'Part 2: {part2}')



