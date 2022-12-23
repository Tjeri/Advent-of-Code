from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, IntEnum


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


class Square:
    top_left: Point
    bottom_right: Point
    size: int

    def __init__(self, tl_x, tl_y, size: int) -> None:
        self.top_left = Point(tl_x, tl_y)
        self.bottom_right = self.top_left + Point(size - 1, size - 1)
        self.size = size


class DieFace:
    id: int
    global_pos: Point
    size: int
    board: list[list[Tile]]
    neighbors: dict[Direction, tuple[DieFace, Direction]]

    def __init__(self, _id: int, base_square: Square, board: list[list[Tile]]) -> None:
        self.id = _id
        self.global_pos = base_square.top_left
        self.size = base_square.size
        self.board = board
        self.neighbors = dict()

    def get_start_position(self) -> Point:
        return Point(min(x for x, tile in enumerate(self.board[0]) if tile is Tile.Open), 0)

    def get_tile(self, position: Point) -> Tile:
        if self.is_oob(position):
            raise ValueError
        return self.board[position.y][position.x]

    def is_oob(self, position: Point) -> bool:
        return position.x < 0 or position.x >= self.size or position.y < 0 or position.y >= self.size

    def move(self, start: Point, direction: Direction) -> BoardPosition:
        next_position = start + direction.movement
        if self.is_oob(next_position):
            next_board_position = self.leave(next_position, direction)
            if next_board_position.is_valid():
                return next_board_position
            return BoardPosition(self, start, direction)
        return BoardPosition(self, next_position, direction)

    def enter(self, xy: int, from_: Direction) -> BoardPosition:
        facing = from_.turn_around()
        if facing is Direction.Right:
            return BoardPosition(self, Point(0, xy), facing)
        elif facing is Direction.Down:
            return BoardPosition(self, Point(xy, 0), facing)
        elif facing is Direction.Left:
            return BoardPosition(self, Point(self.size - 1, xy), facing)
        elif facing is Direction.Up:
            return BoardPosition(self, Point(xy, self.size - 1), facing)
        raise ValueError

    def leave(self, position: Point, direction: Direction) -> BoardPosition:
        neighbor, enter_from = self.neighbors[direction]
        xy = position.x if direction.is_vertical else position.y
        if direction is enter_from:
            xy = self.size - 1 - xy
        return neighbor.enter(xy, enter_from)


class Tile(Enum):
    Open = '.'
    Wall = '#'
    Nirvana = ' '


class Direction(IntEnum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3

    @property
    def is_vertical(self) -> bool:
        # noinspection PyTypeChecker
        return self.value % 2 == 1

    @property
    def movement(self) -> Point:
        if self is Direction.Right:
            return Point(1, 0)
        if self is Direction.Down:
            return Point(0, 1)
        if self is Direction.Left:
            return Point(-1, 0)
        if self is Direction.Up:
            return Point(0, -1)
        raise ValueError

    def turn(self, right: bool) -> Direction:
        # noinspection PyTypeChecker
        next_direction_id: int = self.value + (1 if right else -1)
        if next_direction_id < 0:
            next_direction_id = 3
        elif next_direction_id > 3:
            next_direction_id = 0
        return Direction(next_direction_id)

    def turn_around(self) -> Direction:
        return self.turn(True).turn(True)


D = Direction


@dataclass
class BoardPosition:
    die_face: DieFace
    position: Point
    direction: Direction

    @property
    def global_position(self) -> Point:
        return self.die_face.global_pos + self.position

    @property
    def score(self) -> int:
        # noinspection PyTypeChecker
        return 1000 * (self.die_face.global_pos.y + self.position.y + 1) \
            + 4 * (self.die_face.global_pos.x + self.position.x + 1) \
            + self.direction.value

    def is_valid(self) -> bool:
        return self.die_face.get_tile(self.position) is Tile.Open

    def move(self) -> BoardPosition:
        next_position = self.die_face.move(self.position, self.direction)
        if next_position.is_valid():
            return next_position
        return self

    def move_multi(self, steps: int) -> BoardPosition:
        pos = self
        for _ in range(steps):
            pos = pos.move()
        return pos

    def turn(self, right: bool) -> BoardPosition:
        return BoardPosition(self.die_face, self.position, self.direction.turn(right))


@dataclass
class DiceTransformation:
    size: int
    areas: list[Square]
    mapping: dict[int, dict[Direction, int]]


class DieBoard:
    faces: list[DieFace]
    position: BoardPosition

    def __init__(self, faces: list[DieFace], position: BoardPosition) -> None:
        self.faces = faces
        self.position = position

    @property
    def score(self) -> int:
        # noinspection PyTypeChecker
        return self.position.score

    def move(self, steps: int) -> None:
        self.position = self.position.move_multi(steps)

    def turn(self, right: bool) -> None:
        self.position = self.position.turn(right)

    def advance(self, movements: str) -> None:
        start = 0
        turn_pattern = re.compile('R|L')

        def read_next():
            if movements[start] in ('R', 'L'):
                return movements[start]
            result = turn_pattern.search(movements, start)
            if result is None:
                return movements[start:]
            return movements[start:result.start()]

        while start < len(movements):
            movement = read_next()
            start += len(movement)
            if movement == 'R':
                self.turn(True)
            elif movement == 'L':
                self.turn(False)
            else:
                self.move(int(movement))


class DieBoardBuilder:
    board: list[list[Tile]]

    def __init__(self) -> None:
        self.board = list()

    def add_row(self, line: str) -> None:
        self.board.append([Tile(char) for char in line])

    def build_board(self, face_area: list[Square],
                    face_mapping: dict[int, dict[Direction, tuple[int, Direction]]]) -> DieBoard:
        die_faces: list[DieFace] = [DieFace(i, square, self.get_board_square(square)) for i, square in
                                    enumerate(face_area)]
        for die_id, mapping in face_mapping.items():
            die_face = die_faces[die_id]
            for direction, neighbor in mapping.items():
                neighbor_id, neighbor_from = neighbor
                die_face.neighbors[direction] = (die_faces[neighbor_id], neighbor_from)
        return DieBoard(die_faces, BoardPosition(die_faces[0], die_faces[0].get_start_position(), Direction.Right))

    def get_board_square(self, square: Square) -> list[list[Tile]]:
        result = list()
        for y in range(square.top_left.y, square.bottom_right.y + 1):
            result.append(self.board[y][square.top_left.x:square.bottom_right.x + 1])
        return result


# path = '../data/2022/sample.txt'
path = '../data/2022/day22.txt'
# _face_areas = [Square(8, 0, 4), Square(0, 4, 4), Square(4, 4, 4), Square(8, 4, 4), Square(8, 8, 4), Square(12, 8, 4)]
_face_areas = [Square(50, 0, 50), Square(100, 0, 50), Square(50, 50, 50), Square(50, 100, 50), Square(0, 100, 50),
               Square(0, 150, 50)]
# _mapping_1 = {
#     0: {D.Right: (0, D.Left), D.Down: (3, D.Up), D.Left: (0, D.Right), D.Up: (4, Direction.Down)},
#     1: {D.Right: (2, D.Left), D.Down: (1, D.Up), D.Left: (3, D.Right), D.Up: (1, Direction.Down)},
#     2: {D.Right: (3, D.Left), D.Down: (2, D.Up), D.Left: (1, D.Right), D.Up: (2, Direction.Down)},
#     3: {D.Right: (1, D.Left), D.Down: (4, D.Up), D.Left: (2, D.Right), D.Up: (0, Direction.Down)},
#     4: {D.Right: (5, D.Left), D.Down: (0, D.Up), D.Left: (5, D.Right), D.Up: (3, Direction.Down)},
#     5: {D.Right: (4, D.Left), D.Down: (5, D.Up), D.Left: (4, D.Right), D.Up: (5, Direction.Down)},
# }
_mapping_1 = {
    0: {D.Right: (1, D.Left), D.Down: (2, D.Up), D.Left: (1, D.Right), D.Up: (3, Direction.Down)},
    1: {D.Right: (0, D.Left), D.Down: (1, D.Up), D.Left: (0, D.Right), D.Up: (1, Direction.Down)},
    2: {D.Right: (2, D.Left), D.Down: (3, D.Up), D.Left: (2, D.Right), D.Up: (0, Direction.Down)},
    3: {D.Right: (4, D.Left), D.Down: (0, D.Up), D.Left: (4, D.Right), D.Up: (2, Direction.Down)},
    4: {D.Right: (3, D.Left), D.Down: (5, D.Up), D.Left: (3, D.Right), D.Up: (5, Direction.Down)},
    5: {D.Right: (5, D.Left), D.Down: (4, D.Up), D.Left: (5, D.Right), D.Up: (4, Direction.Down)},
}
# _mapping_2 = {
#     0: {D.Right: (5, D.Right), D.Down: (3, D.Up), D.Left: (2, D.Up), D.Up: (1, D.Up)},
#     1: {D.Right: (2, D.Left), D.Down: (4, D.Down), D.Left: (5, D.Down), D.Up: (0, D.Up)},
#     2: {D.Right: (3, D.Left), D.Down: (4, D.Left), D.Left: (1, D.Right), D.Up: (0, D.Left)},
#     3: {D.Right: (5, D.Up), D.Down: (4, D.Up), D.Left: (2, D.Right), D.Up: (0, D.Down)},
#     4: {D.Right: (5, D.Left), D.Down: (1, D.Down), D.Left: (2, D.Down), D.Up: (3, D.Down)},
#     5: {D.Right: (0, D.Right), D.Down: (1, D.Left), D.Left: (4, D.Right), D.Up: (3, D.Right)},
# }
_mapping_2 = {
    0: {D.Right: (1, D.Left), D.Down: (2, D.Up), D.Left: (4, D.Left), D.Up: (5, D.Left)},
    1: {D.Right: (3, D.Right), D.Down: (2, D.Right), D.Left: (0, D.Right), D.Up: (5, D.Down)},
    2: {D.Right: (1, D.Down), D.Down: (3, D.Up), D.Left: (4, D.Up), D.Up: (0, D.Down)},
    3: {D.Right: (1, D.Right), D.Down: (5, D.Right), D.Left: (4, D.Right), D.Up: (2, D.Down)},
    4: {D.Right: (3, D.Left), D.Down: (5, D.Up), D.Left: (0, D.Left), D.Up: (2, D.Left)},
    5: {D.Right: (3, D.Down), D.Down: (1, D.Up), D.Left: (0, D.Up), D.Up: (4, D.Down)},
}
builder = DieBoardBuilder()
_die1: DieBoard
_die2: DieBoard
read_board = True
with open(path) as file:
    for _line in file.readlines():
        _line = _line.strip('\r\n')
        if not read_board:
            _die1 = builder.build_board(_face_areas, _mapping_1)
            _die1.advance(_line)
            _die2 = builder.build_board(_face_areas, _mapping_2)
            _die2.advance(_line)
        elif _line:
            builder.add_row(_line)
        else:
            read_board = False

print(f'Part 1: {_die1.score}')
print(f'Part 2: {_die2.score}')
