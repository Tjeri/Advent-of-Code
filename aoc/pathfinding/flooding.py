def flood(flood_map: list[list[str]], block_inner: set[str], replace_outer_with: str) -> None:
    width = len(flood_map[0])
    height = len(flood_map)
    check = ({(x, 0) for x in range(width)}
             | {(x, height - 1) for x in range(width)}
             | {(0, y) for y in range(height)}
             | {(width - 1, y) for y in range(height)})
    while check:
        x, y = check.pop()
        char = flood_map[y][x]
        if char in block_inner or char == replace_outer_with:
            continue
        flood_map[y][x] = replace_outer_with
        if x > 0:
            check.add((x - 1, y))
        if x < width - 1:
            check.add((x + 1, y))
        if y > 0:
            check.add((x, y - 1))
        if y < height - 1:
            check.add((x, y + 1))
