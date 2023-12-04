from aoc.input import read_input

from incode_computer import IntcodeComputer


class TractorBeamCalculator:
    program: list[int]

    first_x: dict[int, int]

    def __init__(self, program: list[int]) -> None:
        self.program = program
        self.first_x = {}

    def print_map(self, start_x: int, start_y: int, width: int, height: int) -> None:
        for y in range(start_y, start_y + height):
            line = ''
            for x in range(start_x, start_x + width):
                if self.is_affected(x, y):
                    line += '#'
                else:
                    line += '.'
            print(line)

    def is_affected(self, x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
        computer = IntcodeComputer(self.program)
        computer.run([x, y])
        return computer.output[-1] == 1

    def calculate_affected_points(self, size: int) -> int:
        affected_points = 0
        for y in range(size):
            for x in range(size):
                if self.is_affected(x, y):
                    affected_points += 1
        return affected_points

    def find_square(self, size: int) -> tuple[int, int]:
        size -= 1
        lower = 500
        upper = 2_000

        while lower + 1 < upper:
            y = (upper + lower) // 2
            x = self.find_last_x(y)
            if self.is_affected(x - size, y) and self.is_affected(x, y + size) and self.is_affected(x - size, y + size):
                upper = y
            else:
                lower = y

        x, y = self.find_last_x(upper) - size, upper

        for _y in range(y, y - 10, -1):
            for _x in range(x, x - 10, -1):
                if self.is_affected(_x, _y) \
                        and self.is_affected(_x + size, _y) \
                        and self.is_affected(_x, _y + size) \
                        and self.is_affected(_x + size, _y + size):
                    x, y = _x, _y
        return x, y

    def find_first_x(self, y: int) -> int:
        ys = list(self.first_x.keys())
        ys.sort()
        x = y // 2
        for i in range(len(ys)):
            if ys[i] > y:
                if i > 0:
                    x = self.first_x[ys[i - 1]]
                break

        while True:
            if self.is_affected(x, y):
                self.first_x[y] = x
                return x
            x += 1

    def find_last_x(self, y: int) -> int:
        lower = self.find_first_x(y)
        upper = lower + 1000

        while lower + 1 < upper:
            x = (upper + lower) // 2
            if self.is_affected(x, y):
                lower = x
            else:
                upper = x

        return lower


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]
_calculator = TractorBeamCalculator(_program)

print(f'Part 1: {_calculator.calculate_affected_points(50)}')

_x, _y = _calculator.find_square(100)
print(f'Part 2: {_x * 10_000 + _y}')
