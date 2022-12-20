from copy import copy
from typing import TypeVar

TNumber = TypeVar('TNumber', bound='Number')


class Number:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)


class DecryptedNumber(Number):
    decrypted_value: int

    def __init__(self, value: int, mod: int) -> None:
        self.decrypted_value = value * decryption_key
        super().__init__(self.decrypted_value % mod)

    def __str__(self) -> str:
        return str(self.decrypted_value)

    def __repr__(self) -> str:
        return str(self)


def read_numbers() -> list[Number]:
    numbers: list[Number] = list()
    with open(path) as file:
        for line in file.readlines():
            numbers.append(Number(int(line.strip())))
    return numbers


def mix_numbers(numbers: list[TNumber], amount: int = 1) -> list[TNumber]:
    result = copy(numbers)
    mod = len(numbers) - 1
    for _ in range(amount):
        for number in numbers:
            index = result.index(number)
            new_index = index + number.value
            new_index = new_index % mod
            result.pop(index)
            result.insert(new_index, number)
    return result


def apply_decryption_key(numbers: list[Number]) -> list[DecryptedNumber]:
    mod = len(numbers) - 1
    return [DecryptedNumber(number.value, mod) for number in numbers]


def part1(numbers: list[Number]) -> int:
    def get_value(offset: int) -> int:
        return numbers[(zero_index + offset) % len(numbers)].value

    for zero_index in range(len(numbers)):
        if numbers[zero_index].value == 0:
            break
    return get_value(1000) + get_value(2000) + get_value(3000)


def part2(numbers: list[DecryptedNumber]) -> int:
    def get_value(offset: int) -> int:
        return numbers[(zero_index + offset) % len(numbers)].decrypted_value

    for zero_index in range(len(numbers)):
        if numbers[zero_index].decrypted_value == 0:
            break
    return get_value(1000) + get_value(2000) + get_value(3000)


path = '../data/2022/day20.txt'
decryption_key = 811_589_153

_numbers = read_numbers()

_mixed = mix_numbers(_numbers)
print(f'Part 1: {part1(_mixed)}')

_decrypted = apply_decryption_key(_numbers)
_mixed = mix_numbers(_decrypted, 10)
print(f'Part 2: {part2(_mixed)}')
