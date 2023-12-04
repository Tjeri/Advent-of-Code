from enum import IntEnum
from tkinter import Canvas, Tk

from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input
from incode_computer import IntcodeComputer


class Tile(IntEnum):
    Empty = 0
    Wall = 1
    Block = 2
    Paddle = 3
    Ball = 4

    def __str__(self) -> str:
        if self is Tile.Empty:
            return ' '
        if self is Tile.Wall:
            return 'X'
        if self is Tile.Block:
            return '#'
        if self is Tile.Paddle:
            return '_'
        if self is Tile.Ball:
            return '●'
        raise ValueError

    def draw(self, canvas: Canvas, x: int, y: int, size: int) -> None:
        if self is Tile.Wall:
            canvas.create_rectangle((x + 1) * size, (y + 1) * size, (x + 2) * size, (y + 2) * size, fill='black')
        elif self is Tile.Block:
            canvas.create_rectangle((x + 1) * size + 1, (y + 1.25) * size, (x + 2) * size - 1, (y + 1.75) * size, fill='grey')
        elif self is Tile.Paddle:
            canvas.create_rectangle((x + 1) * size + 1, (y + 1) * size, (x + 2) * size - 1, (y + 1.5) * size, fill='black')
        elif self is Tile.Ball:
            canvas.create_oval((x + 1) * size, (y + 1) * size, (x + 2) * size, (y + 2) * size, fill='red')


class JoystickPosition(IntEnum):
    Left = -1
    Neutral = 0
    Right = 1


class Game:
    computer: IntcodeComputer
    score: int = 0
    tiles: dict[Point, Tile]

    def __init__(self, _program: list[int]) -> None:
        self.computer = IntcodeComputer(_program).replace(0, 2)
        self.tiles = {}

    def __str__(self) -> str:
        area = Rect.from_size(Point(0, 0), 0, 0)
        for point in self.tiles:
            area.update(point)

        lines = []
        for y in range(area.top_left.y, area.bottom_right.y + 1):
            line = ''
            for x in range(area.top_left.x, area.bottom_right.x + 1):
                line += str(self.tiles.get(Point(x, y), Tile.Empty))
            lines.append(line)
        return f'Score: {self.score}\n' + '\n'.join(lines)

    def draw(self, canvas: Canvas | None) -> None:
        if canvas is None:
            return
        canvas.delete('all')
        for position, tile in self.tiles.items():
            tile.draw(canvas, position.x, position.y, 10)
        canvas.create_text(235, 15, text=f'Score: {self.score}', fill='white')
        canvas.update()

    def update_tiles(self) -> None:
        output = self.computer.output
        values = {Point(output[i], output[i + 1]): output[i + 2] for i in range(0, len(output), 3)}
        self.score = values.pop(Point(-1, 0), self.score)
        self.tiles.update({position: Tile(value) for position, value in values.items()})

        self.computer.output.clear()

    def run(self, animate: bool) -> None:
        window, canvas = None, None
        if animate:
            window = Tk()
            canvas = Canvas(window, bg='white', width=470, height=250)
            canvas.pack(fill='both', expand=True)
        self.computer.run()
        self.update_tiles()
        while not self.computer.state.finishing:
            self.draw(canvas)
            ball = self.get_position(Tile.Ball)
            paddle = self.get_position(Tile.Paddle)
            movement = JoystickPosition.Neutral
            if ball.x < paddle.x:
                movement = JoystickPosition.Left
            elif ball.x > paddle.x:
                movement = JoystickPosition.Right
            self.computer.run([movement])
            self.update_tiles()
        self.draw(canvas)
        if window:
            window.mainloop()

    def get_position(self, search_tile: Tile) -> Point:
        for position, tile in self.tiles.items():
            if tile == search_tile:
                return position
        raise RuntimeError


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

_computer = IntcodeComputer(_program)
_computer.run()

part1 = len([i for i, value in enumerate(_computer.output) if i % 3 == 2 and value == Tile.Block.value])
print(f'Part 1: {part1}')

_game = Game(_program)
_game.run(True)
print(f'Part 2: {_game.score}')
