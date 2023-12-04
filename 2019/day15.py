from __future__ import annotations

from enum import IntEnum

from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input
from aoc.pathfinding.bfs import breadth_first_search, Graph, Node, T
from incode_computer import IntcodeComputer


class Direction(IntEnum):
    North = 1
    South = 2
    West = 3
    East = 4

    @property
    def back(self) -> Direction:
        if self is Direction.North:
            return Direction.South
        if self is Direction.South:
            return Direction.North
        if self is Direction.West:
            return Direction.East
        if self is Direction.East:
            return Direction.West

    @property
    def vector(self) -> Point:
        if self is Direction.North:
            return Point(0, -1)
        if self is Direction.South:
            return Point(0, 1)
        if self is Direction.West:
            return Point(1, 0)
        if self is Direction.East:
            return Point(-1, 0)


class Tile(IntEnum):
    Empty = -1
    Wall = 0
    Ground = 1
    OxygenSystem = 2

    def __str__(self) -> str:
        if self is Tile.Empty:
            return ' '
        if self is Tile.Wall:
            return '█'
        if self is Tile.Ground:
            return ' '
        if self is Tile.OxygenSystem:
            return 'X'


class PointNode(Node):
    position: Point

    def __init__(self, position: Point) -> None:
        self.position = position

    def __hash__(self) -> int:
        return hash(self.position)


class Droid(Graph[PointNode]):
    brain: IntcodeComputer

    map: dict[Point, Tile]
    nodes: dict[Point, PointNode]

    def __init__(self, program: list[int]) -> None:
        self.brain = IntcodeComputer(program)
        self.map = {}
        self.nodes = {}

    def __str__(self) -> str:
        area = Rect.from_size(Point(0, 0), 0, 0)
        for point in self.map:
            area.update(point)

        lines = []
        path = {node.position for node in breadth_first_search(self).build_path()}
        for y in range(area.top_left.y, area.bottom_right.y + 1):
            line = ''
            for x in range(area.top_left.x, area.bottom_right.x + 1):
                tile = self.map.get(Point(x, y), Tile.Empty)
                if x == 0 and y == 0:
                    line += 'o'
                elif tile is Tile.OxygenSystem:
                    line += str(tile)
                elif Point(x, y) in path:
                    line += '●'
                else:
                    line += str(tile)
            lines.append(line)
        return '\n'.join(lines)

    def get_root(self) -> PointNode:
        return self.nodes.setdefault(Point(0, 0), PointNode(Point(0, 0)))

    def get_goal(self) -> PointNode:
        for position, tile in self.map.items():
            if tile is Tile.OxygenSystem:
                return self.nodes.setdefault(position, PointNode(position))
        raise RuntimeError('No Goal found.')

    def is_goal(self, node: PointNode) -> bool:
        return self.map.get(node.position, Tile.Empty) is Tile.OxygenSystem

    def get_edges(self, node: PointNode) -> list[PointNode]:
        edges = []
        for direction in Direction:
            point = node.position + direction.vector
            tile = self.map.get(point, Tile.Empty)
            if tile in (Tile.Empty, Tile.Wall):
                continue
            edges.append(self.nodes.setdefault(point, PointNode(point)))
        return edges

    def explore(self, position: Point = Point(0, 0), from_direction: Direction | None = None) -> None:
        for direction in Direction:
            if direction is from_direction:
                continue
            next_position = position + direction.vector
            if next_position in self.map:
                continue
            self.brain.run([direction])
            tile = Tile(self.brain.output[-1])
            self.map[next_position] = tile
            if tile is not Tile.Wall:
                self.explore(next_position, direction.back)
                self.brain.run([direction.back])

    def fill_with_oxygen(self) -> int:
        minute = 0
        goal = self.get_goal()
        explored = {goal}
        queue = [goal]
        next_queue = set()
        while queue:
            minute += 1
            for node in queue:
                for edge in self.get_edges(node):
                    if edge in explored:
                        continue
                    explored.add(edge)
                    next_queue.add(edge)
            queue = list(next_queue)
            next_queue.clear()
        return minute - 1


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

_droid = Droid(_program)
_droid.explore()
print(f'Part 1: {len(breadth_first_search(_droid).build_path()) - 1}')
print(f'Part 2: {_droid.fill_with_oxygen()}')
