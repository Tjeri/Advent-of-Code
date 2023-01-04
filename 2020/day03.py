from aoc.input import read_input


class TreeMap:
    trees: list[list[bool]] = list()
    width: int = 0
    height: int = 0

    def __init__(self, lines: list[str]) -> None:
        self.trees = [[char == '#' for char in line] for line in lines]
        self.width = len(lines[0])
        self.height = len(lines)

    def is_tree(self, x: int, y: int) -> bool:
        if y >= self.height:
            return False
        return self.trees[y][x % self.width]


def find_trees(slope_x: int, slope_y: int) -> int:
    trees = 0
    for i in range(1, tree_map.height):
        if tree_map.is_tree(slope_x * i, slope_y * i):
            trees += 1
    return trees


tree_map = TreeMap(read_input())
print(f'Part 1: {find_trees(3, 1)}')
print(f'Part 2: {find_trees(1, 1) * find_trees(3, 1) * find_trees(5, 1) * find_trees(7, 1) * find_trees(1, 2)}')
