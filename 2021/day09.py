cave = []
with open('../data/2021/day09.txt') as file:
    for line in file.readlines():
        cave.append([int(c) for c in line.strip()])

risk_level = 0
for y in range(0, len(cave)):
    for x in range(0, len(cave[y])):
        value = cave[y][x]
        if x > 0 and value >= cave[y][x - 1]:
            continue
        if x < len(cave[y]) - 1 and value >= cave[y][x + 1]:
            continue
        if y > 0 and value >= cave[y - 1][x]:
            continue
        if y < len(cave) - 1 and value >= cave[y + 1][x]:
            continue
        risk_level += value + 1

print(f'Part 1: {risk_level}')


def find_basin(_x: int, _y: int) -> int:
    if cave[_y][_x] == -1 or cave[_y][_x] == 9:
        return 0
    cave[_y][_x] = -1
    size = 1
    if _x > 0:
        size += find_basin(_x - 1, _y)
    if _x < len(cave[_y]) - 1:
        size += find_basin(_x + 1, _y)
    if _y > 0:
        size += find_basin(_x, _y - 1)
    if _y < len(cave) - 1:
        size += find_basin(_x, _y + 1)
    return size


basins = []
for y in range(0, len(cave)):
    for x in range(0, len(cave[y])):
        basin = find_basin(x, y)
        if basin > 0:
            basins.append(basin)

basins.sort(reverse=True)
print(f'Part 2: {basins[0] * basins[1] * basins[2]}')
