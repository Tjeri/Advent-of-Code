import operator
from collections.abc import Callable
from functools import reduce
from turtledemo.penrose import start

from aoc.input import read_input
from itertools import count
import z4

Button = tuple[int, ...]
JoltageState = tuple[int, ...]
ButtonState = tuple[JoltageState, int]


class Machine:
    indicator_lights: tuple[bool, ...]
    joltage_levels: JoltageState
    buttons: list[Button]

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

    def calculate_joltage_manual(self, solver_min: int) -> int:
        def get_buttons(index: int) -> list[Button]:
            return [button for button in self.buttons if index in button]

        def joltages_left(state: JoltageState) -> JoltageState:
            return tuple(expected - level for level, expected in zip(state, self.joltage_levels))

        def is_valid(state: JoltageState) -> bool:
            return not any(level > expected for level, expected in zip(state, self.joltage_levels))

        def is_done(state: JoltageState) -> bool:
            return all(level == expected for level, expected in zip(state, self.joltage_levels))

        def add_button_to_state(state: ButtonState, button: Button, amount: int) -> ButtonState:
            return (
                tuple(base + amount if k in button else base for k, base in enumerate(state[0])),
                state[1] + amount
            )

        def press_buttons(amount_needed: int, buttons_to_press: list[Button],
                          base_state: ButtonState, min_presses: int) -> list[ButtonState]:
            if amount_needed == 0:
                return [base_state]
            button = buttons_to_press[0]
            if len(buttons_to_press) == 1:
                state = add_button_to_state(base_state, button, amount_needed)
                if is_valid(state[0]) and state[1] < min_presses:
                    return [state]
                return []

            result = []
            for i in range(amount_needed + 1):
                state = add_button_to_state(base_state, button, i)
                if not is_valid(state[0]) or state[1] >= min_presses:
                    break
                result += press_buttons(amount_needed - i, buttons_to_press[1:], state, min_presses)
            return result

        def fix_joltages(base_state: ButtonState, min_presses: int) -> int:
            left = joltages_left(base_state[0])
            index = min(filter(lambda y: y[1] > 0, enumerate(left)), key=lambda x: get_buttons(x[0]))[0]
            expected = self.joltage_levels[index] - base_state[0][index]
            buttons = get_buttons(index)
            states = press_buttons(expected, buttons, base_state, min_presses)
            for state in states:
                if is_done(state[0]):
                    min_presses = min(min_presses, state[1])
            if index < len(self.joltage_levels):
                for state in states:
                    if state[1] < min_presses:
                        min_presses = min(min_presses, fix_joltages(state, min_presses))
            return min_presses

        return fix_joltages((tuple(0 for _ in self.joltage_levels), 0), solver_min)



_lines = read_input(True)
_machines = [Machine(_line) for _line in _lines]
print(f'Part 1: {sum(_machine.calculate_indicators() for _machine in _machines)}')
print(f'Part 2 (Solver): {sum(_machine.calculate_joltage_solver() for _machine in _machines)}')
# print(f'Part 2 (Manual): {sum(_machine.calculate_joltage_manual() for _machine in _machines)}')
for _i, _machine in enumerate(_machines):
    print(_i)
    print(_machine.calculate_joltage_solver())
    print(_machine.calculate_joltage_manual(_machine.calculate_joltage_solver()))
