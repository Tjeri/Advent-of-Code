from aoc.input import read_input
from incode_computer import AsciiIntcodeComputer


class Springdroid:
    brain: AsciiIntcodeComputer

    def __init__(self, program: list[int]) -> None:
        self.brain = AsciiIntcodeComputer(program)

    def execute(self, instructions: list[str]) -> int:
        for instruction in instructions:
            self.brain.run(instruction)

        if self.brain.output[-1] > 255:
            return self.brain.output[-1]
        else:
            print(self.brain.str_output)
            return -1


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

_droid = Springdroid(_program)
script = [
    'NOT A J',
    'NOT C T',
    'OR T J',
    'AND D J',
    'WALK'
]
print(f'Part 1: {_droid.execute(script)}')

_droid = Springdroid(_program)
script = [
    'NOT H J',
    'OR C J',
    'AND B J',
    'AND A J',
    'NOT J J',
    'AND D J',
    'RUN'
]
print(f'Part 2: {_droid.execute(script)}')
