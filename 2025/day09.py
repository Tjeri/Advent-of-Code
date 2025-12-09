import shapely.geometry as geom

from aoc.coord2d.point import Point
from aoc.input import read_input


def part1(tiles: list[Point]) -> int:
    result = 0
    for i, tile in enumerate(tiles):
        for tile2 in tiles[i + 1:]:
            result = max(result, (abs(tile.x - tile2.x) + 1) * (abs(tile.y - tile2.y) + 1))
    return result


def part2(tiles: list[Point]) -> int:
    tile_polygon = geom.Polygon(geom.Point(tile.x, tile.y) for tile in tiles)

    result = 0
    for i, tile in enumerate(tiles):
        for tile2 in tiles[i + 1:]:
            if tile_polygon.covers(geom.Polygon([
                (tile.x, tile.y),
                (tile.x, tile2.y),
                (tile2.x, tile2.y),
                (tile2.x, tile.y)
            ])):
                result = max(result, (abs(tile.x - tile2.x) + 1) * (abs(tile.y - tile2.y) + 1))
    return result


_lines = read_input(True)
_tiles = [Point(*map(int, _line.split(','))) for _line in _lines]

print(f'Part 1: {part1(_tiles)}')
print(f'Part 2: {part2(_tiles)}')
