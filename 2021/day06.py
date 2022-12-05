days = 256

fish_map: dict[int, int] = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0
}
with open('../data/2021/day06.txt') as file:
    for fish_str in file.readline().split(','):
        fish = int(fish_str)
        fish_map[fish] += 1

for day in range(0, days):
    new_map: dict[int, int] = dict()
    for i in range(0, 8):
        new_map[i] = fish_map[i + 1]
    new_map[6] += fish_map[0]
    new_map[8] = fish_map[0]
    fish_map = new_map

print(f'Part 1: {sum(value for value in fish_map.values())}')

