from incode_computer import IntcodeComputer
from aoc.input import read_input

_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

part1 = IntcodeComputer(_program)
part1.run([1])
print(f'Part 1: {part1.output[0]}')

part2 = IntcodeComputer(_program)
part2.run([2])
print(f'Part 2: {part2.output[0]}')
