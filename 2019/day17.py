from aoc.input import read_input
from incode_computer import AsciiIntcodeComputer


class VacuumRobot:
    brain: AsciiIntcodeComputer

    def __init__(self, program: list[int], active: bool = False) -> None:
        self.brain = AsciiIntcodeComputer(program)
        if active:
            self.brain.replace(0, 2)
        self.brain.run()

    def __str__(self) -> str:
        return self.brain.str_output

    def add_input(self, str_input: str) -> None:
        self.brain.run(str_input)

    @property
    def alignment_parameter_sum(self) -> int:
        result = 0
        image = str(self).split('\n')
        for y in range(1, len(image) - 1):
            line = image[y]
            for x in range(1, len(line) - 1):
                if line[x] == '#' \
                        and line[x - 1] == '#' and line[x + 1] == '#' \
                        and image[y - 1][x] == '#' and image[y + 1][x] == '#':
                    result += x * y
        return result


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]
_robot = VacuumRobot(_program)
print(f'Part 1: {_robot.alignment_parameter_sum}')

# print(_robot)
path = 'R,12,L,8,R,12,' \
       'R,8,R,6,R,6,R,8,' \
       'R,12,L,8,R,12,' \
       'R,8,R,6,R,6,R,8,' \
       'R,8,L,8,R,8,R,4,R,4,' \
       'R,8,L,8,R,8,R,4,R,4,' \
       'R,8,R,6,R,6,R,8,' \
       'R,8,L,8,R,8,R,4,R,4,' \
       'R,8,R,6,R,6,R,8,' \
       'R,12,L,8,R,12'
subroutine_A = 'R,12,L,8,R,12'
subroutine_B = 'R,8,R,6,R,6,R,8'
subroutine_C = 'R,8,L,8,R,8,R,4,R,4'
mainroutine = 'A,B,A,B,C,C,B,C,B,A'
_robot2 = VacuumRobot(_program, True)
_robot2.add_input(mainroutine)
_robot2.add_input(subroutine_A)
_robot2.add_input(subroutine_B)
_robot2.add_input(subroutine_C)
_robot2.add_input('n')
print(f'Part 2: {_robot2.brain.output[-1]}')
