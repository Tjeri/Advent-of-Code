from __future__ import annotations

from aoc.input import read_split_input


class RangeMap:
    source: range
    destination: range

    def __init__(self, line: str) -> None:
        destination, source, length = map(int, line.split(' '))
        self.source = range(source, source + length)
        self.destination = range(destination, destination + length)

    def __str__(self) -> str:
        return f'Map {self.source} to {self.destination}'

    def __lt__(self, other: RangeMap) -> bool:
        return self.source.start < other.source.start

    def map(self, source_range: range) -> tuple[range | None, range | None, range | None]:
        before = range(source_range.start, min(source_range.stop, self.source.start))
        mapped = range(max(source_range.start, self.source.start), min(source_range.stop, self.source.stop))
        after = range(max(source_range.start, self.source.stop), source_range.stop)

        if before.start >= before.stop:
            before = None
        if mapped.start < mapped.stop:
            offset = mapped.start - self.source.start
            start = self.destination.start + offset
            mapped = range(start, start + (mapped.stop - mapped.start))
        else:
            mapped = None
        if after.start >= after.stop:
            after = None

        return before, mapped, after


class Map:
    range_maps: list[RangeMap]

    def __init__(self, lines: list[str]) -> None:
        self.range_maps = []
        for line in lines[1:]:
            self.range_maps.append(RangeMap(line))
        self.range_maps.sort()

    def map(self, source: range) -> list[range]:
        result = []
        for range_map in self.range_maps:
            before, mapped, after = range_map.map(source)
            result.append(before)
            result.append(mapped)
            if after is None:
                break
            source = after
        else:
            result.append(source)
        result = [r for r in result if r]
        result.sort(key=lambda r: r.start)
        return result


def parse_seeds(line: str) -> list[int]:
    return list(map(int, line[7:].strip().split(' ')))


def part1(seeds: list[int], maps: list[Map]) -> int:
    result = None
    for seed in seeds:
        mapped = range(seed, seed + 1)
        for _map in maps:
            mapped = _map.map(mapped)[0]
        if result is None or mapped.start < result:
            result = mapped.start
    return result


def part2(seeds: list[int], maps: list[Map]) -> int:
    seed_ranges = [range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    seed_ranges.sort(key=lambda r: r.start)
    for _map in maps:
        new_ranges = []
        for seed_range in seed_ranges:
            new_ranges += _map.map(seed_range)
        seed_ranges = new_ranges
        seed_ranges.sort(key=lambda r: r.start)
    return seed_ranges[0].start


_blocks = read_split_input(True)
_seeds = parse_seeds(_blocks[0][0])
_maps = [Map(_lines) for _lines in _blocks[1:]]
print(f'Part 1: {part1(_seeds, _maps)}')
print(f'Part 2: {part2(_seeds, _maps)}')
