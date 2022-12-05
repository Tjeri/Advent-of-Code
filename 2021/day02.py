movements = []
with open('../data/2021/day02.txt') as file:
    for line in file.readlines():
        movements.append(line)

horizontal = 0
depth = 0

for movement in movements:
    match movement.split(' '):
        case 'forward', x:
            horizontal += int(x)
        case 'down', z:
            depth += int(z)
        case 'up', z:
            depth -= int(z)
        case _:
            raise ValueError(movement)

print(f'Part 1: {horizontal * depth}')

horizontal = 0
depth = 0
aim = 0

for movement in movements:
    match movement.split(' '):
        case 'forward', x:
            x = int(x)
            horizontal += x
            depth += x * aim
        case 'down', z:
            aim += int(z)
        case 'up', z:
            aim -= int(z)
        case _:
            raise ValueError(movement)

print(f'Part 2: {horizontal * depth}')
