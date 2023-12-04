from __future__ import annotations

from enum import IntEnum

from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input
from incode_computer import IntcodeComputer


class Direction(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

    @property
    def vector(self) -> Point:
        if self is Direction.Up:
            return Point(0, -1)
        if self is Direction.Right:
            return Point(1, 0)
        if self is Direction.Down:
            return Point(0, 1)
        if self is Direction.Left:
            return Point(-1, 0)
        raise ValueError(f'Invalid Direction: {self}')

    def turn_right(self) -> Direction:
        return Direction((self.value + 1) % 4)

    def turn_left(self) -> Direction:
        return Direction((self.value - 1) % 4)


class Color(IntEnum):
    Black = 0
    White = 1


class Robot:
    brain: IntcodeComputer
    panels: dict[Point, Color]
    position: Point
    direction: Direction

    def __init__(self, program: list[int], initial_color: Color) -> None:
        self.brain = IntcodeComputer(program)
        self.panels = {Point(0, 0): initial_color}
        self.position = Point(0, 0)
        self.direction = Direction.Up

    def __str__(self) -> str:
        points = [point for point, color in self.panels.items() if color is Color.White]

        area = Rect.from_size(points[0], 0, 0)
        for point in points[1:]:
            area.update(point)

        lines = []
        for y in range(area.top_left.y, area.bottom_right.y + 1):
            line = ''
            for x in range(area.top_left.x, area.bottom_right.x + 1):
                if self.panels.get(Point(x, y), Color.Black) is Color.White:
                    line += '█'
                else:
                    line += ' '
            lines.append(line)
        return '\n'.join(lines)

    def run(self) -> None:
        while not self.brain.state.finishing:
            self.brain.run([self.panels.get(self.position, Color.Black).value])
            paint, turn = self.brain.output[-2:]
            self.panels[self.position] = Color(paint)
            if turn == 0:
                self.direction = self.direction.turn_left()
            elif turn == 1:
                self.direction = self.direction.turn_right()
            else:
                raise ValueError(f'Invalid turn signal: {turn}')
            self.position = self.position + self.direction.vector


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

_robot = Robot(_program, Color.Black)
_robot.run()
print(f'Part 1: {len(_robot.panels)}')

_robot2 = Robot(_program, Color.White)
_robot2.run()
print(f'Part 2:\n{_robot2}')
