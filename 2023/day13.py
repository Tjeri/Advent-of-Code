from aoc.input import read_split_input


def transpose(block: list[str]) -> list[str]:
    return [''.join(line[x] for line in block) for x in range(len(block[0]))]


def count_str_diffs(str1: str, str2: str) -> int:
    count = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count


def find_mirror(block: list[str], required_diffs: int) -> int:
    for i in range(1, len(block)):
        diffs = 0
        for j in range(0, i):
            if i + j < len(block):
                diffs += count_str_diffs(block[i - j - 1], block[i + j])
            if diffs > required_diffs:
                break
        else:
            if diffs == required_diffs:
                return i


def sum_mirrors(blocks: list[list[str]], str_diffs: int) -> int:
    result = 0
    for block in blocks:
        row = find_mirror(block, str_diffs)
        if row:
            result += 100 * row
            continue
        column = find_mirror(transpose(block), str_diffs)
        if column:
            result += column
            continue
    return result


_blocks = read_split_input(True)
print(f'Part 1: {sum_mirrors(_blocks, 0)}')
print(f'Part 2: {sum_mirrors(_blocks, 1)}')
