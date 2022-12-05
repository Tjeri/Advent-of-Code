from dataclasses import dataclass
from typing import Any

file_name = '../data/2021/day15.txt'


@dataclass
class Node:
    x: int
    y: int
    f: int
    g: int

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            return False
        return self.g < other.f


class Graph:
    nodes: list[list[int]]
    max_node: int = 0
    width: int
    height: int

    def __init__(self):
        self.nodes = list()
        self.width = 0
        self.height = 0

    def expand_map(self) -> None:
        nodes: list[list[int]] = [[] for _ in range(self.height * 5)]
        for my in range(5):
            for mx in range(5):
                for y in range(self.height):
                    for x in range(self.width):
                        nodes[my * self.height + y].append((self.nodes[y][x] + my + mx - 1) % 9 + 1)
        self.nodes = nodes
        self.width *= 5
        self.height *= 5

    def add_row(self) -> None:
        self.nodes.append([])
        self.height += 1

    def add_node(self, value: int) -> None:
        self.nodes[-1].append(value)
        if self.height == 1:
            self.width += 1
        if value > self.max_node:
            self.max_node = value

    def goal_distance(self, x: int, y: int) -> int:
        return 0

    def a_star(self) -> int:
        from heapq import heappush as push, heappop as pop
        start = Node(0, 0, self.goal_distance(0, 0), 0)
        nodes: list[Node] = [start]
        origins: dict[tuple[int, int], tuple[int, int]] = dict()

        f_scores: dict[tuple[int, int], int] = {start.pos: start.f}
        g_scores: dict[tuple[int, int], int] = {start.pos: start.g}

        while nodes:
            node = pop(nodes)
            if node.x == self.width - 1 and node.y == self.height - 1:
                result = self.nodes[node.y][node.x]
                pos = node.pos
                while pos in origins:
                    pos = origins[pos]
                    result += self.nodes[pos[1]][pos[0]]
                return result - self.nodes[0][0]
            neighbors = [
                (node.x - 1, node.y),
                (node.x + 1, node.y),
                (node.x, node.y - 1),
                (node.x, node.y + 1)
            ]
            for neighbor in neighbors:
                x, y = neighbor
                if x < 0 or y < 0 or x >= self.width or y >= self.height:
                    continue
                g_score = node.g + self.nodes[y][x]
                if neighbor not in g_scores or g_score < g_scores[neighbor]:
                    n_node = Node(x, y, g_score + self.goal_distance(x, y), g_score)
                    origins[neighbor] = node.pos
                    f_scores[neighbor] = n_node.f
                    g_scores[neighbor] = n_node.g
                    push(nodes, n_node)


graph = Graph()
with open(file_name) as file:
    for line in file.readlines():
        graph.add_row()
        for _value in line.strip():
            graph.add_node(int(_value))

print(f'Part 1: {graph.a_star()}')
graph.expand_map()
print(f'Part 2: {graph.a_star()}')
