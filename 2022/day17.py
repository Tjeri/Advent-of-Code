import math
from enum import Enum
from typing import Any

from aoc.coord2d.point import Point


class Stone(Enum):
    HorizontalLine = [1 + 2 + 4 + 8]
    Cross = [2, 1 + 2 + 4, 2]
    Corner = [1 + 2 + 4, 4, 4]
    VerticalLine = [1, 1, 1, 1]
    Block = [1 + 2, 1 + 2]

    @property
    def width(self) -> int:
        return int(math.log2(max(self.value) + 1))

    @property
    def height(self) -> int:
        return len(self.value)

    def __getitem__(self, item: Any) -> int:
        ...


class Field:
    stones: list[Stone] = [Stone.HorizontalLine, Stone.Cross, Stone.Corner, Stone.VerticalLine, Stone.Block]
    stone_id: int = -1
    jets: list[bool]
    jet_id: int = -1

    blocked: list[int]
    width: int = 7
    height: int = 0
    current_stone: Stone
    current_pos: Point

    seen: set[str]
    heights: dict[str, tuple[int, int]]

    def __init__(self, jet_pattern: str) -> None:
        self.jets = [jet == '>' for jet in jet_pattern]
        self.blocked = list()
        self.seen = set()
        self.heights = dict()

    def __str__(self) -> str:
        result = ''
        for row in reversed(field.blocked):
            line = ''
            for blocked in range(7):
                if row & pow(2, blocked):
                    line += '#'
                else:
                    line += '.'
            result += line + '\n'
        return result

    def reset(self) -> None:
        self.stone_id = -1
        self.jet_id = -1
        self.blocked = list()
        self.height = 0
        self.seen = set()
        self.heights = dict()

    def get_current_id(self) -> str:
        return f'{self.stone_id}-{self.jet_id}'

    def simulate(self, stones: int) -> None:
        start_i = 0
        for i in range(stones):
            self.spawn_stone()
            while self.move_stone():
                pass
            self.settle_stone()
            _id = self.get_current_id()
            if _id in self.seen:
                if _id in self.heights:
                    index2, height2 = self.heights[_id]
                    loop_length = i - index2
                    loop_height = self.height - height2
                    loops, remainder = divmod(stones - i, loop_length)
                    self.height += loops * loop_height
                    start_i = stones - remainder
                    break
                self.heights[_id] = (i, self.height)
            self.seen.add(_id)
        if start_i == 0:
            return
        for i in range(start_i, stones):
            self.spawn_stone()
            while self.move_stone():
                pass
            self.settle_stone()

    def spawn_stone(self) -> None:
        self.stone_id += 1
        if self.stone_id == len(self.stones):
            self.stone_id = 0
        self.current_stone = self.stones[self.stone_id]
        self.current_pos = Point(2, len(self.blocked) + 3)

    def move_stone(self) -> bool:
        self.jet_id += 1
        if self.jet_id == len(self.jets):
            self.jet_id = 0
        move = 1 if self.jets[self.jet_id] else -1
        if self.check_stone_fits(Point(self.current_pos.x + move, self.current_pos.y)):
            self.current_pos.x += move
        if self.check_stone_fits(Point(self.current_pos.x, self.current_pos.y - 1)):
            self.current_pos.y -= 1
            return True
        return False

    def check_stone_fits(self, pos: Point) -> bool:
        if pos.x < 0 or pos.x + self.current_stone.width > self.width:
            return False
        for _y in range(self.current_stone.height):
            y = pos.y + _y
            if y >= len(self.blocked):
                return True
            if y < 0:
                return False
            if self.current_stone.value[_y] << pos.x & self.blocked[y]:
                return False
        return True

    def settle_stone(self) -> None:
        for i in range(self.current_stone.height):
            y = self.current_pos.y + i
            if y >= len(self.blocked):
                self.blocked.append(self.current_stone.value[i] << self.current_pos.x)
                self.height += 1
            else:
                self.blocked[y] |= self.current_stone.value[i] << self.current_pos.x


with open('../data/2022/day17.txt') as file:
    field = Field(file.readline().strip())

field.simulate(2022)
print(f'Part 1: {field.height}')
field.reset()
field.simulate(1_000_000_000_000)
print(f'Part 2: {field.height - 1}')
