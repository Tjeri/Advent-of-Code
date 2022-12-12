important_cycles = [20, 60, 100, 140, 180, 220]


class CPU:
    register: list[int]

    def __init__(self) -> None:
        self.register = [1]

    def read_instruction(self, instruction: str) -> None:
        self.register.append(self.register[-1])
        if instruction.startswith('addx'):
            self.register.append(self.register[-1] + int(instruction[5:]))

    def get_signal_strength(self, cycle: int) -> int:
        return cycle * self.register[cycle - 1]

    def get_signal_strengths(self, *cycles: int) -> int:
        return sum(self.get_signal_strength(cycle) for cycle in cycles)

    def draw_crt(self) -> str:
        result = ''
        for pos, value in enumerate(self.register[:-1]):
            mpos = pos % 40
            if pos > 0 and mpos == 0:
                result += '\n'
            if mpos - 1 <= value <= mpos + 1:
                result += '#'
            else:
                result += '.'
        return result


cpu = CPU()
with open('../data/2022/day10.txt') as file:
    for line in file.readlines():
        cpu.read_instruction(line.strip())

print(f'Part 1: {cpu.get_signal_strengths(*important_cycles)}')
# BACEKLHF
print(f'Part 2:\n{cpu.draw_crt()}')
