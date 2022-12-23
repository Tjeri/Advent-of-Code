from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self) -> int:
        return hash(f'{self.x}/{self.y}')


@dataclass
class Rect:
    top_left: Point
    bottom_right: Point

    @property
    def width(self) -> int:
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> int:
        return self.bottom_right.y - self.top_left.y

    def update(self, point: Point) -> None:
        if point.x < self.top_left.x:
            self.top_left.x = point.x
        if point.y < self.top_left.y:
            self.top_left.y = point.y
        if point.x > self.bottom_right.x:
            self.bottom_right.x = point.x
        if point.y > self.bottom_right.y:
            self.bottom_right.y = point.y


class Tile(Enum):
    Elf = '#'
    Ground = '.'


class Direction(Enum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()

    NE = auto()
    SE = auto()
    SW = auto()
    NW = auto()

    @property
    def movement(self) -> Point:
        if self is Direction.N:
            return Point(0, -1)
        if self is Direction.E:
            return Point(1, 0)
        if self is Direction.S:
            return Point(0, 1)
        if self is Direction.W:
            return Point(-1, 0)
        if self is Direction.NE:
            return Point(1, -1)
        if self is Direction.SE:
            return Point(1, 1)
        if self is Direction.SW:
            return Point(-1, 1)
        if self is Direction.NW:
            return Point(-1, -1)
        raise ValueError

    def to_check(self) -> list[Direction]:
        if self is Direction.N:
            return [D.N, D.NE, D.NW]
        if self is Direction.E:
            return [D.E, D.NE, D.SE]
        if self is Direction.S:
            return [D.S, D.SE, D.SW]
        if self is Direction.W:
            return [D.W, D.SW, D.NW]
        raise ValueError


D = Direction


class Grove:
    elves: set[Point]
    order: list[Direction]

    def __init__(self) -> None:
        self.elves = set()
        self.order = [D.N, D.S, D.W, D.E]

    def __str__(self) -> str:
        result = ''
        rect = self.get_elf_rect()
        for y in range(rect.top_left.y, rect.bottom_right.y + 1):
            row = ''
            for x in range(rect.top_left.x, rect.bottom_right.x + 1):
                if Point(x, y) in self.elves:
                    row += '#'
                else:
                    row += '.'
            result += row + '\n'
        return result

    def get_elf_rect(self) -> Rect:
        rect = Rect(Point(75, 75), Point(0, 0))
        for position in self.elves:
            rect.update(position)
        return rect

    def count_elf_contained_ground_tiles(self) -> int:
        rect = self.get_elf_rect()
        ground = 0
        for y in range(rect.top_left.y, rect.bottom_right.y + 1):
            for x in range(rect.top_left.x, rect.bottom_right.x + 1):
                if Point(x, y) not in self.elves:
                    ground += 1
        return ground

    def add_row(self, line: str, y: int) -> None:
        for x, char in enumerate(line):
            if char == '#':
                self.elves.add(Point(x, y))

    def simulate(self) -> None:
        i = 1
        while self.simulate_round():
            if i == 10:
                print(f'Part 1: {self.count_elf_contained_ground_tiles()}')
            i += 1
        print(f'Part 2: {i}')

    def simulate_round(self) -> bool:
        movements = self.collect_movements()
        if not movements:
            return False
        for _from, _to in movements.items():
            self.elves.remove(_from)
            self.elves.add(_to)
        self.order.append(self.order.pop(0))
        return True

    def collect_movements(self) -> dict[Point, Point]:
        movements: dict[Point, Point] = dict()
        proposed: dict[Point, Point] = dict()
        blocked: set[Point] = set()
        for position in self.elves:
            if not self.wants_to_move(position):
                continue
            for direction in self.order:
                if not self.check_can_move(position, direction):
                    continue
                move = position + direction.movement
                if move in blocked:
                    continue
                if move in proposed:
                    blocked.add(move)
                    move_from = proposed.pop(move)
                    movements.pop(move_from)
                else:
                    proposed[move] = position
                    movements[position] = move
                break
        return movements

    def wants_to_move(self, position: Point) -> bool:
        for direction in Direction:
            if position + direction.movement in self.elves:
                return True
        return False

    def check_can_move(self, position: Point, direction: Direction) -> bool:
        for _direction in direction.to_check():
            if position + _direction.movement in self.elves:
                return False
        return True


board = Grove()
with open('../data/2022/day23.txt') as file:
    for _i, _line in enumerate(file.readlines()):
        board.add_row(_line.strip(), _i)

board.simulate()
