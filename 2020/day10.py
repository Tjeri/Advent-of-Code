from functools import reduce

from aoc.input import read_input


def convert_to_distance(numbers: list[int]) -> None:
    for i in range(len(numbers) - 1, 0, -1):
        numbers[i] = numbers[i] - numbers[i - 1]


def calculate_part1(distances: list[int]) -> int:
    return len([distance for distance in distances if distance == 1]) \
        * len([distance for distance in distances if distance == 3])


def find_optional_blocks(distances: list[int]) -> list[int]:
    optional_blocks: list[int] = list()
    last_required = 0
    for i in range(1, len(distances)):
        if distances[i] in (0, 3):
            last_required = i
            continue
        if distances[i + 1] == 3:
            if last_required + 1 < i:
                optional_blocks.append(i - last_required - 1)
    return optional_blocks


def calculate_part2(optional_blocks: list[int]) -> int:
    multiplier_map = {1: 2, 2: 4, 3: 7}
    return reduce(int.__mul__, (list(map(lambda a: multiplier_map[a], optional_blocks))))


adapters: list[int] = list(map(int, read_input()))
adapters.append(0)
adapters.append(max(adapters) + 3)
adapters.sort()
convert_to_distance(adapters)
print(f'Part 1: {calculate_part1(adapters)}')
adapters = find_optional_blocks(adapters)
print(f'Part 2: {calculate_part2(adapters)}')
