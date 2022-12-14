from __future__ import annotations

import math

from tools.a_star import Node, a_star


class HillNode(Node):
    pos: tuple[int, int]
    height: int

    def __init__(self, pos: tuple[int, int], height: int | str) -> None:
        super().__init__(f'{pos[0]}/{pos[1]}')
        self.pos = pos
        if isinstance(height, int):
            self.height = height
        else:
            self.height = ord(height) - ord('a')

    def try_add_neighbor(self, neighbor: HillNode) -> None:
        if neighbor.height - self.height <= 1:
            self.add_neighbor(neighbor)
        if self.height - neighbor.height <= 1:
            neighbor.add_neighbor(self)


def heuristic(a: HillNode, b: HillNode) -> float:
    return math.sqrt(pow(abs(a.pos[0] - b.pos[0]), 2) + pow(abs(a.pos[1] - b.pos[1]), 2))


hills: list[list[HillNode]] = list()
start: HillNode = HillNode((-1, -1), 0)
possible_starts: list[HillNode] = list()
goal: HillNode = HillNode((-1, -1), 25)
with open('../data/2022/day12.txt') as file:
    for y, line in enumerate(file.readlines()):
        line = line.strip()
        hills.append(list())
        for x, char in enumerate(line):
            if char == 'S':
                node = HillNode((x, y), 'a')
                start = node
            elif char == 'E':
                node = HillNode((x, y), 'z')
                goal = node
            else:
                node = HillNode((x, y), char)
            if node.height == 1:
                possible_starts.append(node)
            hills[y].append(node)
            if x > 0:
                hills[y][x - 1].try_add_neighbor(node)
            if y > 0:
                hills[y - 1][x].try_add_neighbor(node)

print(f'Part 1: {len(a_star(start, goal, heuristic)) - 1}')

shortest = 462
for possible_start in possible_starts:
    shortest = min(shortest, len(a_star(possible_start, goal, heuristic)))
print(f'Part 2: {shortest}')
