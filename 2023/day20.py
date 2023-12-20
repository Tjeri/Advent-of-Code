from enum import Enum
from math import lcm

from aoc.input import read_input


class Module(Enum):
    FlipFlop = 0
    Conjunction = 1
    Broadcaster = 2


class PulseMachine:
    modules: dict[str, Module]
    flip_flop_outputs: dict[str, list[str]]
    flip_flop_states: dict[str, bool]
    conjunction_outputs: dict[str, list[str]]
    conjunction_inputs: dict[str, dict[str, bool]]
    broadcaster: list[str]

    started_pulses = 0
    low_pulses = 0
    high_pulses = 0

    def __init__(self, lines: list[str]) -> None:
        self.modules = {}
        self.flip_flop_states = {}
        self.flip_flop_outputs = {}
        self.conjunction_inputs = {}
        self.conjunction_outputs = {}
        for line in lines:
            self.parse_module(*line.split(' -> '))
        self.find_conjunction_inputs()

    def is_start_state(self) -> bool:
        ff = not any(self.flip_flop_states.values())
        con = all(not any(d.values()) for d in self.conjunction_inputs.values())
        return ff and con

    def send_pulse(self, sent_true: set[str] | None = None) -> set[str]:
        if sent_true is None:
            sent_true = set()
        result = set()
        self.started_pulses += 1
        pulses: list[tuple[str, str, bool]] = [('button', 'broadcaster', False)]
        while pulses:
            actuator, to, pulse = pulses.pop(0)
            if pulse:
                self.high_pulses += 1
            else:
                self.low_pulses += 1
            module = self.modules.get(to)
            if not module:
                continue
            if module == Module.FlipFlop:
                if pulse:
                    continue
                state = self.flip_flop_states[to]
                self.flip_flop_states[to] = not state
                for out in self.flip_flop_outputs[to]:
                    pulses.append((to, out, not state))
            elif module == Module.Conjunction:
                inputs = self.conjunction_inputs[to]
                inputs[actuator] = pulse
                send = not all(state for state in inputs.values())
                if send and to in sent_true:
                    result.add(to)
                for out in self.conjunction_outputs[to]:
                    pulses.append((to, out, send))
            elif module == Module.Broadcaster:
                for out in self.broadcaster:
                    pulses.append((to, out, pulse))
            else:
                raise ValueError(actuator, to, pulse)
        return result

    def parse_module(self, module: str, output: str) -> None:
        if module == 'broadcaster':
            self.broadcaster = output.split(', ')
            self.modules[module] = Module.Broadcaster
        elif module.startswith('%'):
            module = module[1:]
            self.flip_flop_states[module] = False
            self.flip_flop_outputs[module] = output.split(', ')
            self.modules[module] = Module.FlipFlop
        elif module.startswith('&'):
            module = module[1:]
            self.conjunction_outputs[module] = output.split(', ')
            self.modules[module] = Module.Conjunction
        else:
            raise ValueError(module, output)

    def find_conjunction_inputs(self) -> None:
        for conjunction in self.conjunction_outputs:
            inputs = {}
            for flip_flop, out in self.flip_flop_outputs.items():
                if conjunction in out:
                    inputs[flip_flop] = False
            for con, out in self.conjunction_outputs.items():
                if conjunction in out:
                    inputs[con] = False
            if conjunction in self.broadcaster:
                inputs['broadcaster'] = False
            self.conjunction_inputs[conjunction] = inputs


def part1(lines: list[str]) -> int:
    machine = PulseMachine(lines)
    machine.send_pulse()
    while machine.started_pulses < 1000:
        machine.send_pulse()
    return machine.high_pulses * machine.low_pulses


def part2(lines: list[str]) -> int:
    machine = PulseMachine(lines)
    for conjunction, outputs in machine.conjunction_outputs.items():
        if 'rx' in outputs:
            break
    else:
        raise ValueError
    relevant_modules = set(machine.conjunction_inputs.keys())
    loops = dict()
    while len(loops) < len(relevant_modules):
        result = machine.send_pulse(relevant_modules)
        for module in result:
            if module not in loops:
                loops[module] = machine.started_pulses
    return lcm(*loops.values())


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 2: {part2(_lines)}')
