import os
import sys

import pyperclip


class Direction:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __repr__(self):
        return f'Direction({self.row}, {self.column})'


class Box1:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __repr__(self):
        return f'Box1({self.row}, {self.column})'


class Wall:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __repr__(self):
        return f'Wall({self.row}, {self.column})'


class Robot:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __repr__(self):
        return f'Robot({self.row}, {self.column})'


def can_move(item, direction, items):
    if isinstance(item, Wall):
        return False

    r0, c0 = item.row + direction.row, item.column + direction.column
    result = True
    for item0 in items:
        if item0.row == r0 and item0.column == c0:
            result = result and can_move(item0, direction, items)
    return result


def move(item, direction, items):
    assert not isinstance(item, Wall)
    r0, c0 = item.row + direction.row, item.column + direction.column
    for item0 in items:
        if item0.row == r0 and item0.column == c0:
            move(item0, direction, items)
    assert not any(item.row == r0 and item.column == c0 for item in items)
    item.row = r0
    item.column = c0


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        lines = [line.strip() for line in infile]

    grid = []
    instructions = []
    reading = 'grid'
    for line in lines:
        if not line:
            reading = 'instructions'
        elif reading == 'grid':
            grid.append(tuple(line))
        elif reading == 'instructions':
            instructions.extend(list(line))
    return tuple(grid), tuple(instructions)


def make_grid(items, robot, N, M):
    grid0 = [['.' for _ in range(M)] for _ in range(M)]
    for item in items:
        if isinstance(item, Wall):
            grid0[item.row][item.column] = '#'
        elif isinstance(item, Box1):
            grid0[item.row][item.column] = 'O'
    grid0[robot.row][robot.column] = '@'
    return '\n'.join(''.join(row) for row in grid0)


def solve1(grid, instructions):
    N, M = len(grid), len(grid[0])
    # Find items
    robot = None
    items = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '@':
                robot = Robot(r, c)
            elif val == '#':
                items.append(Wall(r, c))
            elif val == 'O':
                items.append(Box1(r, c))

    assert robot
    assert items
    directions = {
        '>': Direction(0, 1),
        '<': Direction(0, -1),
        '^': Direction(-1, 0),
        'v': Direction(1, 0)
    }

    print(make_grid(items, robot, N, M))
    for i, instruction in enumerate(instructions):
        print(i, instruction, robot)
        direction = directions[instruction]
        if can_move(robot, direction, items):
            move(robot, direction, items)
        print(make_grid(items, robot, N, M))

    soln = 0
    for item in items:
        if isinstance(item, Box1):
            soln += (100 * item.row) + item.column
    return soln


def test_solve1():
    grid, instructions = parse_input(os.path.join('data', 'test15a.txt'))
    assert solve1(grid, instructions) == 2028
    grid, instructions = parse_input(os.path.join('data', 'test15b.txt'))
    assert solve1(grid, instructions) == 10092


def main():
    "Main program"
    # Configure logging
    grid, instructions = parse_input(os.path.join('data', 'input15.txt'))
    # grid, instructions = parse_input(os.path.join('data', 'test15a.txt'))
    soln = solve1(grid, instructions)
    print('Part 1:', soln)
    assert soln == 1509863
    # pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())