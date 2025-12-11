import operator
from functools import reduce
from turtledemo.penrose import start

from aoc.input import read_input
from itertools import count
import z4


class Machine:
    indicator_lights: tuple[bool, ...]
    joltage_levels: tuple[int, ...]
    buttons: list[tuple[int, ...]]

    def __init__(self, line: str) -> None:
        self.indicator_lights = tuple(light == '#' for light in line[1:line.index(']')])
        self.joltage_levels = tuple(map(int, line[line.index('{') + 1:line.index('}')].split(',')))
        self.buttons = []
        index = line.find('(')
        while index >= 0:
            end_index = line.find(')', index)
            self.buttons.append(tuple(map(int, line[index + 1:end_index].split(','))))
            index = line.find('(', end_index)

    def calculate_indicators(self) -> int:
        states = {tuple(False for _ in range(len(self.indicator_lights)))}
        for i in count(start=1):
            next_states = set()
            for state in states:
                for button in self.buttons:
                    next_states.add(
                        tuple(
                            not light if i in button else light for (i, light) in enumerate(state)))
            if self.indicator_lights in next_states:
                return i
            states = next_states
        return -1

    def calculate_joltage_solver(self) -> int:
        optimizer = z4.Optimize()
        button_vars = z4.IntVector('b', len(self.buttons))

        for button in button_vars:
            optimizer.add(button >= 0)

        used_buttons = [[] for _ in self.joltage_levels]
        for i, button in enumerate(self.buttons):
            for joltage in button:
                used_buttons[joltage].append(button_vars[i])

        for j, joltage in enumerate(self.joltage_levels):
            optimizer.add(joltage == z4.Sum(used_buttons[j]))

        optimizer.minimize(z4.Sum(button_vars))
        optimizer.check()
        return int(str(optimizer.model().eval(z4.Sum(button_vars))))

    def calculate_joltage_manual(self) -> int:
        def get_buttons(index: int) -> list[tuple[int, ...]]:
            return [button for button in self.buttons if index in button]

        buttons = get_buttons(0)
        expected = self.joltage_levels[0]
        for i in range(expected):
            for j in range(expected - i):
                # automate the looping?
                pass
        # get all buttons for joltage 0
        # split button presses over those buttons and loop
        # go further inside to joltage 1, check what buttons can be pressed there
        # split so it fits with joltage 0 as well
        # go further inside to joltage 2, etc
        # find all results probably? this is the difficult part
        # go deeper until all joltages are done
        # probably needs to be done recursively
        # find minimum presses -> all results, can cancel on any amounts of presses > found minimum

        pass



_lines = read_input(True)
_machines = [Machine(_line) for _line in _lines]
print(f'Part 1: {sum(_machine.calculate_indicators() for _machine in _machines)}')
print(f'Part 2: {sum(_machine.calculate_joltage_solver() for _machine in _machines)}')
