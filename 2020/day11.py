from enum import Enum

from aoc.coord2d.point import Point
from aoc.input import read_input


class State(Enum):
    Floor = '.'
    Empty = 'L'
    Occupied = '#'


class Game:
    seats: dict[Point, State]
    width: int
    height: int
    allowed_neighbors: int = 3

    def __init__(self, lines: list[str]) -> None:
        self.seats = dict()
        self.width = len(lines[0])
        self.height = len(lines)
        for y in range(self.height):
            for x in range(self.width):
                state = State(lines[y][x])
                if state is not State.Floor:
                    self.seats[Point(x, y)] = state

    @property
    def occupied(self) -> int:
        return len([s for s in self.seats.values() if s is State.Occupied])

    def simulate(self) -> None:
        copy = None
        while copy != self.seats:
            copy = self.seats
            self.advance_state()

    def advance_state(self) -> None:
        new_seats = dict()
        for position, state in self.seats.items():
            occupied_neighbors = self.count_occupied_neighbors(position)
            if state is State.Empty and not occupied_neighbors:
                new_seats[position] = State.Occupied
            elif state is State.Occupied and occupied_neighbors > self.allowed_neighbors:
                new_seats[position] = State.Empty
            else:
                new_seats[position] = state
        self.seats = new_seats

    def count_occupied_neighbors(self, position: Point) -> int:
        neighbors = position.get_all_neighbors()
        return len([neighbor for neighbor in neighbors if self.is_neighbor_occupied(position, neighbor)])

    def is_neighbor_occupied(self, position: Point, neighbor: Point) -> bool:
        return self.seats.get(neighbor, State.Empty) is State.Occupied


class Game2(Game):
    allowed_neighbors = 4

    def is_neighbor_occupied(self, position: Point, neighbor: Point) -> bool:
        if self.is_oob(neighbor):
            return False
        if neighbor in self.seats:
            return self.seats[neighbor] is State.Occupied
        next_neighbor = neighbor + (neighbor - position)
        return self.is_neighbor_occupied(neighbor, next_neighbor)

    def is_oob(self, point: Point) -> bool:
        return point.x < 0 or point.x >= self.width or point.y < 0 or point.y >= self.height


_lines = read_input()
game = Game(_lines)
game.simulate()
print(f'Part 1: {game.occupied}')
game2 = Game2(_lines)
game2.simulate()
print(f'Part 2: {game2.occupied}')
