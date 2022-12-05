from __future__ import annotations

import math

stack_lines = []
stacks = []
stacks_2 = []
with open('../data/2022/day05.txt') as file:
    read_stack = True
    for line in file.readlines():
        if read_stack:
            if len(line) < 3:
                read_stack = False
                for stack in stacks:
                    stack.reverse()
                    stacks_2.append(stack.copy())
                continue
            if len(stacks) == 0:
                for i in range(math.ceil(len(line) / 4)):
                    stacks.append(list())
            if read_stack:
                for i in range(len(line) // 4):
                    char = line[4 * i + 1]
                    if 'A' <= char <= 'Z':
                        stacks[i].append(char)
        else:
            _, _amount, _, _from, _, _to = line.strip().split(' ')
            __from, __to = int(_from) - 1, int(_to) - 1
            crates = list()
            for i in range(int(_amount)):
                stacks[__to].append(stacks[__from].pop())
                crates.insert(0, stacks_2[__from].pop())
            stacks_2[__to] += crates

part_1 = ''.join([stack[-1] for stack in stacks])
print(f'Part 1: {part_1}')
part_2 = ''.join([stack[-1] for stack in stacks_2])
print(f'Part 2: {part_2}')
