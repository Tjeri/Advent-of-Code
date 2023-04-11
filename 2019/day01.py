from aoc.input import read_input


def calculate_fuel(mass: int) -> int:
    return max(mass // 3 - 2, 0)


def calculate_total_fuel(mass: int) -> int:
    total_fuel = 0
    while mass > 0:
        fuel = calculate_fuel(mass)
        mass = fuel
        total_fuel += fuel
    return total_fuel


_lines = [int(_line) for _line in read_input()]

print(f'Part 1: {sum(calculate_fuel(_line) for _line in _lines)}')
print(f'Part 2: {sum(calculate_total_fuel(_line) for _line in _lines)}')
