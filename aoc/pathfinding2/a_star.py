from __future__ import annotations

from typing import Callable, Hashable, TypeVar

from aoc.data_structures.priority_queue import PriorityQueue

T = TypeVar('T', bound=Hashable)


def dijkstra(start: T, goal: Callable[[T], bool], neighbors: Callable[[T], dict[T, float]]) -> tuple[float, list[T]]:
    return a_star(start, goal, neighbors, lambda a: 0)


def a_star(start: T, goal: Callable[[T], bool], neighbors: Callable[[T], dict[T, float]],
           heuristic: Callable[[T], float]) -> tuple[float, list[T]]:
    open_set: PriorityQueue[T] = PriorityQueue()
    open_set.push(start, 0)

    came_from: dict[T, T] = dict()
    node_costs: dict[T, float] = dict()
    node_costs[start] = 0

    while open_set:
        current: T = open_set.pop()
        if goal(current):
            break
        current_cost = node_costs[current]
        for neighbor, cost in neighbors(current).items():
            new_cost = current_cost + cost
            if new_cost < node_costs.get(neighbor, new_cost + 1):
                node_costs[neighbor] = new_cost
                open_set.push(neighbor, new_cost + heuristic(neighbor))
                came_from[neighbor] = current
            else:
                continue

    end_goal: T
    for node in came_from:
        if goal(node):
            end_goal = node
            break
    else:
        # no path found
        return 0, []
    path: list[T] = list()
    current: T = end_goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return node_costs[end_goal], path



def dijkstra_all_shortest_paths(start: T, goal: Callable[[T], bool], neighbors: Callable[[T], dict[T, float]]) -> tuple[float, list[list[T]]]:
    return a_star_all_shortest_paths(start, goal, neighbors, lambda a: 0)


def a_star_all_shortest_paths(start: T, goal: Callable[[T], bool], neighbors: Callable[[T], dict[T, float]],
                              heuristic: Callable[[T], float]) -> tuple[float, list[list[T]]]:
    open_set: PriorityQueue[T] = PriorityQueue()
    open_set.push(start, 0)

    came_from: dict[T, set[T]] = dict()
    node_costs: dict[T, float] = dict()
    node_costs[start] = 0

    while open_set:
        current: T = open_set.pop()
        if goal(current):
            break
        current_cost = node_costs[current]
        for neighbor, cost in neighbors(current).items():
            new_cost = current_cost + cost
            if new_cost < node_costs.get(neighbor, new_cost + 1):
                node_costs[neighbor] = new_cost
                open_set.push(neighbor, new_cost + heuristic(neighbor))
                came_from[neighbor] = set()
                came_from[neighbor].add(current)
            elif new_cost == node_costs.get(neighbor, new_cost + 1):
                came_from[neighbor].add(current)
            else:
                continue

    end_goal: T
    for node in came_from:
        if goal(node):
            end_goal = node
            break
    else:
        # no path found
        return 0, []
    paths: list[list[T]] = list()
    paths.append([end_goal])
    while True:
        changes = False
        new_paths = []
        for path in paths:
            current = path[-1]
            if current == start:
                continue
            changes = True
            nodes = list(came_from[current])
            if len(nodes) > 0:
                for node in nodes[1:]:
                    copy = path.copy()
                    copy.append(node)
                    new_paths.append(copy)
            path.append(nodes[0])
        if new_paths:
            paths += new_paths
        if not changes:
            break

    for path in paths:
        path.reverse()
    return node_costs[end_goal], paths
