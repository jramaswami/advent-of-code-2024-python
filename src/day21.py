import collections
import dataclasses
import functools
import heapq
import math
import os
import sys

import pyperclip


@dataclasses.dataclass(frozen = True)
class Vector:
    row :int
    col :int

    def __add__(self, other):
        return Vector(self.row + other.row, self.col + other.col)

    def manhattan_distance(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        data = tuple(line.strip() for line in infile if line.strip())
    return data


def parse_expected(filepath):
    """Parse result file and return a dictionary where the key
    is the code and the value is the length of the expected sequence
    after three translations.
    """
    data = {}
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:
                code, sequence = line.split(': ')
                data[code] = len(sequence.strip())
    return data


OFFSETS = {
    '^': Vector(-1, 0),
    'v': Vector(1, 0),
    '<': Vector(0, -1),
    '>': Vector(0, 1)
}


NUMBER_PAD = '789\n456\n123\n.0A'.split('\n')
DIRECTION_PAD = '.^A\n<v>'.split('\n')


def check_path(grid, origin, dest, path):
    curr = origin
    if grid[curr.row][curr.col] == '.':
        return False
    for d in path:
        curr = curr + OFFSETS[d]
        if grid[curr.row][curr.col] == '.':
            return False
    return curr == dest


def grid_path(grid, origin, dest):
    # The path should be the manhattan distance
    dr = dest.row - origin.row
    dc = dest.col - origin.col
    path = []
    if dr < 0:
        path.append('^' * abs(dr))
    elif dr > 0:
        path.append('v' * dr)
    if dc < 0:
        path.append('<' * abs(dc))
    elif dc > 0:
        path.append('>' * dc)
    path = ''.join(path)
    if not check_path(grid, origin, dest, path):
        path = path[::-1]
        assert check_path(grid, origin, dest, path)
    return path


def code_from_path(path, grid, locations):
    code = []
    curr_posn = locations['A']
    for p in path:
        if p == 'A':
            code.append(grid[curr_posn.row][curr_posn.col])
        else:
            curr_posn = curr_posn + OFFSETS[p]
    return ''.join(code)


def solve1(codes):
    np_locations = dict()
    for r, row in enumerate(NUMBER_PAD):
        for c, val in enumerate(row):
            if val != '.':
                np_locations[val] = Vector(r, c)

    dp_locations = dict()
    for r, row in enumerate(DIRECTION_PAD):
        for c, val in enumerate(row):
            if val != '.':
                dp_locations[val] = Vector(r, c)

    # Robot 1
    robot1 = []
    for code in codes:
        path = []
        curr_key = 'A'
        for next_key in code:
            # Move to next key
            origin = np_locations[curr_key]
            dest = np_locations[next_key]
            p = grid_path(NUMBER_PAD, origin, dest)
            # print(curr_key, next_key, p)
            path.append(p)
            # Press A
            path.append('A')
            curr_key = next_key
        path = ''.join(path)
        assert code == code_from_path(path, NUMBER_PAD, np_locations)
        robot1.append(path)

    # Robot 2
    robot2 = []
    for i, code in enumerate(robot1):
        path = []
        curr_key = 'A'
        for next_key in code:
            # Move to next key
            origin = dp_locations[curr_key]
            dest = dp_locations[next_key]
            p = grid_path(DIRECTION_PAD, origin, dest)
            path.append(p)
            # Press A
            path.append('A')
            curr_key = next_key
        path = ''.join(path)
        assert code == code_from_path(path, DIRECTION_PAD, dp_locations)
        robot2.append(path)

    # Robot 3
    robot3 = []
    for i, code in enumerate(robot2):
        path = []
        curr_key = 'A'
        for next_key in code:
            # Move to next key
            origin = dp_locations[curr_key]
            dest = dp_locations[next_key]
            p = grid_path(DIRECTION_PAD, origin, dest)
            path.append(p)
            # Press A
            path.append('A')
            curr_key = next_key
        path = ''.join(path)
        assert code == code_from_path(path, DIRECTION_PAD, dp_locations)
        robot3.append(path)

    soln = 0
    for code, path in zip(codes, robot3):
        numeric_code = int(code[:-1])
        path_length = len(path)
        soln += (numeric_code * path_length)
    return soln


def main():
    "Main program"
    codes = parse_input(os.path.join('data', 'test21a.txt'))
    codes = parse_input(os.path.join('data', 'input21.txt'))
    soln = solve1(codes)
    print('Part 1:', soln)
    pyperclip.copy(soln)
    # 218302 is too high

if __name__ == '__main__':
    sys.exit(main())