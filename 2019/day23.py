from aoc.input import read_input
from incode_computer import IntcodeComputer


class Network:
    controllers: dict[int, IntcodeComputer]
    queues: dict[int, list[tuple[int, int]]]

    def __init__(self, program: list[int]) -> None:
        self.controllers = {}
        for i in range(50):
            controller = IntcodeComputer(program)
            controller.run((i,))
            self.controllers[i] = controller
        self.queues = {i: [] for i in range(50)}

    def run(self) -> tuple[int, int]:
        while True:
            for controller in self.controllers.values():
                if controller.output:
                    address, x, y = controller.output[:3]
                    if address == 255:
                        if self.handle_255(x, y):
                            return x, y
                    else:
                        self.queues[address].append((x, y))
                    controller.output = controller.output[3:]
            for address, controller in self.controllers.items():
                queue = self.queues[address]
                if queue:
                    controller.run(queue.pop(0))
                else:
                    controller.run((-1,))
            if all(not controller.output for controller in self.controllers.values()) \
                    and all(not queue for queue in self.queues.values()):
                finished, x, y = self.handle_idle()
                if finished:
                    return x, y

    def handle_255(self, x: int, y: int) -> bool:
        return True

    def handle_idle(self) -> tuple[bool, int, int]:
        raise ValueError('System is idle without handling.')


class Network2(Network):
    nat: tuple[int, int] = -1, -1
    last_sent: tuple[int, int] = -1, -1

    def handle_255(self, x: int, y: int) -> bool:
        self.nat = (x, y)
        return False

    def handle_idle(self) -> tuple[bool, int, int]:
        if self.nat == self.last_sent:
            return True, self.last_sent[0], self.last_sent[1]
        self.last_sent = self.nat
        self.controllers[0].run(self.nat)
        return False, -1, -1


_lines = read_input()
_program = [int(_number) for _number in _lines[0].split(',')]
_network = Network(_program)
print(f'Part 1: {_network.run()[1]}')
_network2 = Network2(_program)
_network2.run()
print(f'Part 2: {_network2.nat[1]}')
