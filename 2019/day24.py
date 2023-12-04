from __future__ import annotations

import itertools

from aoc.input import read_input


class GameOfLife:
    map: list[list[bool]]
    cache: set[tuple[bool, ...]]

    def __init__(self, lines: list[str]) -> None:
        self.map = [[char == '#' for char in line] for line in lines]
        self.cache = set()

    @property
    def map_id(self) -> tuple[bool, ...]:
        return tuple(itertools.chain.from_iterable(self.map))

    @property
    def biodiversity_rating(self) -> int:
        map_id = self.map_id
        return sum(pow(2, i) for i in range(len(map_id)) if map_id[i])

    def run(self) -> int:
        while not self.finished():
            self.next()
        return self.biodiversity_rating

    def next(self) -> GameOfLife:
        self.cache.add(self.map_id)
        new_map = []
        for y, line in enumerate(self.map):
            new_line = []
            for x, bug in enumerate(line):
                neighbors = self.count_neighbors(x, y)
                if bug:
                    new_line.append(neighbors == 1)
                else:
                    new_line.append(1 <= neighbors <= 2)
            new_map.append(new_line)
        self.map = new_map
        return self

    def finished(self) -> bool:
        return self.map_id in self.cache

    def count_neighbors(self, x: int, y: int) -> int:
        def exists(nx: int, ny: int):
            return 0 <= ny < len(self.map) and 0 <= nx < len(self.map[ny])

        neighbors = 0
        if exists(x - 1, y) and self.map[y][x - 1]:
            neighbors += 1
        if exists(x + 1, y) and self.map[y][x + 1]:
            neighbors += 1
        if exists(x, y - 1) and self.map[y - 1][x]:
            neighbors += 1
        if exists(x, y + 1) and self.map[y + 1][x]:
            neighbors += 1
        return neighbors


class RecursiveGameOfLife:
    maps: dict[int, list[list[bool]]]

    def __init__(self, lines: list[str]) -> None:
        self.maps = {0: [[char == '#' for char in line] for line in lines]}

    @property
    def bug_count(self) -> int:
        return sum(itertools.chain(*itertools.chain(*itertools.chain(self.maps.values()))))

    def run(self, rounds: int) -> int:
        for _ in range(rounds):
            self.next()
        return self.bug_count

    def next(self) -> RecursiveGameOfLife:
        def new_layer(_layer: int) -> list[list[bool]]:
            map_ = self.maps.get(_layer, [[False] * 5] * 5)
            result = []
            for y, line in enumerate(map_):
                new_line = []
                for x, bug in enumerate(line):
                    if x == 2 and y == 2:
                        new_line.append(False)
                        continue
                    neighbors = self.count_neighbors(x, y, _layer)
                    if bug:
                        new_line.append(neighbors == 1)
                    else:
                        new_line.append(1 <= neighbors <= 2)
                result.append(new_line)
            return result

        new_maps = {}
        for layer in self.maps:
            new_maps[layer] = new_layer(layer)
        new_outer = new_layer(min(self.maps) - 1)
        if any(itertools.chain(new_outer)):
            new_maps[min(self.maps) - 1] = new_outer
        new_inner = new_layer(max(self.maps) + 1)
        if any(itertools.chain(new_inner)):
            new_maps[max(self.maps) + 1] = new_inner
        self.maps = new_maps
        return self

    def count_neighbors(self, x: int, y: int, layer: int) -> int:
        def count(nx: int, ny: int, nlayer: int) -> int:
            if nx < 0:
                return count(1, 2, nlayer - 1)
            if nx > 4:
                return count(3, 2, layer - 1)
            if ny < 0:
                return count(2, 1, layer - 1)
            if ny > 4:
                return count(2, 3, layer - 1)
            if nx == 2 and ny == 2:
                if x == 1:
                    return sum(count(0, _y, layer + 1) for _y in range(5))
                if x == 3:
                    return sum(count(4, _y, layer + 1) for _y in range(5))
                if y == 1:
                    return sum(count(_x, 0, layer + 1) for _x in range(5))
                if y == 3:
                    return sum(count(_x, 4, layer + 1) for _x in range(5))
                return 0
            _map = self.maps.get(nlayer)
            if _map:
                return int(_map[ny][nx])
            return 0

        return count(x - 1, y, layer) + count(x + 1, y, layer) + count(x, y - 1, layer) + count(x, y + 1, layer)


_lines = read_input()
_game = GameOfLife(_lines)
print(f'Part 1:  {_game.run()}')
_game2 = RecursiveGameOfLife(_lines)
print(f'Part 2: {_game2.run(200)}')
