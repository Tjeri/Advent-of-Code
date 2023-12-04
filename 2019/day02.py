from incode_computer import IntcodeComputer
from aoc.input import read_input

_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

_part1 = IntcodeComputer(_program).replace(1, 12).replace(2, 2)
_part1.run()
print(f'Part 1: {_part1.memory[0]}')

for noun in range(0, 100):
    for verb in range(0, 100):
        _part2 = IntcodeComputer(_program).replace(1, noun).replace(2, verb)
        _part2.run()
        if _part2.memory[0] == 19690720:
            print(f'Part 2: {100 * noun + verb}')
            exit(0)
