tree_heights = list()
grid_height = 0
grid_width = 0


def is_visible(x: int, y: int) -> bool:
    if x == 0 or y == 0 or x == grid_width - 1 or y == grid_height - 1:
        return True
    height = tree_heights[y][x]
    for __x in range(0, x):
        if tree_heights[y][__x] >= height:
            break
    else:
        return True
    for __x in range(x + 1, len(tree_heights[y])):
        if tree_heights[y][__x] >= height:
            break
    else:
        return True
    for __y in range(0, y):
        if tree_heights[__y][x] >= height:
            break
    else:
        return True
    for __y in range(y + 1, len(tree_heights)):
        if tree_heights[__y][x] >= height:
            break
    else:
        return True
    return False


def calculate_scenic_score(x: int, y: int) -> int:
    if x == 0 or y == 0 or x == grid_width - 1 or y == grid_height - 1:
        return 0
    height = tree_heights[y][x]
    left, right, up, down = 0, 0, 0, 0
    for __x in range(x - 1, -1, -1):
        left += 1
        if tree_heights[y][__x] >= height:
            break
    for __x in range(x + 1, grid_width):
        right += 1
        if tree_heights[y][__x] >= height:
            break
    for __y in range(y - 1, -1, -1):
        up += 1
        if tree_heights[__y][x] >= height:
            break
    for __y in range(y + 1, grid_height):
        down += 1
        if tree_heights[__y][x] >= height:
            break
    return left * right * up * down


with open('../data/2022/day08.txt') as file:
    for line in file.readlines():
        line = line.strip()
        tree_heights.append([int(tree) for tree in line])
        if grid_width == 0:
            grid_width = len(tree_heights[0])
        grid_height += 1

visible = 0
for _y in range(0, grid_height):
    for _x in range(0, grid_width):
        if is_visible(_x, _y):
            visible += 1
print(f'Part 1: {visible}')

best_score = 0
for _y in range(1, grid_height - 1):
    for _x in range(1, grid_width - 1):
        if (score := calculate_scenic_score(_x, _y)) > best_score:
            best_score = score
print(f'Part 2: {best_score}')
