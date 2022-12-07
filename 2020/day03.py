class TreeMap:
    trees: list[list[bool]] = list()
    width: int = 0
    height: int = 0

    def add_line(self, _line: str) -> None:
        self.trees.append([char == '#' for char in _line])
        if self.width == 0:
            self.width = len(_line)
        self.height += 1

    def is_tree(self, x: int, y: int) -> bool:
        if y >= self.height:
            return False
        return self.trees[y][x % self.width]


tree_map = TreeMap()
with open('../data/2020/day03.txt') as file:
    for line in file.readlines():
        tree_map.add_line(line.strip())


def find_trees(slope_x: int, slope_y: int) -> int:
    trees = 0
    for i in range(1, tree_map.height):
        if tree_map.is_tree(slope_x * i, slope_y * i):
            trees += 1
    return trees


print(f'Part 1: {find_trees(3, 1)}')
print(f'Part 2: {find_trees(1, 1) * find_trees(3, 1) * find_trees(5, 1) * find_trees(7, 1) * find_trees(1, 2)}')
