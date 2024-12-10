from aoc.input import read_input


def parse_space(line: str) -> list[int | None]:
    blocks = []
    for pos, char in enumerate(line):
        if pos % 2 == 0:
            blocks += [pos // 2] * int(char)
        else:
            blocks += [None] * int(char)
    return blocks


def defragment(blocks: list[int | None]) -> list[int]:
    result = []
    end_index = len(blocks)
    for index, block in enumerate(blocks):
        if index >= end_index:
            break
        if block is not None:
            result.append(block)
        else:
            end_index -= 1
            while blocks[end_index] is None:
                end_index -= 1
            result.append(blocks[end_index])
    return result


def defragment2(blocks: list[int | None]) -> list[int | None]:
    end = len(blocks) - 1
    while blocks[end] != 0:
        while blocks[end] is None:
            end -= 1
        if blocks[end] == 0:
            break
        end_start = end
        while blocks[end_start] == blocks[end_start - 1]:
            end_start -= 1
        block_size = end - end_start + 1
        start = blocks.index(None)
        while start < end_start and start != -1:
            empty_block_size = 1
            for i in range(start + 1, end_start):
                if blocks[i] is not None:
                    break
                empty_block_size += 1
            if empty_block_size >= block_size:
                for i in range(block_size):
                    blocks[start + i] = blocks[end_start + i]
                    blocks[end_start + i] = None
                break
            start = blocks.index(None, start + empty_block_size)
        end -= block_size
    return blocks


def calculate_checksum(blocks: list[int | None]) -> int:
    checksum = 0
    for index, block in enumerate(blocks):
        if block is not None:
            checksum += index * block
    return checksum


_lines = read_input(True)
print('Part 1:', calculate_checksum(defragment(parse_space(_lines[0]))))
print('Part 2:', calculate_checksum(defragment2(parse_space(_lines[0]))))
