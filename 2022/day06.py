with open('../data/2022/day06.txt') as file:
    line = file.readline().strip()


def get_marker_position(length: int) -> int:
    for i in range(len(line)):
        if len(set(line[i:i + length])) == length:
            return i + length


print(f'Part 1: {get_marker_position(4)}')
print(f'Part 2: {get_marker_position(14)}')
