from collections.abc import Callable

from aoc.input import read_input


class Console:
    state: dict[str, int]
    code: list[tuple[str, int]]
    visited: set[int]

    def __init__(self, lines: list[str]) -> None:
        self.reset_state()
        self.code = list()
        for line in lines:
            instruction, amount = line.split(' ')
            self.code.append((instruction, int(amount)))

    def reset_state(self) -> None:
        self.state = {'acc': 0, 'jmp': 0, 'nop': 0}
        self.visited = set()

    @property
    def position(self) -> int:
        return self.state['jmp']

    @property
    def accumulator(self) -> int:
        return self.state['acc']

    def change_instruction(self, pos: int, to: str) -> None:
        self.code[pos] = to, self.code[pos][1]

    def run_until_done_or_infinite(self) -> bool:
        while self.position not in self.visited:
            self.visited.add(self.position)
            instruction, amount = self.code[self.position]
            self.state[instruction] += amount
            if instruction != 'jmp':
                self.state['jmp'] += 1
            if self.position >= len(self.code):
                return True
        return False

    def fix(self) -> None:
        for pos in range(len(self.code)):
            self.reset_state()
            if console.code[pos][0] == 'jmp':
                console.change_instruction(pos, 'nop')
                if console.run_until_done_or_infinite():
                    break
                console.change_instruction(pos, 'jmp')
            elif console.code[pos][0] == 'nop':
                console.change_instruction(pos, 'jmp')
                if console.run_until_done_or_infinite():
                    break
                console.change_instruction(pos, 'nop')


console = Console(read_input())
console.run_until_done_or_infinite()
print(f'Part 1: {console.accumulator}')
console.fix()
print(f'Part 2: {console.accumulator}')
