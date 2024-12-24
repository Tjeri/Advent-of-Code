from itertools import combinations, permutations
from aoc.input import read_split_input
from aoc.utils.list import flatten


def parse_wires(lines: list[str]) -> dict[str, int]:
  result = {}
  for line in lines:
    name, value = line.split(': ')
    result[name] = int(value)
  return result


def parse_connections(lines: list[str]) -> list[tuple[str, str, str, str]]:
  result = []
  for line in lines:
    condition, output = line.split(' -> ')
    result.append(tuple(condition.split(' ')) + (output,))
  return result


def evaluate_condition(a: int, condition: str, b: int) -> int:
  if condition == 'AND':
    return a & b
  if condition == 'OR':
    return a | b
  if condition == 'XOR':
    return a ^ b
  raise ValueError(f'Invalid condition: {condition}')


def find_binary_number(wires: dict[str, int], start: str) -> int:
  result = []
  for wire in sorted(wires.keys(), reverse=True):
    if wire.startswith(start):
      result.append(str(wires[wire]))
  return int(''.join(result), 2)


def part1(original_wires: dict[str, int], connections: list[tuple[str, str, str, str]]) -> int:
  wires = original_wires.copy()
  changed = True
  while changed:
    changed = False
    for (a, cond, b, out) in connections:
      if a in wires and b in wires:
        new_value = evaluate_condition(wires[a], cond, wires[b])
        if out not in wires or wires[out] != new_value:
          wires[out] = new_value
          changed = True
  return find_binary_number(wires, 'z')


def part2(wires: dict[str, int], connections: list[tuple[str, str, str, str]]):
  def swap(a, b):
    for _a, cond, _b, out in connections:
      if out != a and out != b:
        continue
      for __a, _cond, __b, _out in connections:
        if _out == out:
          continue
        if _out == a or _out == b:
          connections.remove((_a, cond, _b, out))
          connections.remove((__a, _cond, __b, _out))
          connections.append((_a, cond, _b, _out))
          connections.append((__a, _cond, __b, out))
          return

  def get_keys(char: str) -> list[str]:
    result = []
    for wire in wires.keys():
      if wire.startswith(char):
        result.append(wire)
    result.sort()
    return result

  def find_connection(a, b, condition) -> str:
    for _a, cond, _b, out in connections:
      if cond == condition and (_a == a and _b == b or _a == b and _b == a):
        return out

  xs = get_keys('x')
  ys = get_keys('y')
  assert len(xs) == len(ys)

  swaps = [('z06', 'vwr'), ('z11', 'tqm'), ('z16', 'kfs'), ('hcm', 'gfv')]
  for _swap in swaps:
    swap(*_swap)
  last_z_and = None
  last_xor_and = None
  for i, (x, y) in enumerate(zip(xs, ys)):
    xor = find_connection(x, y, 'XOR')
    if i == 0:
      last_z_and = find_connection(x, y, 'AND')
      last_xor_and = last_z_and
      continue
    _or = last_z_and if last_z_and == last_xor_and else find_connection(last_z_and, last_xor_and, 'OR')
    z = find_connection(xor, _or, 'XOR')
    expect_z = f'z{i:02}'
    assert z == expect_z
    last_z_and = find_connection(xor, _or, 'AND')
    last_xor_and = find_connection(x, y, 'AND')
  swap_list = flatten(swaps)
  swap_list.sort()
  return ','.join(swap_list)


_blocks = read_split_input(True)
_wires = parse_wires(_blocks[0])
_connections = parse_connections(_blocks[1])
# print('Part 1:', part1(_wires, _connections))
print('Part 2:', part2(_wires, _connections))
