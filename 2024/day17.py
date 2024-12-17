from aoc.input import read_split_input


class Device:
    A: int = 0
    B: int = 0
    C: int = 0
    Program: list[int]

    pointer: int = 0

    def __init__(self, blocks: list[list[str]]) -> None:
        registers = blocks[0]
        self.A = int(registers[0][registers[0].index(': ') + 2:])
        self.B = int(registers[1][registers[1].index(': ') + 2:])
        self.C = int(registers[2][registers[2].index(': ') + 2:])

        program = blocks[1][0]
        self.Program = list(map(int, program[program.index(': ') + 2:].split(',')))

    @property
    def literal(self) -> int:
        return self.Program[self.pointer + 1]

    @property
    def combo(self):
        literal = self.Program[self.pointer + 1]
        if literal < 4:
            return literal
        if literal == 4:
            return self.A
        if literal == 5:
            return self.B
        if literal == 6:
            return self.C
        raise ValueError(f'Invalid literal for Combo: {literal}')

    def run(self) -> list[int]:
        result = []
        while self.pointer < len(self.Program) - 1:
            opcode = self.Program[self.pointer]
            if opcode == 0:
                self.A = self.A // (2 ** self.combo)
            elif opcode == 1:
                self.B = self.B ^ self.literal
            elif opcode == 2:
                self.B = self.combo % 8
            elif opcode == 3:
                if self.A != 0:
                    self.pointer = self.literal
                    continue
            elif opcode == 4:
                self.B = self.B ^ self.C
            elif opcode == 5:
                result.append(self.combo % 8)
            elif opcode == 6:
                self.B = self.A // (2 ** self.combo)
            elif opcode == 7:
                self.C = self.A // (2 ** self.combo)
            else:
                raise ValueError(opcode)
            self.pointer += 2
        return result


def part1(blocks: list[list[str]]) -> str:
    device = Device(blocks)
    return ','.join(map(str, device.run()))


def part2(blocks: list[list[str]]) -> int:
    device = Device(blocks)
    last_a = 0
    a_range = range(0, 1)
    for i in range(1, len(device.Program) + 1):
        a_range = range(max(last_a * 8, 1), a_range.stop * 8)
        for a in a_range:
            device = Device(blocks)
            device.A = a
            if device.run() == device.Program[-i:]:
                last_a = a
                break
    return last_a


def part2_2(blocks: list[list[str]]) -> int:
    device = Device(blocks)
    possible_as = [0]
    for i in range(1, len(device.Program) + 1):
        new_as = []
        for last_a in possible_as:
            for a in range(max(last_a * 8, 1), (last_a + 1) * 8):
                device = Device(blocks)
                device.A = a
                if device.run() == device.Program[-i:]:
                    new_as.append(a)
        possible_as = new_as
    return min(possible_as)


_blocks = read_split_input(True)
print('Part 1:', part1(_blocks))
# print('Part 2:', part2(_blocks))
print('Part 2:', part2_2(_blocks))
