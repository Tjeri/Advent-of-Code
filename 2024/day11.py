from functools import cache

from aoc.input import read_input


@cache
def modify(number: int) -> list[int]:
    if number == 0:
        return [1]
    string = str(number)
    if len(string) % 2 == 0:
        return [int(string[:len(string) // 2]), int(string[len(string) // 2:])]
    return [number * 2024]


def blink(numbers: list[int]) -> list[int]:
    result = []
    for number in numbers:
        result += modify(number)
    return result


def blink2(numbers: dict[int, int]) -> dict[int, int]:
    result = dict()
    for number, amount in numbers.items():
        new_numbers = modify(number)
        for new_number in new_numbers:
            result.setdefault(new_number, 0)
            result[new_number] += amount
    return result


_lines = read_input(True)
_numbers = list(map(int, _lines[0].split(' ')))
for i in range(25):
    _numbers = blink(_numbers)
print('Part 1:', len(_numbers))

_numbers2 = dict()
for _number in list(map(int, _lines[0].split(' '))):
    _numbers2.setdefault(_number, 0)
    _numbers2[_number] += 1

for i in range(75):
    print(i)
    _numbers2 = blink2(_numbers2)
print('Part 2:', sum(_numbers2.values()))
