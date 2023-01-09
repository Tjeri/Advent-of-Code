import itertools

from aoc.input import read_input


def mask1(value: int, mask: str) -> int:
    binary = list(bin(value))
    while len(binary) < 38:
        binary.insert(2, '0')
    for i in range(36):
        if mask[i] != 'X':
            binary[i + 2] = mask[i]
    return int(''.join(binary), 2)


def mask2(value: int, mask: str) -> list[int]:
    result = []
    binary = list(bin(value))
    while len(binary) < 38:
        binary.insert(2, '0')
    floating = []
    for i in range(36):
        if mask[i] == '0':
            continue
        elif mask[i] == '1':
            binary[i + 2] = mask[i]
        else:
            binary[i + 2] = '0'
            floating.append(i + 2)
    result.append(int(''.join(binary), 2))
    for num in range(1, pow(2, len(floating))):
        binary_mask = bin(num)[2:]
        for i, bit in enumerate(reversed(binary_mask)):
            binary[floating[-1 - i]] = bit
            result.append(int(''.join(binary), 2))
    return result


def decode1(lines: list[str]) -> int:
    memory: dict[int, int] = dict()
    mask: str = 'X' * 36
    for line in lines:
        if line.startswith('mask'):
            mask = line[7:]
        else:
            address_end = line.index(']')
            address = int(line[4:address_end])
            memory[address] = mask1(int(line[address_end + 4:]), mask)
    return sum(memory.values())


def decode2(lines: list[str]) -> int:
    memory: dict[int, int] = dict()
    mask: str = 'X' * 36
    for line in lines:
        if line.startswith('mask'):
            mask = line[7:]
        else:
            address_end = line.index(']')
            addresses = mask2(int(line[4:address_end]), mask)
            value = int(line[address_end + 4:])
            for address in addresses:
                memory[address] = value
    return sum(memory.values())


_lines = read_input()
print(f'Part 1: {decode1(_lines)}')
print(f'Part 2: {decode2(_lines)}')
