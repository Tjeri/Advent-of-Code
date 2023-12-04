import math
from typing import NamedTuple

from aoc.input import read_input


class Component(NamedTuple):
    amount: int
    chemical: str


class Reaction(NamedTuple):
    inputs: list[Component]
    output: Component


def parse_reaction(line: str) -> Reaction:
    inputs, output = line.split(' => ')

    input_chemicals = []
    for input_chemical in inputs.split(', '):
        amount, chemical = input_chemical.split(' ')
        input_chemicals.append(Component(int(amount), chemical))
    amount, chemical = output.split(' ')
    return Reaction(input_chemicals, Component(int(amount), chemical))


def consume(component: Component, resources: dict[str, int], reactions: dict[str, Reaction]) -> int:
    available = resources.get(component.chemical, 0)
    missing = component.amount - available
    ores = 0
    if missing > 0:
        ores = produce(Component(missing, component.chemical), resources, reactions)
    resources[component.chemical] -= component.amount
    return ores


def produce(component: Component, resources: dict[str, int], reactions: dict[str, Reaction]) -> int:
    reaction = reactions[component.chemical]
    reaction_amount = math.ceil(component.amount / reaction.output.amount)
    ores = 0
    for input_component in reaction.inputs:
        needed_input_amount = reaction_amount * input_component.amount
        if input_component.chemical == 'ORE':
            resources.setdefault(component.chemical, 0)
            resources[component.chemical] += reaction_amount * reaction.output.amount
            return needed_input_amount
        ores += consume(Component(needed_input_amount, input_component.chemical), resources, reactions)
    resources.setdefault(component.chemical, 0)
    resources[component.chemical] += reaction_amount * reaction.output.amount
    return ores


def maximize_fuel(reactions: dict[str, Reaction], available_ore: int) -> int:
    lower = 1
    upper = available_ore
    while upper - lower > 1:
        middle = (upper + lower) // 2
        needed = produce(Component(middle, 'FUEL'), {}, reactions)
        if needed == available_ore:
            return middle
        if needed > available_ore:
            upper = middle
        else:
            lower = middle
    return lower


_lines = read_input()
_reaction_list = [parse_reaction(_line) for _line in _lines]
_reactions = {_reaction.output.chemical: _reaction for _reaction in _reaction_list}

print(f'Part 1: {produce(Component(1, "FUEL"), {}, _reactions)}')
print(f'Part 2: {maximize_fuel(_reactions, 1_000_000_000_000)}')
