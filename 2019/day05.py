from incode_computer import IntcodeComputer
from aoc.input import read_input

_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

_part1 = IntcodeComputer(_program)
_part1.run([1])
print(f'Part 1: {_part1.output[-1]}')

_part2 = IntcodeComputer(_program)
_part2.run([5])
print(f'Part 2: {_part2.output[0]}')
