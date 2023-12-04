from aoc.input import read_input


class Game:
    id: int
    rounds: list[dict[str, int]]

    def __init__(self, line: str) -> None:
        split1 = line.split(': ')
        self.id = int(split1[0].split(' ')[1])
        self.rounds = [
            {cubes.split(' ')[1]: int(cubes.split(' ')[0]) for cubes in round.split(', ')}
            for round in split1[1].split('; ')
        ]

    def is_possible(self, cubes: dict[str, int]) -> bool:
        for color, amount in cubes.items():
            for round in self.rounds:
                if round.get(color, 0) > amount:
                    return False
        return True

    def get_minimum_possible(self) -> dict[str, int]:
        result = dict()
        for round in self.rounds:
            for color, amount in round.items():
                if result.get(color, 0) < amount:
                    result[color] = amount
        return result

    def get_power(self) -> int:
        power = 1
        for _, amount in self.get_minimum_possible().items():
            power *= amount
        return power


def part1(lines: list[str]) -> int:
    allowed = {'red': 12, 'green': 13, 'blue': 14}
    result = 0
    for line in lines:
        game = Game(line)
        if game.is_possible(allowed):
            result += game.id
    return result


def part2(lines: list[str]) -> int:
    result = 0
    for line in lines:
        game = Game(line)
        result += game.get_power()
    return result


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 2: {part2(_lines)}')
