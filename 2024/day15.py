from aoc.coord2d.point import Point
from aoc.input import read_split_input


def parse_map(lines: list[str]):
    walls: set[Point] = set()
    boxes: set[Point] = set()
    robot: Point | None = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                walls.add(Point(x, y))
            elif char == 'O':
                boxes.add(Point(x, y))
            elif char == '@':
                robot = Point(x, y)
    if robot is None:
        raise ValueError('Robot not found')
    return walls, boxes, robot


def part1(walls, boxes, robot, moves: str):
    for char in moves:
        move = dir_map[char]
        if robot + move in walls:
            continue
        if robot + move in boxes:
            i = 1
            while robot + (i + 1) * move in boxes:
                i += 1
            if robot + (i + 1) * move in walls:
                continue
            for j in range(i, 0, -1):
                boxes.remove(robot + j * move)
                boxes.add(robot + (j + 1) * move)
            robot += move
        else:
            robot += move
    score = 0
    for box in boxes:
        score += 100 * box.y + box.x
    return score


def parse_map2(lines: list[str]):
    walls: set[Point] = set()
    boxes: dict[Point, tuple[Point, Point]] = {}
    robot: Point | None = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                walls.add(Point(x * 2, y))
                walls.add(Point(x * 2 + 1, y))
            elif char == 'O':
                first, second = Point(x * 2, y), Point(x * 2 + 1, y)
                boxes[first] = (first, second)
                boxes[second] = (first, second)
            elif char == '@':
                robot = Point(x * 2, y)
    if robot is None:
        raise ValueError('Robot not found')
    return walls, boxes, robot


def part2(walls: set[Point], boxes: dict[Point, tuple[Point, Point]], robot: Point, moves: str):
    for char in moves:
        move = dir_map[char]
        new_pos = robot + move
        if new_pos in walls:
            continue
        if new_pos in boxes:
            move_boxes = []
            do_move = []
            box1, box2 = boxes[new_pos]
            move_boxes += [box1, box2]
            do_move.append(box1)
            while move_boxes:
                box = move_boxes.pop(0)
                box_move = box + move
                if box_move in boxes:
                    box3, box4 = boxes[box_move]
                    if box3 in do_move:
                        continue
                    move_boxes += [box3, box4]
                    do_move.append(box3)
                if box_move in walls:
                    break
            else:
                robot += move
                for box in reversed(do_move):
                    box1, box2 = boxes[box]
                    box1_new, box2_new = box1 + move, box2 + move
                    boxes.pop(box1)
                    boxes.pop(box2)
                    boxes[box1_new] = (box1_new, box2_new)
                    boxes[box2_new] = (box1_new, box2_new)
        else:
            robot += move
    score = 0
    for box in boxes:
        if box == boxes[box][0]:
            score += 100 * box.y + box.x
    return score


dir_map = {'^': Point(0, -1), '>': Point(1, 0), 'v': Point(0, 1), '<': Point(-1, 0)}
_map, _moves = read_split_input(True)
_walls, _boxes, _robot = parse_map(_map)
print('Part 1:', part1(_walls, _boxes, _robot, ''.join(_moves)))
_walls, _boxes, _robot = parse_map2(_map)
print('Part 2:', part2(_walls, _boxes, _robot, ''.join(_moves)))
