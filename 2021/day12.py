from typing import Optional

file_name = '../data/2021/day12.txt'


class Graph:
    start: str = 'start'
    end: str = 'end'
    paths: list[tuple[str, str]]
    small_caves: set[str]

    def __init__(self):
        self.paths = []
        self.small_caves = set()

    def add_path(self, raw: str) -> None:
        sep = raw.index('-')
        _start = raw[:sep]
        _end = raw[sep + 1:]
        self.paths.append((_start, _end))
        if _start[0] > 'Z':
            self.small_caves.add(_start)
        if _end[0] > 'Z':
            self.small_caves.add(_end)

    def find_connected_nodes(self, node: str, exclude: Optional[set[str]] = None) -> list[str]:
        connected = set()
        for path in self.paths:
            if node not in path:
                continue
            if path[0] == node:
                connected.add(path[1])
            else:
                connected.add(path[0])
        return list(connected - exclude)

    def find_paths(self, start: Optional[str] = None, history: Optional[list[str]] = None,
                   visited_small_twice: bool = False) -> Optional[set[str]]:
        if start is None:
            start = self.start
        _history = [] if history is None else history.copy()
        _history.append(start)
        if start == self.end:
            return {','.join(_history)}
        paths = set()
        exclude = {node for node in _history if node in self.small_caves} if visited_small_twice else {'start'}
        for connected in self.find_connected_nodes(start, exclude):
            if connected in self.small_caves and connected in _history:
                _paths = self.find_paths(connected, _history, True)
            else:
                _paths = self.find_paths(connected, _history, visited_small_twice)
            if _paths:
                paths.update(_paths)
        return paths


graph = Graph()
with open(file_name) as file:
    for line in file.readlines():
        graph.add_path(line.strip())

print(f'Part 1: {len(graph.find_paths(visited_small_twice=True))}')
print(f'Part 1: {len(graph.find_paths())}')
