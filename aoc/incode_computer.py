from __future__ import annotations

from enum import IntEnum
from typing import Callable, Iterable, Iterator


class State(IntEnum):
    Initialized = 0
    Running = 1
    Input = 2

    Error = 69
    Over = 98
    Exit = 99

    @property
    def finishing(self) -> bool:
        return self in (State.Error, State.Over, State.Exit)


class ParameterMode(IntEnum):
    Position = 0
    Immediate = 1

    @staticmethod
    def parse_modes(digits: str) -> list[ParameterMode]:
        return [ParameterMode(int(digit)) for digit in reversed(digits)]


class OpCode(IntEnum):
    Null = 0
    Add = 1
    Multiply = 2
    Input = 3
    Output = 4
    JumpIfTrue = 5
    JumpIfFalse = 6
    LessThan = 7
    Equals = 8

    Exit = 99


class IntcodeComputer:
    memory: list[int]
    input: Iterator[int]
    output: list[int]
    debug: bool

    state: State = State.Initialized
    position: int = 0
    opcode: OpCode = OpCode.Null
    parameter_modes: list[ParameterMode]

    __opcodes: dict[OpCode, Callable[[], None]]

    def __init__(self, program: list[int], *, debug: bool = False) -> None:
        self.memory = program.copy()
        self.debug = debug

        self.input = iter([])
        self.output = []

        self.parameter_modes = []

        self.__opcodes = {
            OpCode.Add: self.add,
            OpCode.Multiply: self.multiply,
            OpCode.Input: self.read_input,
            OpCode.Output: self.write_output,
            OpCode.JumpIfTrue: self.jump_if_true,
            OpCode.JumpIfFalse: self.jump_if_false,
            OpCode.LessThan: self.less_than,
            OpCode.Equals: self.is_equal
        }

    def replace(self, position: int, value: int) -> IntcodeComputer:
        self.memory[position] = value
        return self

    def debug_print(self, text: str) -> None:
        if self.debug:
            print(text)

    def run(self, program_input: Iterable[int] | None = None) -> None:
        self.state = State.Running
        if program_input is not None:
            self.input = iter(program_input)
        while not self.state.finishing:
            self.read_instruction()
            self.operation()

            if self.state == State.Input:
                return

            if not self.state.finishing and self.position >= len(self.memory):
                self.debug_print('program over')
                self.state = State.Over

    def read_instruction(self) -> None:
        instruction = self.memory[self.next_position()]
        self.opcode = OpCode(int(str(instruction)[-2:]))
        self.parameter_modes = ParameterMode.parse_modes(str(instruction)[:-2].rjust(3, '0'))
        self.debug_print(f'Read instruction: {instruction} as Opcode: {self.opcode.name}, '
                         f'Parameter Modes: {[mode.name for mode in self.parameter_modes]}')

    def operation(self) -> None:
        if self.opcode in self.__opcodes:
            self.__opcodes[self.opcode]()
        elif self.opcode == OpCode.Exit:
            self.debug_print('exit program')
            self.state = State.Exit
        else:
            self.debug_print(f'Error in program: {self.opcode} at {self.position}')
            self.state = State.Error
            raise ValueError(f'Invalid Program, opcode = {self.opcode} at {self.position}')

    def next_position(self) -> int:
        self.position += 1
        return self.position - 1

    def next_parameter_mode(self) -> ParameterMode:
        if self.parameter_modes:
            result = self.parameter_modes[0]
            self.parameter_modes = self.parameter_modes[1:]
            return result
        return ParameterMode.Position

    def get(self) -> int:
        position = self.next_position()
        parameter_mode = self.next_parameter_mode()
        if parameter_mode == ParameterMode.Position:
            self.debug_print(f'Read Pos {self.memory[position]} as {self.memory[self.memory[position]]}')
            return self.memory[self.memory[position]]
        if parameter_mode == ParameterMode.Immediate:
            self.debug_print(f'Read Pos {position} directly as {self.memory[position]}')
            return self.memory[position]
        raise NotImplementedError(f'Parameter Mode {parameter_mode} not implemented.')

    def set(self, value: int) -> None:
        position = self.next_position()
        parameter_mode = self.next_parameter_mode()
        if parameter_mode == ParameterMode.Position:
            self.debug_print(f'Write Pos {self.memory[position]}: {value}')
            self.memory[self.memory[position]] = value
        elif parameter_mode == ParameterMode.Immediate:
            self.debug_print(f'Write Pos {position} directly: {value}')
            self.memory[position] = value
        else:
            raise NotImplementedError(f'Parameter Mode {parameter_mode} not implemented.')

    def add(self) -> None:
        result = self.get() + self.get()
        self.debug_print('Add')
        self.set(result)

    def multiply(self) -> None:
        result = self.get() * self.get()
        self.debug_print('Multiply')
        self.set(result)

    def read_input(self) -> None:
        self.debug_print('Read Input')
        try:
            self.set(next(self.input))
        except StopIteration:
            self.state = State.Input
            self.position -= 1
            return

    def write_output(self) -> None:
        self.output.append(self.get())
        self.debug_print('Write Output')

    def jump_if_true(self) -> None:
        if self.get() != 0:
            self.debug_print('Jump!')
            self.position = self.get()
        else:
            self.debug_print('Stay')
            self.next_position()

    def jump_if_false(self) -> None:
        if self.get() == 0:
            self.debug_print('Jump!')
            self.position = self.get()
        else:
            self.debug_print('Stay')
            self.next_position()

    def less_than(self) -> None:
        is_less_than = self.get() < self.get()
        self.debug_print('Less than')
        self.set(1 if is_less_than else 0)

    def is_equal(self) -> None:
        is_equal = self.get() == self.get()
        self.debug_print('Equals')
        self.set(1 if is_equal else 0)
