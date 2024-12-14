import itertools
import operator
import re
from functools import reduce
import tkinter as tk

from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input


class Robot:
    def __init__(self, px, py, vx, vy) -> None:
        self.start = Point(px, py)
        self.move = Point(vx, vy)

    def pos_at(self, time: int) -> Point:
        return (self.start + time * self.move) % Point(width, height)


def get_robots(lines: list[str]) -> list[Robot]:
    result = []
    for line in lines:
        result.append(Robot(*map(int, pattern.match(line).groups())))
    return result

def part1() -> None:
    end_positions = []
    for robot in robots:
        end_positions.append(robot.pos_at(100))
    quadrants = [
        Rect(Point(0, 0), Point(width // 2 - 1, height // 2 - 1)),
        Rect(Point(width // 2 + 1, 0), Point(width, height // 2 - 1)),
        Rect(Point(0, height // 2 + 1), Point(width // 2 - 1, height)),
        Rect(Point(width // 2 + 1, height // 2 + 1), Point(width, height))
    ]
    amounts = [0] * 4
    for pos in end_positions:
        for i, quadrant in enumerate(quadrants):
            if pos in quadrant:
                amounts[i] += 1
                break
    print('Part 1:', reduce(operator.mul, amounts))

def part2() -> None:
    start = 6644
    step = 1000
    def loop():
        i = next(counter)
        canvas.delete('all')
        canvas.create_text(50, 25, justify=tk.CENTER, text=str(i), fill='white')
        for robot in robots:
            pos = robot.pos_at(i)
            canvas.create_rectangle(50 + pos.x, 50 + pos.y, 50 + pos.x, 50 + pos.y, outline='green')

    counter = itertools.count(start)
    top = tk.Tk()
    canvas = tk.Canvas(top, bg='black', height=100+height, width=100+width)
    canvas.pack()
    loop()
    top.mainloop()

real_input = True
pattern = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')
_lines = read_input(real_input)
width = 101 if real_input else 11
height = 103 if real_input else 7
robots = get_robots(_lines)

# part1()
part2()
