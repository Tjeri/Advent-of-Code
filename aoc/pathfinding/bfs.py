from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Hashable, TypeVar

T = TypeVar('T', bound='Node')


class Graph(ABC, Generic[T]):
    @abstractmethod
    def get_root(self) -> T:
        pass

    @abstractmethod
    def is_goal(self, node: T) -> bool:
        pass

    @abstractmethod
    def get_edges(self, node: T) -> list[T]:
        pass


class Node(ABC, Hashable):
    parent: T | None = None

    def get_parent(self: T) -> T | None:
        return self.parent

    def set_parent(self: T, parent: T | None) -> None:
        self.parent = parent

    def build_path(self: T) -> list[T]:
        node = self
        path = [self]
        while node := node.get_parent():
            path.append(node)
        return path


def breadth_first_search(graph: Graph[T]) -> T:
    explored: set[T] = {graph.get_root()}
    queue: list[T] = [graph.get_root()]
    while queue:
        node = queue.pop(0)
        if graph.is_goal(node):
            return node
        for edge in graph.get_edges(node):
            if edge in explored:
                continue
            explored.add(edge)
            edge.set_parent(node)
            queue.append(edge)
    raise RuntimeError('No Path found.')


bfs = breadth_first_search
