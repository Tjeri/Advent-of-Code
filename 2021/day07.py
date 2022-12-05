pmin = 10000
pmax = 0
positions = []
with open('../data/2021/day07.txt') as file:
    for pos_s in file.readline().split(','):
        pos = int(pos_s)
        if pos < pmin:
            pmin = pos
        if pos > pmax:
            pmax = pos
        positions.append(pos)

min_fuel = None
for goal in range(pmin, pmax + 1):
    fuel = sum(abs(pos - goal) for pos in positions)
    if min_fuel is None or fuel < min_fuel:
        min_fuel = fuel
print(f'Part 1: {min_fuel}')

min_fuel = None
for goal in range(pmin, pmax + 1):
    fuel = sum(sum(range(1, abs(pos - goal) + 1)) for pos in positions)
    if min_fuel is None or fuel < min_fuel:
        min_fuel = fuel
print(f'Part 2: {min_fuel}')
