rules: dict[str, list[tuple[int, str]] | None] = dict()


def read_rules():
    with open('../data/2020/day07.txt') as file:
        for line in file.readlines():
            line = line.strip()
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


def contains_shiny_gold(bag: str) -> bool:
    if bag == 'shiny gold bag':
        return False
    bag_rules = rules[bag]
    if not bag_rules:
        return False
    for amount, bag_id in bag_rules:
        if bag_id == 'shiny gold bag':
            return True
        if contains_shiny_gold(bag_id):
            return True
    return False


def count_bags_inside(bag: str) -> int:
    bag_rules = rules[bag]
    if not bag_rules:
        return 0
    bags = 0
    for amount, bag_id in bag_rules:
        bags += amount
        bags += amount * count_bags_inside(bag_id)
    return bags


read_rules()

print(f'Part 1: {len([_bag for _bag in rules.keys() if contains_shiny_gold(_bag)])}')
print(f'Part 2: {count_bags_inside("shiny gold bag")}')
