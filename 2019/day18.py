from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from aoc.coord2d.point import Point
from aoc.input import read_input
from aoc.pathfinding.bfs import bfs, Graph, Node


class CaveNodeType(IntEnum):
    Start = 0
    Intersection = 1
    Key = 2
    Door = 3


class CaveNode(Node):
    position: Point
    type: CaveNodeType
    value: int | None = None

    def __init__(self, x: int, y: int, char: str) -> None:
        self.position = Point(x, y)
        self.paths = set()
        if char == '@':
            self.type = CaveNodeType.Start
        elif char == '.':
            self.type = CaveNodeType.Intersection
        elif 'A' <= char <= 'Z':
            self.type = CaveNodeType.Door
            self.value = ord(char) - ord('A')
        elif 'a' <= char <= 'z':
            self.type = CaveNodeType.Key
            self.value = ord(char) - ord('a')
        else:
            raise ValueError(f'Invalid Node type: {char}')

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.value is not None:
            return f'Node({self.position.x}/{self.position.y})[{self.type.name}: {self.value}]'
        return f'Node({self.position.x}/{self.position.y})[{self.type.name}]'

    def __hash__(self) -> int:
        return hash(self.position)


class CavePath:
    start: CaveNode
    end: CaveNode
    length: int
    pois: list[CaveNode]

    def __init__(self, path: list[CaveNode]) -> None:
        self.start = path[0]
        self.end = path[-1]
        self.length = len(path) - 1
        self.pois = []
        for node in path[1:-1]:
            if node.type in (CaveNodeType.Key, CaveNodeType.Door):
                self.pois.append(node)

    def collect_keys(self) -> set[int]:
        return {poi.value for poi in self.pois + [self.start, self.end] if poi.type is CaveNodeType.Key}

    def can_use(self, keys: set[int]) -> bool:
        additional_keys = set()
        for poi in self.pois:
            if poi.type is CaveNodeType.Key:
                additional_keys.add(poi.value)
            elif poi.type is CaveNodeType.Door and poi.value not in keys and poi.value not in additional_keys:
                return False
        return True


@dataclass
class CaveGraph(Graph[CaveNode]):
    start: CaveNode
    end: CaveNode
    nodes: dict[Point, CaveNode]

    def get_root(self) -> CaveNode:
        return self.start

    def is_goal(self, node: CaveNode) -> bool:
        return node == self.end

    def get_edges(self, node: CaveNode) -> list[CaveNode]:
        edges = []
        for direction in (Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)):
            position = node.position + direction
            if position in self.nodes:
                edges.append(self.nodes[position])
        return edges


class Cave:
    start: tuple[CaveNode, ...]
    nodes: dict[Point, CaveNode]
    keys: list[CaveNode]
    path_table: dict[CaveNode, dict[CaveNode, CavePath]]

    cache: dict[tuple[CaveNode, ...], dict[tuple[int, ...], int]]

    def __init__(self, lines: list[str]) -> None:
        self.parse_nodes(lines)
        self.keys.sort(key=lambda key: key.value)
        self.find_paths()
        self.cache = {}

    def parse_nodes(self, lines: list[str]) -> None:
        starts = []
        self.nodes = {}
        self.keys = []
        for y, line in enumerate(lines[1:-1]):
            for x, char in enumerate(line[1:-1]):
                if char == '#':
                    continue
                node = CaveNode(x, y, char)
                self.nodes[node.position] = node
                if node.type is CaveNodeType.Start:
                    starts.append(node)
                elif node.type is CaveNodeType.Key:
                    self.keys.append(node)
        self.start = tuple(starts)

    def find_paths(self) -> None:
        self.path_table = {}
        relevant_nodes = list(self.start) + self.keys
        for node in relevant_nodes:
            for other in relevant_nodes:
                if node == other or other in self.path_table.get(node, {}):
                    continue
                graph = CaveGraph(node, other, self.nodes)
                try:
                    end = bfs(graph)
                    path = end.build_path()
                    self.path_table.setdefault(other, {})[node] = CavePath(path)
                    path.reverse()
                    self.path_table.setdefault(node, {})[other] = CavePath(path)
                except RuntimeError:
                    pass
                finally:
                    self.reset_parents()

    def reset_parents(self) -> None:
        for node in self.nodes.values():
            node.set_parent(None)

    def find_shortest_path(self) -> int:
        return self._find_shortest_path(self.start, set())

    def _find_shortest_path(self, current_nodes: tuple[CaveNode, ...], keys: set[int]) -> int:
        if len(keys) == len(self.keys):
            return 0
        if current_nodes in self.cache and tuple(keys) in self.cache[current_nodes]:
            return self.cache[current_nodes][tuple(keys)]
        shortest = 2_000_000_000
        for key in self.keys:
            if key in current_nodes or key.value in keys:
                continue
            for i, node in enumerate(current_nodes):
                path = self.path_table[node].get(key)
                if path and path.can_use(keys):
                    new_nodes = current_nodes[:i] + (key,) + current_nodes[i + 1:]
                    length = self._find_shortest_path(new_nodes, keys | path.collect_keys()) + path.length
                    if length < shortest:
                        shortest = length
                    break
        self.cache.setdefault(current_nodes, {})[tuple(keys)] = shortest
        return shortest


_lines = read_input()
_cave = Cave(_lines)
print(f'Part 1: {_cave.find_shortest_path()}')

_lines = read_input(True, 2)
_cave2 = Cave(_lines)
print(f'Part 2: {_cave2.find_shortest_path()}')
