from __future__ import annotations

import heapq
from typing import TypeVar, Generic, Any, Callable

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    elements: list[T]

    def __init__(self) -> None:
        self.elements = list()

    def push(self, item: T, priority: float) -> None:
        heapq.heappush(self.elements, (priority, item))

    def pop(self) -> T:
        return heapq.heappop(self.elements)[1]

    def __bool__(self) -> bool:
        return len(self.elements) > 0


class Node:
    id: str
    neighbors: list[tuple[float, Node]]

    def __init__(self, _id: str) -> None:
        self.id = _id
        self.neighbors = list()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Node):
            raise ValueError(f'Can\'t compare Node with {type(other)}.')
        return self.id == other.id

    def __lt__(self, other: Any):
        if not isinstance(other, Node):
            raise ValueError(f'Can\'t compare Node with {type(other)}.')
        return self.id < other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def add_neighbor(self, neighbor: Node, cost: float = 1) -> None:
        self.neighbors.append((cost, neighbor))


def dijkstra(start: Node, goal: Node) -> list[Node]:
    return a_star(start, goal, lambda a, b: 0)


def a_star(start: Node, goal: Node, heuristic: Callable[[Node, Node], float]) -> list[Node]:
    open_set: PriorityQueue[Node] = PriorityQueue()
    open_set.push(start, 0)

    came_from: dict[Node, Node] = dict()
    node_costs: dict[Node, float] = dict()
    node_costs[start] = 0

    while open_set:
        current: Node = open_set.pop()
        if current == goal:
            break
        current_cost = node_costs[current]
        for cost, neighbor in current.neighbors:
            new_cost = current_cost + cost
            if new_cost < node_costs.get(neighbor, new_cost + 1):
                node_costs[neighbor] = new_cost
                open_set.push(neighbor, new_cost + heuristic(neighbor, goal))
                came_from[neighbor] = current
            else:
                continue

    if goal not in came_from:
        # no path found
        return []
    path: list[Node] = list()
    current: Node = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
