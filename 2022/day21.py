from collections import OrderedDict
from copy import copy

from parse import parse


def solve1(original_lines: OrderedDict[str, str]) -> int:
    lines = copy(original_lines)
    while lines:
        id_, line = lines.popitem(last=False)
        try:
            exec(line)
        except NameError:
            lines[id_] = line
    return eval('root')


def solve2(original_lines: OrderedDict[str, str]) -> int:
    _globals, _locals = globals(), locals()

    def evaluate_possible_terms() -> None:
        seen = set()
        while lines:
            id_, line = lines.popitem(last=False)
            if id_ in seen:
                lines[id_] = line
                break
            seen.add(id_)
            try:
                exec(line, _globals, _locals)
                seen.clear()
            except NameError:
                lines[id_] = line

    def evaluate_root() -> str:
        root = lines.pop('root')
        left, right = root[7:].split(' + ')
        if left in _locals:
            exec(f'{right} = {eval(left, _globals, _locals)}', _globals, _locals)
            return right
        else:
            exec(f'{left} = {eval(right, _globals, _locals)}', _globals, _locals)
            return left

    def evaluate_term(term_id: str) -> str:
        pattern = '{} = {} {} {}'
        term = lines.pop(term_id)
        result, left, op, right = parse(pattern, term)
        result = eval(result, _globals, _locals)
        if left in _locals:
            left = eval(left, _globals, _locals)
            if op == '+':
                exec(f'{right} = {result} - {left}', _globals, _locals)
            elif op == '-':
                exec(f'{right} = {left} - {result}', _globals, _locals)
            elif op == '*':
                exec(f'{right} = {result} / {left}', _globals, _locals)
            elif op == '/':
                exec(f'{right} = {left} / {result}', _globals, _locals)
            else:
                raise ValueError
            return right
        else:
            right = eval(right, _globals, _locals)
            if op == '+':
                exec(f'{left} = {result} - {right}', _globals, _locals)
            elif op == '-':
                exec(f'{left} = {result} + {right}', _globals, _locals)
            elif op == '*':
                exec(f'{left} = {result} / {right}', _globals, _locals)
            elif op == '/':
                exec(f'{left} = {result} * {right}', _globals, _locals)
            else:
                raise ValueError
            return left

    lines = copy(original_lines)
    del lines['humn']
    evaluate_possible_terms()
    next_term = evaluate_root()
    while lines:
        next_term = evaluate_term(next_term)
    return eval('humn')


_lines: OrderedDict[str, str] = OrderedDict()
with open('../data/2022/day21.txt') as file:
    for _line in file.readlines():
        _lines[_line[:4]] = _line.strip().replace(': ', ' = ')

print(f'Part 1: {solve1(_lines)}')
print(f'Part 2: {solve2(_lines)}')
