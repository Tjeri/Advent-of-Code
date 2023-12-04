from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input
from aoc.pathfinding.bfs import bfs, Graph, Node

T = TypeVar('T', bound='PointNode')


class PointNode(Point, Node):
    def __init__(self, point: Point) -> None:
        super().__init__(point.x, point.y)

    @property
    def point(self) -> Point:
        return Point(self.x, self.y)


class RecursivePointNode(PointNode):
    layer: int

    def __init__(self, point: Point, layer: int = 0):
        self.layer = layer
        super().__init__(point)

    def __repr__(self) -> str:
        return f'{super().__repr__()} [{self.layer}]'

    def __eq__(self, other: RecursivePointNode) -> bool:
        return super().__eq__(other) and self.layer == other.layer

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.layer))


class Maze(Generic[T], Graph[T], ABC):
    map: list[str]
    start: T
    end: T
    portals: dict[Point, T]
    portal_ids: dict[Point, str]
    outer_bounds: Rect
    inner_bounds: Rect

    nodes: dict[T, T]

    def __init__(self, lines: list[str]) -> None:
        self.map = lines
        self.portal_ids = {}
        self.nodes = {}
        self.parse_bounds()
        self.parse_portals()

    def parse_bounds(self) -> None:
        self.outer_bounds = Rect(Point(2, 2), Point(len(self.map[0]) - 3, len(self.map) - 3))
        middle = self.outer_bounds.middle
        maze_chars = ('#', '.')
        x, y, x2, y2 = 0, 0, 0, 0
        for x in range(self.outer_bounds.top_left.x, middle.x):
            if self.map[middle.y][x] not in maze_chars:
                break
        for y in range(self.outer_bounds.top_left.y, middle.y):
            if self.map[y][middle.x] not in maze_chars:
                break
        for x2 in range(self.outer_bounds.bottom_right.x, middle.x, -1):
            if self.map[middle.y][x2] not in maze_chars:
                break
        for y2 in range(self.outer_bounds.bottom_right.y, middle.y, -1):
            if self.map[y2][middle.x] not in maze_chars:
                break
        self.inner_bounds = Rect(Point(x - 1, y - 1), Point(x2 + 1, y2 + 1))

    def parse_portals(self) -> None:
        portals: dict[str, list[Point]] = {}
        y1 = self.outer_bounds.top_left.y
        y2 = self.outer_bounds.bottom_right.y
        for x in range(self.outer_bounds.top_left.x, self.outer_bounds.bottom_right.x):
            if self.map[y1][x] == '.':
                portal = self.map[y1 - 2][x] + self.map[y1 - 1][x]
                portals.setdefault(portal, []).append(Point(x, y1))
            if self.map[y2][x] == '.':
                portal = self.map[y2 + 1][x] + self.map[y2 + 2][x]
                portals.setdefault(portal, []).append(Point(x, y2))

        x1 = self.outer_bounds.top_left.x
        x2 = self.outer_bounds.bottom_right.x
        for y in range(self.outer_bounds.top_left.y, self.outer_bounds.bottom_right.y):
            if self.map[y][x1] == '.':
                portal = self.map[y][x1 - 2] + self.map[y][x1 - 1]
                portals.setdefault(portal, []).append(Point(x1, y))
            if self.map[y][x2] == '.':
                portal = self.map[y][x2 + 1] + self.map[y][x2 + 2]
                portals.setdefault(portal, []).append(Point(x2, y))

        y1 = self.inner_bounds.top_left.y
        y2 = self.inner_bounds.bottom_right.y
        for x in range(self.inner_bounds.top_left.x, self.inner_bounds.bottom_right.x):
            if self.map[y1][x] == '.':
                portal = self.map[y1 + 1][x] + self.map[y1 + 2][x]
                portals.setdefault(portal, []).append(Point(x, y1))
            if self.map[y2][x] == '.':
                portal = self.map[y2 - 2][x] + self.map[y2 - 1][x]
                portals.setdefault(portal, []).append(Point(x, y2))

        x1 = self.inner_bounds.top_left.x
        x2 = self.inner_bounds.bottom_right.x
        for y in range(self.inner_bounds.top_left.y, self.inner_bounds.bottom_right.y):
            if self.map[y][x1] == '.':
                portal = self.map[y][x1 + 1] + self.map[y][x1 + 2]
                portals.setdefault(portal, []).append(Point(x1, y))
            if self.map[y][x2] == '.':
                portal = self.map[y][x2 - 2] + self.map[y][x2 - 1]
                portals.setdefault(portal, []).append(Point(x2, y))

        self.start = self.create_node(portals.pop('AA')[0])
        self.register_node(self.start)
        self.portal_ids[self.start.point] = 'AA'
        self.end = self.create_node(portals.pop('ZZ')[0])
        self.register_node(self.end)
        self.portal_ids[self.end.point] = 'ZZ'
        self.portals = {}
        for portal_id, (start, end) in portals.items():
            self.portal_ids[start] = portal_id
            self.portal_ids[end] = portal_id
            start_node = self.create_portal_node(start)
            end_node = self.create_portal_node(end)
            self.register_node(start_node)
            self.register_node(end_node)
            self.portals[start] = end_node
            self.portals[end] = start_node

    def register_node(self, node: T) -> None:
        self.nodes[node] = node

    @abstractmethod
    def create_node(self, position: Point) -> T:
        pass

    @abstractmethod
    def create_portal_node(self, position: Point) -> T:
        pass

    @abstractmethod
    def create_relative_node(self, node: T, position: Point) -> T:
        pass

    @abstractmethod
    def get_portal_node(self, start: T) -> T | None:
        pass

    def get_relative_node(self, node: T, x: int, y: int) -> T | None:
        position = node + Point(x, y)
        if self.map[position.y][position.x] == '.':
            relative_node = self.create_relative_node(node, node + Point(x, y))
            return self.nodes.setdefault(relative_node, relative_node)

    def get_root(self) -> T:
        return self.start

    def is_goal(self, node: T) -> bool:
        return self.end == node

    def get_edges(self, node: T) -> list[T]:
        edges = [
            self.get_relative_node(node, -1, 0),
            self.get_relative_node(node, 0, 1),
            self.get_relative_node(node, 1, 0),
            self.get_relative_node(node, 0, -1),
            self.get_portal_node(node)
        ]
        return [neighbor for neighbor in edges if neighbor is not None]


class PortalMaze(Maze[PointNode]):
    def create_node(self, position: Point) -> PointNode:
        return PointNode(position)

    def create_portal_node(self, position: Point) -> PointNode:
        return self.create_node(position)

    def create_relative_node(self, node: PointNode, position: Point) -> PointNode:
        return self.create_node(position)

    def get_portal_node(self, start: PointNode) -> PointNode | None:
        return self.portals.get(start.point)


class RecursiveMaze(Maze, Graph[RecursivePointNode]):
    def create_node(self, position: Point) -> RecursivePointNode:
        return RecursivePointNode(position)

    def create_portal_node(self, position: Point) -> RecursivePointNode:
        return RecursivePointNode(position, layer=-1 if position in self.inner_bounds else 1)

    def create_relative_node(self, node: RecursivePointNode, position: Point) -> RecursivePointNode:
        return RecursivePointNode(position, layer=node.layer)

    def get_portal_node(self, start: RecursivePointNode) -> RecursivePointNode | None:
        portal: RecursivePointNode | None = self.portals.get(start.point)
        if portal is not None:
            if start.layer == 0 and portal.layer == -1:
                return None
            portal_node = RecursivePointNode(portal.point, layer=start.layer + portal.layer)
            return self.nodes.setdefault(portal_node, portal_node)


_lines = read_input(strip_whitespace=False)

_maze = PortalMaze(_lines)
part1 = len(bfs(_maze).build_path()) - 1
print(f'Part 1: {part1}')

_maze = RecursiveMaze(_lines)
part2 = len(bfs(_maze).build_path()) - 1
print(f'Part 2: {part2}')
