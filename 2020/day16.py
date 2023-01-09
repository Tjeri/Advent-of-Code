from aoc.input import read_split_input

Ticket = list[int]
ErrorRate = int


class Rule:
    name: str
    ranges: list[range]

    def __init__(self, line: str) -> None:
        parts = line.split(': ')
        self.name = parts[0]
        ranges = parts[1].split(' or ')
        self.ranges = []
        for _range in ranges:
            start, end = _range.split('-')
            self.ranges.append(range(int(start), int(end) + 1))

    def matches_field(self, field: int) -> bool:
        for _range in self.ranges:
            if field in _range:
                return True
        return False


class TicketSolver:
    rules: list[Rule]
    own_ticket: Ticket
    other_tickets: list[Ticket]
    field_order: list[Rule]

    def __init__(self, line_blocks: list[list[str]]) -> None:
        self.rules = [Rule(line) for line in line_blocks[0]]
        self.own_ticket = self.parse_ticket(line_blocks[1][1])
        self.other_tickets = [self.parse_ticket(line) for line in line_blocks[2][1:]]
        self.field_order = []

    @staticmethod
    def parse_ticket(line: str) -> Ticket:
        return list(map(int, line.split(',')))

    def remove_invalid_tickets(self) -> ErrorRate:
        new_tickets = []
        error_rate = 0
        for ticket in self.other_tickets:
            valid, ticket_error_rate = self.validate_ticket(ticket)
            if valid:
                new_tickets.append(ticket)
            else:
                error_rate += ticket_error_rate
        self.other_tickets = new_tickets
        return error_rate

    def validate_ticket(self, ticket: Ticket) -> tuple[bool, ErrorRate]:
        valid = True
        error_rate = 0
        for field in ticket:
            if not self.find_matching_field_rules(field):
                valid = False
                error_rate += field
        return valid, error_rate

    def solve_field_order(self) -> None:
        field_order = [None for _ in self.rules]
        fitted_rules: set[Rule] = set()

        while None in field_order:
            for i in range(len(field_order)):
                if field_order[i]:
                    continue
                rules: set[Rule] | None = None
                for ticket in self.other_tickets:
                    field = ticket[i]
                    matching = self.find_matching_field_rules(field)
                    matching -= fitted_rules
                    if rules is None:
                        rules = matching
                    else:
                        rules.intersection_update(matching)
                    if len(rules) == 1:
                        break
                if len(rules) == 1:
                    rule, = rules
                    field_order[i] = rule
                    fitted_rules.add(rule)
        self.field_order = field_order

    def find_matching_field_rules(self, field: int) -> set[Rule]:
        fitting = set()
        for rule in self.rules:
            if rule.matches_field(field):
                fitting.add(rule)
        return fitting

    def calculate_part2(self) -> int:
        result = 1
        for i, rule in enumerate(self.field_order):
            if rule.name.startswith('departure'):
                result *= self.own_ticket[i]
        return result


_lines = read_split_input()
solver = TicketSolver(_lines)
print(f'Part 1: {solver.remove_invalid_tickets()}')
solver.solve_field_order()
print(f'Part 2: {solver.calculate_part2()}')
