import sys
sys.path.append('..')

from aoc.input import read_input

def find_max(numbers: list[int], min_index: int, max_index: int) -> tuple[int, int]:
    max = 0
    max_i = -1
    for i, num in enumerate(numbers[min_index:max_index]):
        if num == 9:
            return num, i + min_index
        if num > max:
            max = num
            max_i = i
    return max, max_i + min_index

def find_best(rows: list[list[int]], per_row: int) -> int:
    result = 0
    for row in rows:
        best = []
        last_index = -1
        for i in range(per_row):
            max, index = find_max(row, last_index + 1, len(row) - per_row + i + 1)
            best.append(max)
            last_index = index
        row_result = 0
        for max in best:
            row_result *= 10
            row_result += max
        result += row_result
    return result


_lines = read_input(True)
_numbers = [list(map(int, _line)) for _line in _lines]

print(f'Part 1: {find_best(_numbers, 2)}')
print(f'Part 2: {find_best(_numbers, 12)}')


