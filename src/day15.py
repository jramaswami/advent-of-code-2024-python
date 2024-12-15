import os
import sys

import pyperclip


class Direction:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __repr__(self):
        return f'Direction({self.row}, {self.column})'


class Box1:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def can_move(self, direction, items):
        r0, c0 = self.row + direction.row, self.column + direction.column
        result = True
        for item in items:
            if item.collides(r0, c0):
                result = result and item.can_move(direction, items)
        return result

    def move(self, direction, items):
        r0, c0 = self.row + direction.row, self.column + direction.column
        for item in items:
            if item.collides(r0, c0):
                item.move(direction, items)
        assert not any(item.collides(r0, c0) for item in items)
        self.row = r0
        self.column = c0

    def collides(self, r, c):
        return r == self.row and c == self.column

    def __repr__(self):
        return f'Box1({self.row}, {self.column})'


class Box2:
    def __init__(self, r, c):
        self.row = r
        self.column1 = c
        self.column2 = c + 1

    def can_move(self, direction, items):
        # print(f'Box2 can_move({self}, {direction}, ...)')
        if direction == Direction(r=0, c=1):
            # Right
            r0, c0 = self.row + direction.row, self.column2 + direction.column
            result = True
            for item in items:
                if item.collides(r0, c0):
                    result = result and item.can_move(direction, items)
            return result
        elif direction == Direction(r=0, c=-1):
            # Left
            r0, c0 = self.row + direction.row, self.column1 + direction.column
            result = True
            for item in items:
                if item.collides(r0, c0):
                    result = result and item.can_move(direction, items)
            return result
        elif direction == Direction(r=1, c=0):
            r0, c0, c1 = self.row + direction.row, self.column1 + direction.column, self.column2 + direction.column
            result = True
            for item in items:
                if item.collides(r0, c0) or item.collides(r0, c1):
                    result = result and item.can_move(direction, items)
            return result
        elif direction == Direction(r=-1, c=0):
            r0, c0, c1 = self.row + direction.row, self.column1 + direction.column, self.column2 + direction.column
            result = True
            for item in items:
                if item.collides(r0, c0) or item.collides(r0, c1):
                    result = result and item.can_move(direction, items)
            return result

    def move(self, direction, items):
        if direction == Direction(r=0, c=1):
            # Right
            r0, c0 = self.row + direction.row, self.column2 + direction.column
            for item in items:
                if item.collides(r0, c0):
                    item.move(direction, items)
            assert not any(item.collides(r0, c0) for item in items)
            self.column1 += 1
            self.column2 += 1
        elif direction == Direction(r=0, c=-1):
            # Left
            r0, c0 = self.row + direction.row, self.column1 + direction.column
            for item in items:
                if item.collides(r0, c0):
                    item.move(direction, items)
            assert not any(item.collides(r0, c0) for item in items)
            self.column1 -= 1
            self.column2 -= 1
        elif direction == Direction(r=1, c=0):
            r0, c0, c1 = self.row + direction.row, self.column1 + direction.column, self.column2 + direction.column
            for item in items:
                if item.collides(r0, c0) or item.collides(r0, c1):
                    item.move(direction, items)
            assert not any(item.collides(r0, c0) or item.collides(r0, c1) for item in items)
            self.row += 1
        elif direction == Direction(r=-1, c=0):
            r0, c0, c1 = self.row + direction.row, self.column1 + direction.column, self.column2 + direction.column
            for item in items:
                if item.collides(r0, c0) or item.collides(r0, c1):
                    item.move(direction, items)
            assert not any(item.collides(r0, c0) or item.collides(r0, c1) for item in items)
            self.row -= 1

    def collides(self, r, c):
        return r == self.row and c in [self.column1, self.column2]

    def __repr__(self):
        return f'Box2({self.row}, [{self.column1}, {self.column2}])'


class Wall:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def can_move(self, direction, items):
        return False

    def move(self, direction, items):
        raise ValueError(f'Cannot move a wall {self}')

    def collides(self, r, c):
        return r == self.row and c == self.column

    def __repr__(self):
        return f'Wall({self.row}, {self.column})'


class Robot:
    def __init__(self, r, c):
        self.row = r
        self.column = c

    def can_move(self, direction, items):
        r0, c0 = self.row + direction.row, self.column + direction.column
        result = True
        for item in items:
            if item.collides(r0, c0):
                result = result and item.can_move(direction, items)
        return result

    def move(self, direction, items):
        r0, c0 = self.row + direction.row, self.column + direction.column
        for item in items:
            if item.collides(r0, c0):
                item.move(direction, items)
        assert not any(item.collides(r0, c0) for item in items)
        self.row = r0
        self.column = c0

    def collides(self, r, c):
        return r == self.row and c == self.column

    def __repr__(self):
        return f'Robot({self.row}, {self.column})'


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
    grid0 = [['.' for _ in range(M)] for _ in range(N)]
    for item in items:
        if isinstance(item, Wall):
            grid0[item.row][item.column] = '#'
        elif isinstance(item, Box1):
            grid0[item.row][item.column] = 'O'
        elif isinstance(item, Box2):
            grid0[item.row][item.column1] = '['
            grid0[item.row][item.column2] = ']'
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
            elif val == '[':
                items.append(Box2(r, c))

    assert robot
    assert items
    directions = {
        '>': Direction(0, 1),
        '<': Direction(0, -1),
        '^': Direction(-1, 0),
        'v': Direction(1, 0)
    }

    # print(make_grid(items, robot, N, M))
    for i, instruction in enumerate(instructions):
        # print(i, instruction, robot)
        direction = directions[instruction]
        if robot.can_move(direction, items):
            robot.move(direction, items)
        # print(make_grid(items, robot, N, M))

    soln = 0
    for item in items:
        if isinstance(item, Box1):
            soln += (100 * item.row) + item.column
        if isinstance(item, Box2):
            soln += (100 * item.row) + item.column1
    return soln


def test_solve1():
    grid, instructions = parse_input(os.path.join('data', 'test15a.txt'))
    assert solve1(grid, instructions) == 2028
    grid, instructions = parse_input(os.path.join('data', 'test15b.txt'))
    assert solve1(grid, instructions) == 10092


def double_grid(grid):
    grid0 = []
    for row in grid:
        row0 = []
        for x in row:
            if x == '#':
                row0.append('#')
                row0.append('#')
            elif x == 'O':
                row0.append('[')
                row0.append(']')
            elif x == '@':
                row0.append('@')
                row0.append('.')
            elif x == '.':
                row0.append('.')
                row0.append('.')
            else:
                raise ValueError(f'Unrecognized map symbol "{x}"')
        grid0.append(tuple(row0))
    return tuple(grid0)


def solve2(grid, instructions):
    grid0 = double_grid(grid)
    return solve1(grid0, instructions)


def test_solve2():
    grid, instructions = parse_input(os.path.join('data', 'test15b.txt'))
    assert solve2(grid, instructions) == 9021


def main():
    "Main program"
    grid, instructions = parse_input(os.path.join('data', 'input15.txt'))
    soln = solve1(grid, instructions)
    print('Part 1:', soln)
    assert soln == 1509863
    soln = solve2(grid, instructions)
    print('Part 2:', soln)
    pyperclip.copy(soln)
    assert soln == 1548815


if __name__ == '__main__':
    sys.exit(main())