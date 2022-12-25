import numpy


def snafu_to_decimal(snafu: str) -> int:
    base_5 = ''
    subtract = False
    for i in range(len(snafu) - 1, -1, -1):
        num = -1 if subtract else 0
        subtract = False
        if snafu[i] == '=':
            num += 3
            subtract = True
        elif snafu[i] == '-':
            num += 4
            subtract = True
        else:
            num += int(snafu[i])
        if num < 0:
            num += 5
            subtract = True
        base_5 = f'{num}{base_5}'
    return int(base_5, 5)


def decimal_to_snafu(decimal: int) -> str:
    base_5 = numpy.base_repr(decimal, 5)
    snafu = ''
    add = False
    for i in range(len(base_5) - 1, -1, -1):
        num = int(base_5[i])
        if add:
            num += 1
            add = False
        if num >= 5:
            num -= 5
            add = True
        if num <= 2:
            snafu = f'{num}{snafu}'
        elif num == 3:
            snafu = f'={snafu}'
            add = True
        elif num == 4:
            snafu = f'-{snafu}'
            add = True
    if add:
        snafu = f'1{snafu}'
    return snafu


fuel_requirements: list[int] = list()
with open('../data/2022/day25.txt') as file:
    for _line in file.readlines():
        fuel_requirements.append(snafu_to_decimal(_line.strip()))

print(f'Part 1: {decimal_to_snafu(sum(fuel_requirements))}')
