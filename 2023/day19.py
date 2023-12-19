from typing import Callable

from parse import parse

from aoc.input import read_split_input

var_to_id = {'x': 0, 'm': 1, 'a': 2, 's': 3}
part_pattern = '{{x={:d},m={:d},a={:d},s={:d}}}'
finished = ('A', 'R')
start_range = range(1, 4001)

WorkflowStep = Callable[[tuple[int, int, int, int]], str | None]
Workflow = list[WorkflowStep]
Part = tuple[int, int, int, int]
PartRanges = list[range]


def parse_workflows(lines: list[str]) -> dict[str, Workflow]:
    workflows = {}
    for line in lines:
        _id, workflow = parse_workflow(line)
        workflows[_id] = workflow
    return workflows


def parse_workflow(line: str) -> tuple[str, Workflow]:
    _id, rest = line.split('{')
    rest = rest[:-1]
    workflows = []
    for part in rest.split(','):
        workflows.append(parse_workflow_step(part))
    return _id, workflows


def parse_workflow_step(step: str) -> WorkflowStep:
    if ':' in step:
        condition, result = step.split(':')
        if '>' in condition:
            var, num = condition.split('>')
            return lambda xmas: result if xmas[var_to_id[var]] > int(num) else None
        if '<' in condition:
            var, num = condition.split('<')
            return lambda xmas: result if xmas[var_to_id[var]] < int(num) else None
        raise ValueError(step)
    return lambda xmas: step


def parse_parts(parts: list[str]) -> list[Part]:
    return [parse(part_pattern, part).fixed for part in parts]


def run_workflow(part: Part, workflow: Workflow) -> str | None:
    for step in workflow:
        result = step(part)
        if result is not None:
            return result
    raise ValueError(part, workflow)


def parse_workflows2(workflows: list[str]) -> dict[str, str]:
    result = {}
    for workflow in workflows:
        _id, workflow = workflow.replace('}', '').split('{')
        result[_id] = workflow
    return result


def find_accept_ranges(workflows: dict[str, str]) -> list[PartRanges]:
    steps = [('in', [start_range] * 4)]
    accept = []
    while steps:
        workflow, ranges = steps.pop(0)
        if workflow == 'A':
            accept.append(ranges)
            continue
        if workflow == 'R':
            continue
        steps += next_steps(workflows[workflow], ranges)
    return accept


def next_steps(workflow: str, ranges: PartRanges) -> list[tuple[str, PartRanges]]:
    steps = []
    for step in workflow.split(','):
        next_id, next_range, other_range = parse_step(step, ranges)
        steps.append((next_id, next_range))
        ranges = other_range
    return steps


def parse_step(step: str, ranges: PartRanges) -> tuple[str, PartRanges, PartRanges | None]:
    if step in finished:
        return step, ranges, None
    if ':' not in step:
        return step, ranges, None
    condition, _id = step.split(':')
    greater = '>' in condition
    if greater:
        var, value = condition.split('>')
    else:
        var, value = condition.split('<')
    index = var_to_id[var]
    value = int(value)
    change_range = ranges[index]
    if greater:
        new_range = range(max(change_range.start, value + 1), change_range.stop)
        other_range = range(change_range.start, min(change_range.stop, value + 1))
    else:
        new_range = range(change_range.start, min(change_range.stop, value))
        other_range = range(max(change_range.start, value), change_range.stop)
    before = ranges[:index]
    after = ranges[index + 1:]
    return _id, before + [new_range] + after, before + [other_range] + after


def calculate_possible_accepted_parts(accept_ranges: list[PartRanges]) -> int:
    result = 0
    for ranges in accept_ranges:
        size = 1
        for r in ranges:
            size *= max(r.stop - r.start, 0)
        result += size
    return result


def part1(workflow_lines: list[str], part_lines: list[str]) -> int:
    workflows = parse_workflows(workflow_lines)
    result = 0
    for part in parse_parts(part_lines):
        workflow_id = 'in'
        while workflow_id not in finished:
            workflow_id = run_workflow(part, workflows[workflow_id])
        if workflow_id == 'A':
            result += sum(part)
    return result


def part1_2(workflow_lines: list[str], part_lines: list[str]) -> int:
    result = 0
    accept_ranges = find_accept_ranges(parse_workflows2(workflow_lines))
    for part in parse_parts(part_lines):
        for accepted in accept_ranges:
            for i in range(len(part)):
                if part[i] not in accepted[i]:
                    break
            else:
                result += sum(part)
                break
    return result


def part2(workflow_lines: list[str]) -> int:
    workflows = parse_workflows2(workflow_lines)
    accept = find_accept_ranges(workflows)
    return calculate_possible_accepted_parts(accept)


_workflows, _parts = read_split_input(True)
print(f'Part 1: {part1(_workflows, _parts)}')
print(f'Part 1 (with Part 2 Solution): {part1_2(_workflows, _parts)}')
print(f'Part 2: {part2(_workflows)}')
