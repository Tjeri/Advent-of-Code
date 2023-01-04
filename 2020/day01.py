from aoc.input import read_input


def check_numbers_1() -> int:
    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == 2020:
                return numbers[i] * numbers[j]


def check_numbers_2() -> int:
    for i in range(len(numbers) - 2):
        for j in range(i + 1, len(numbers) - 1):
            for k in range(j + 1, len(numbers)):
                if numbers[i] + numbers[j] + numbers[k] == 2020:
                    return numbers[i] * numbers[j] * numbers[k]


numbers = list(map(int, read_input()))
print(f'Part 1: {check_numbers_1()}')
print(f'Part 2: {check_numbers_2()}')
