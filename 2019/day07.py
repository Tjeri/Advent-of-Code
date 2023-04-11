import itertools

from aoc.incode_computer import IntcodeComputer, State
from aoc.input import read_input


def amplify(program: list[int], phase_setting_sequence: tuple[int, ...], feedback_loop: bool) -> int:
    value = 0
    computers = [IntcodeComputer(program) for _ in range(len(phase_setting_sequence))]
    for i, phase_setting in enumerate(phase_setting_sequence):
        computers[i].run([phase_setting, value])
        value = computers[i].output[-1]
    if not feedback_loop:
        return value
    while computers[-1].state is State.Input:
        for computer in computers:
            computer.run([value])
            value = computer.output[-1]
    return value


def max_amplification(program: list[int], possible_phase_settings: list[int], feedback_loop: bool) -> int:
    max_signal = 0
    for permutation in itertools.permutations(possible_phase_settings, 5):
        signal = amplify(program, permutation, feedback_loop)
        if signal > max_signal:
            max_signal = signal
    return max_signal


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]

print(f'Part 1: {max_amplification(_program, [0, 1, 2, 3, 4], False)}')
print(f'Part 2: {max_amplification(_program, [5, 6, 7, 8, 9], True)}')
