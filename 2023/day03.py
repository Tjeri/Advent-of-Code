from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input

digits = {str(d) for d in range(10)}
symbols = {'@', '*', '=', '&', '#', '$', '-', '%', '+', '/'}
gear = '*'


class Schematic:
    points: dict[Point, str]
    size: Rect
    numbers: dict[Point, int]
    gears: list[Point]

    def __init__(self, lines: list[str]) -> None:
        self.points = dict()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                self.points[Point(x, y)] = c
        self.size = Rect(Point(0, 0), Point(x, y))
        self.numbers = dict()
        self.gears = list()
        self.parse()

    def parse(self) -> None:
        for y in range(self.size.top_left.y, self.size.bottom_right.y + 1):
            number = 0
            number_start = None
            for x in range(self.size.top_left.y, self.size.bottom_right.x + 1):
                point = Point(x, y)
                if (c := self.points.get(point, '.')) in digits:
                    number = number * 10 + int(c)
                    if not number_start:
                        number_start = Point(x, y)
                else:
                    if number:
                        if self.is_part_number(number, number_start):
                            self.numbers[number_start] = number
                        number = 0
                        number_start = None
                    if c == gear:
                        self.gears.append(point)

            if number and self.is_part_number(number, number_start):
                self.numbers[number_start] = number

    def is_part_number(self, number: int, pos: Point) -> bool:
        for y1 in range(pos.y - 1, pos.y + 2):
            for x1 in range(pos.x - 1, pos.x + len(str(number)) + 1):
                c = self.points.get(Point(x1, y1), '.')
                if c in symbols:
                    return True
        return False

    def get_surrounding_numbers(self, pos: Point) -> list[int]:
        numbers = []
        for y in range(pos.y - 1, pos.y + 2):
            found = False
            for x in range(pos.x - 1, pos.x + 2):
                point = Point(x, y)
                c = self.points.get(point, '.')
                if c in digits:
                    if not found:
                        numbers.append(self.get_number(point))
                        found = True
                else:
                    found = False
        return numbers

    def get_number(self, pos: Point) -> int:
        number = self.numbers.get(pos)
        for x in range(pos.x - 1, -1, -1):
            number = self.numbers.get(Point(x, pos.y), number)
            if number:
                break
        return number


def part2() -> int:
    result = 0
    for gear in schematic.gears:
        numbers = schematic.get_surrounding_numbers(gear)
        if len(numbers) == 2:
            result += numbers[0] * numbers[1]
    return result


_lines = read_input(True)
schematic = Schematic(_lines)
print(f'Part 1: {sum(number for _, number in schematic.numbers.items())}')
print(f'Part 1: {part2()}')
