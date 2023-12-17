from __future__ import annotations

from aoc.coord2d.point import Point
from aoc.input import read_input
from aoc.pathfinding.a_star import dijkstra, Node as _Node


class Node(_Node):
    position: Point
    blocked: Point

    def __init__(self, position: Point, blocked: Point) -> None:
        super().__init__(f'{position.x}/{position.y} - {blocked.x}/{blocked.y}')
        self.position = position
        self.blocked = blocked

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return str(self)

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y


def calculate_best_path(lines: list[str], min_distance: int, max_distance: int) -> int:
    start, goal = build_graph(_lines, min_distance, max_distance)
    path = dijkstra(start, goal)
    costs = path_costs(path, lines)
    return costs


def build_graph(lines: list[str], min_distance: int, max_distance: int) -> tuple[Node, Node]:
    start = Node(Point(0, 0), Point(0, 0))
    goal = Node(Point(len(lines[0]) - 1, len(lines) - 1), Point(0, 0))
    finished = set()
    all_nodes: dict[tuple[Point, Point], Node] = {
        (start.position, start.blocked): start,
        (goal.position, goal.blocked): goal
    }
    nodes = {start}
    while nodes:
        node = nodes.pop()
        if node is None or node in finished:
            continue
        for x in range(min_distance, max_distance + 1):
            nodes.add(add_neighbor(node, x, 0, lines, goal, all_nodes, max_distance))
        for y in range(min_distance, max_distance + 1):
            nodes.add(add_neighbor(node, 0, y, lines, goal, all_nodes, max_distance))
        for x in range(-min_distance, -max_distance - 1, -1):
            nodes.add(add_neighbor(node, x, 0, lines, goal, all_nodes, max_distance))
        for y in range(-min_distance, -max_distance - 1, -1):
            nodes.add(add_neighbor(node, 0, y, lines, goal, all_nodes, max_distance))
        finished.add(node)
    return start, goal


def add_neighbor(node: Node, x: int, y: int, lines: list[str], goal: Node,
                 all_nodes: dict[tuple[Point, Point], Node], max_distance: int) -> Node | None:
    if abs(node.blocked.x + x) > max_distance or abs(node.blocked.y + y) > max_distance:
        return
    if node.blocked.x != 0 and x != 0 and (node.blocked.x > 0) != (x > 0):
        return
    if node.blocked.y != 0 and y != 0 and (node.blocked.y > 0) != (y > 0):
        return
    neighbor_position = Point(node.x + x, node.y + y)
    if not (0 <= neighbor_position.x < len(lines[0])):
        return
    if not (0 <= neighbor_position.y < len(lines)):
        return
    if neighbor_position.x == goal.x and neighbor_position.y == goal.y:
        node.add_neighbor(goal, get_costs(node.position, goal.position, lines))
        return
    if x != 0:
        neighbor_blocked = Point(node.blocked.x + x, 0)
    else:
        neighbor_blocked = Point(0, node.blocked.y + y)
    key = (neighbor_position, neighbor_blocked)
    if key in all_nodes:
        neighbor = all_nodes[key]
    else:
        neighbor = Node(*key)
        all_nodes[key] = neighbor
    node.add_neighbor(neighbor, get_costs(node.position, neighbor_position, lines))
    return neighbor


def get_costs(_from: Point, _to: Point, lines: list[str]) -> int:
    costs = 0
    for x in get_range(_from.x, _to.x):
        for y in get_range(_from.y, _to.y):
            if x != _from.x or y != _from.y:
                costs += int(lines[y][x])
    return costs


def get_range(_from: int, _to: int) -> range:
    if _from <= _to:
        return range(_from, _to + 1)
    return range(_from, _to - 1, -1)


def path_costs(path: list[Node], lines: list[str]) -> int:
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += get_costs(path[i].position, path[i + 1].position, lines)
    return total_cost


_lines = read_input(True)
print(f'Part 1: {calculate_best_path(_lines, 1, 3)}')
print(f'Part 2: {calculate_best_path(_lines, 4, 10)}')
