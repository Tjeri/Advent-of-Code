import operator as op
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import reduce
from typing import Type

file_name = '../data/2021/day16.txt'

with open(file_name) as file:
    data = file.readline()

bits = ''
end = 0
for _hex in data:
    for bit in f'{int(_hex, 16):04b}':
        bits += bit
        if bit == '1':
            end = len(bits)


@dataclass
class Packet(ABC):
    version: int

    @property
    @abstractmethod
    def value(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def version_sum(self) -> int:
        raise NotImplementedError


@dataclass
class Literal(Packet):
    _value: int

    @property
    def value(self) -> int:
        return self._value

    @property
    def version_sum(self) -> int:
        return self.version


@dataclass
class Operator(Packet, ABC):
    bit_mode: bool
    subpackets: list[Packet] = field(default_factory=lambda: [])

    @property
    def version_sum(self) -> int:
        return self.version + sum(sub.version_sum for sub in self.subpackets)


class SumOperator(Operator):
    @property
    def value(self) -> int:
        return sum(sub.value for sub in self.subpackets)


class ProductOperator(Operator):
    @property
    def value(self) -> int:
        return reduce(op.mul, [sub.value for sub in self.subpackets])


class MinOperator(Operator):
    @property
    def value(self) -> int:
        return min(sub.value for sub in self.subpackets)


class MaxOperator(Operator):
    @property
    def value(self) -> int:
        return max(sub.value for sub in self.subpackets)


class GreaterThanOperator(Operator):
    @property
    def value(self) -> int:
        return 1 if self.subpackets[0].value > self.subpackets[1].value else 0


class LessThanOperator(Operator):
    @property
    def value(self) -> int:
        return 1 if self.subpackets[0].value < self.subpackets[1].value else 0


class EqualToOperator(Operator):
    @property
    def value(self) -> int:
        return 1 if self.subpackets[0].value == self.subpackets[1].value else 0


type_id_to_class: dict[int, Type[Literal | Operator]] = {
    0: SumOperator,
    1: ProductOperator,
    2: MinOperator,
    3: MaxOperator,
    4: Literal,
    5: GreaterThanOperator,
    6: LessThanOperator,
    7: EqualToOperator
}


def parse_version(index: int) -> tuple[int, int]:
    return index + 3, int(bits[index:index + 3], 2)


def parse_type_id(index: int) -> tuple[int, int]:
    return index + 3, int(bits[index:index + 3], 2)


def parse_literal(index: int) -> tuple[int, int]:
    literal = ''
    while True:
        literal += bits[index + 1: index + 5]
        if bits[index] == '0':
            break
        index += 5
    return index + 5, int(literal, 2)


def parse_operator_type(index: int) -> tuple[int, bool, int]:
    size = 16 if bits[index] == '0' else 12
    return index + size, size == 16, int(bits[index + 1:index + size], 2)


def parse_subpackets(index: int, bit_mode: bool, length: int) -> tuple[int, list[Packet]]:
    subpackets = []
    if bit_mode:
        new_index = index
        while new_index - index < length:
            new_index, subpacket = parse_packet(new_index)
            subpackets.append(subpacket)
        index = new_index
    else:
        while len(subpackets) < length:
            index, subpacket = parse_packet(index)
            subpackets.append(subpacket)
    return index, subpackets


def parse_packet(index: int) -> tuple[int, Packet]:
    index, version = parse_version(index)
    index, type_id = parse_type_id(index)
    packet_class = type_id_to_class[type_id]
    if packet_class is Literal:
        index, literal = parse_literal(index)
        return index, Literal(version, literal)
    index, bit_mode, length = parse_operator_type(index)
    operator = packet_class(version, bit_mode)
    index, subpackets = parse_subpackets(index, bit_mode, length)
    operator.subpackets += subpackets
    return index, operator


packets = []
parse_index = 0
while parse_index < len(bits) and parse_index < end:
    parse_index, packet = parse_packet(parse_index)
    packets.append(packet)

print(f'Part 1: {sum(packet.version_sum for packet in packets)}')
print(f'Part 2: {sum(packet.value for packet in packets)}')
