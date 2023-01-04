from aoc.input import read_input

Rules = dict[str, list[tuple[int, str]] | None]


def read_rules(lines: list[str]) -> Rules:
    rules = dict()
    for line in lines:
        contain = line.index('contain')
        bag_id = line[:contain - 2]
        if 'no other bags' in line:
            rules[bag_id] = None
        else:
            bag_rules: list[tuple[int, str]] = list()
            for bag in line[contain + 8:-1].split(', '):
                amount, _bag_id = bag.split(' ', maxsplit=1)
                if amount != '1':
                    _bag_id = _bag_id[:-1]
                bag_rules.append((int(amount), _bag_id))
            rules[bag_id] = bag_rules
    return rules


def contains_shiny_gold(bag: str, rules: Rules) -> bool:
    if bag == 'shiny gold bag':
        return False
    bag_rules = rules[bag]
    if not bag_rules:
        return False
    for amount, bag_id in bag_rules:
        if bag_id == 'shiny gold bag':
            return True
        if contains_shiny_gold(bag_id, rules):
            return True
    return False


def count_bags_inside(bag: str, rules: Rules) -> int:
    bag_rules = rules[bag]
    if not bag_rules:
        return 0
    bags = 0
    for amount, bag_id in bag_rules:
        bags += amount
        bags += amount * count_bags_inside(bag_id, rules)
    return bags


_rules = read_rules(read_input())
print(f'Part 1: {len([_bag for _bag in _rules.keys() if contains_shiny_gold(_bag, _rules)])}')
print(f'Part 2: {count_bags_inside("shiny gold bag", _rules)}')
