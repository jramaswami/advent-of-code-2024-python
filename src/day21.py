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


def get_locations(grid):
    locations = dict()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != '.':
                locations[val] = Vector(r, c)
    return locations


NUMBER_PAD = '789\n456\n123\n.0A'.split('\n')
DIRECTION_PAD = '.^A\n<v>'.split('\n')
NUMBER_PAD_LOCATIONS = get_locations(NUMBER_PAD)
DIRECTION_PAD_LOCATIONS = get_locations(DIRECTION_PAD)


def check_path(grid, origin, dest, path):
    curr = origin
    if grid[curr.row][curr.col] == '.':
        return False
    for d in path:
        curr = curr + OFFSETS[d]
        if grid[curr.row][curr.col] == '.':
            return False
    return curr == dest


def grid_paths(grid, origin, dest):
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
    if check_path(grid, origin, dest, path):
        yield path
    path = path[::-1]
    if check_path(grid, origin, dest, path):
        yield path


def code_from_path(path, grid, locations):
    code = []
    curr_posn = locations['A']
    for p in path:
        if p == 'A':
            code.append(grid[curr_posn.row][curr_posn.col])
        else:
            curr_posn = curr_posn + OFFSETS[p]
    return ''.join(code)


def all_paths(grid_name, prev_key, prev_code):
    """Return all the possible codes that come from starting at prev_key
    and produced from the prev_code

    Use BFS to produce the codes.
    """
    result = []

    # Choose grid and locations
    if grid_name == 'd':
        grid = DIRECTION_PAD
        locations = DIRECTION_PAD_LOCATIONS
    else:
        grid = NUMBER_PAD
        locations = NUMBER_PAD_LOCATIONS

    # Queue = (prev key, curr code acc)
    curr_queue = set()
    curr_queue.add((prev_key, ''))
    next_queue = set()
    for i in range(len(prev_code)):
        for prev_key, acc in curr_queue:
            curr_key = prev_code[i]
            origin = locations[prev_key]
            dest = locations[curr_key]
            for pt in grid_paths(grid, origin, dest):
                next_queue.add((curr_key, acc + pt))
        curr_queue, next_queue = next_queue, set()
    return tuple(''.join(x[1]) for x in curr_queue)


def robot(grid_name, prev_codes):
    result = []
    for prev_code in prev_codes:
        prev_key = 'A'
        result.extend(all_paths(grid_name, prev_key, prev_code))
    return result


def solve1(codes):
    robot1 = robot('n', [codes[0]])
    print(robot1)
    robot2 = []
    for pt in robot1:
        print(pt, '->', robot('d', pt))


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