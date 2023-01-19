from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator, Pattern

from aoc.input import read_split_input

split_pattern: Pattern[str] = re.compile(' \\| | ')


def collect_rules(rule_lines: list[str]) -> dict[int, tuple[set[int], str]]:
    rules: dict[int, tuple[set[int], str]] = {}
    for line in rule_lines:
        __id, rule_text = line.split(': ')
        _id = int(__id)
        if '"' in rule_text:
            rules[_id] = (set(), rule_text[1])
            continue
        depends_on = {int(part) for part in re.split(split_pattern, rule_text)}
        rules[_id] = (depends_on, rule_text)
    return rules


def collect_dependencies(rules: dict[int, tuple[set[int], str]]) -> dict[int | None, set[int]]:
    dependencies = {}
    for rule_id, (depends_on, _) in rules.items():
        if not depends_on:
            dependencies.setdefault(None, set()).add(rule_id)
        for dependency_id in depends_on:
            dependencies.setdefault(dependency_id, set()).add(rule_id)
    return dependencies


def replace_regex_rule(rule: str, rules: dict[int, str]) -> str:
    sides = rule.split(' | ')
    replaced = []
    for side in sides:
        replaced.append(''.join([rules[int(_id)] for _id in side.split(' ')]))
    return f'({"|".join(replaced)})'


def build_regex_pattern(rule_lines: list[str]) -> Pattern[str]:
    unfinished_rules = collect_rules(rule_lines)
    dependencies = collect_dependencies(unfinished_rules)
    parsed_rules: dict[int, str] = {}
    for rule_id in dependencies[None]:
        parsed_rules[rule_id] = unfinished_rules[rule_id][1]
        del unfinished_rules[rule_id]
    del dependencies[None]

    ready: list[int] = list(parsed_rules.keys())
    while ready:
        rule_id = ready.pop(0)
        for depending in dependencies.get(rule_id, []):
            depends_on, text = unfinished_rules[depending]
            depends_on.remove(rule_id)
            if not depends_on:
                del unfinished_rules[depending]
                rule = replace_regex_rule(text, parsed_rules)
                parsed_rules[depending] = rule
                ready.append(depending)
    return re.compile(parsed_rules.get(0))


class Matcher(ABC):
    @abstractmethod
    def matches(self, text: str) -> Generator[int, None, None]:
        pass

    def fully_matches(self, text: str) -> bool:
        return any(match for match in self.matches(text) if match == len(text))

    @staticmethod
    def parse_rules(rule_lines: list[str], use_recursive: bool = False) -> dict[int, Matcher]:
        unfinished_rules = collect_rules(rule_lines)
        dependencies = collect_dependencies(unfinished_rules)

        matchers: dict[int, Matcher] = {}
        for rule_id in dependencies[None]:
            matchers[rule_id] = StringMatcher(unfinished_rules[rule_id][1])
            del unfinished_rules[rule_id]
        del dependencies[None]

        ready: list[int] = list(matchers.keys())
        while ready:
            rule_id = ready.pop(0)
            for depending in dependencies.get(rule_id, []):
                depends_on, text = unfinished_rules[depending]
                depends_on.remove(rule_id)
                if not depends_on:
                    del unfinished_rules[depending]
                    matcher = Matcher.parse_rule(text, matchers)
                    if use_recursive:
                        if depending == 8:
                            matcher = RecursiveMatcher8(matcher)
                        elif depending == 11:
                            matcher = RecursiveMatcher11(matcher)
                    matchers[depending] = matcher
                    ready.append(depending)
        return matchers

    @staticmethod
    def parse_rule(rule: str, rules: dict[int, Matcher]) -> Matcher:
        matchers = []
        if '|' in rule:
            for side in rule.split(' | '):
                matchers.append(Matcher.parse_rule(side, rules))
            return OrMatcher(matchers)
        if ' ' in rule:
            for part in rule.split(' '):
                matchers.append(rules[int(part)])
            if all(isinstance(matcher, StringMatcher) for matcher in matchers):
                return StringMatcher(''.join(matcher.match for matcher in matchers))
            return ConcatMatcher(matchers)
        return rules[int(rule)]


@dataclass
class StringMatcher(Matcher):
    match: str

    def matches(self, text: str) -> Generator[int, None, None]:
        if text.startswith(self.match):
            yield len(self.match)


@dataclass
class ConcatMatcher(Matcher):
    matchers: list[Matcher]

    def matches(self, text: str) -> Generator[int, None, None]:
        yield from self.matches_inner(0, text)

    def matches_inner(self, index: int, text: str) -> Generator[int, None, None]:
        if index >= len(self.matchers):
            yield 0
            return
        for match in self.matchers[index].matches(text):
            for next_match in self.matches_inner(index + 1, text[match:]):
                yield match + next_match


@dataclass
class OrMatcher(Matcher):
    matchers: list[Matcher]

    def matches(self, text: str) -> Generator[int, None, None]:
        for matcher in self.matchers:
            yield from matcher.matches(text)


class RecursiveMatcher8(Matcher):
    matcher: Matcher

    def __init__(self, matcher: Matcher) -> None:
        self.matcher = OrMatcher([matcher, ConcatMatcher([matcher, self])])

    def matches(self, text: str) -> Generator[int, None, None]:
        yield from self.matcher.matches(text)


class RecursiveMatcher11(Matcher):
    matcher: Matcher

    def __init__(self, matcher: Matcher) -> None:
        if not isinstance(matcher, ConcatMatcher):
            raise ValueError
        self.matcher = OrMatcher([matcher, ConcatMatcher([matcher.matchers[0], self, matcher.matchers[1]])])

    def matches(self, text: str) -> Generator[int, None, None]:
        yield from self.matcher.matches(text)


def part1_regex(rules_lines: list[str], messages: list[str]) -> int:
    pattern = build_regex_pattern(rules_lines)
    return sum(int(bool(re.fullmatch(pattern, message))) for message in messages)


def part1_custom(rules_line: list[str], messages: list[str]) -> int:
    matcher = Matcher.parse_rules(rules_line)[0]
    matching = 0
    for message in messages:
        if matcher.fully_matches(message):
            matching += 1
    return matching


def part2_custom(rules_line: list[str], messages: list[str]) -> int:
    matcher = Matcher.parse_rules(rules_line, True)[0]
    matching = 0
    for message in messages:
        if matcher.fully_matches(message):
            matching += 1
    return matching


_groups = read_split_input()
print(f'Part 1 (regex): {part1_regex(*_groups)}')
print(f'Part 1 (custom): {part1_custom(*_groups)}')
print(f'Part 2: {part2_custom(*_groups)}')
