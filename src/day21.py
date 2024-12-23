import collections
import dataclasses
import functools
import math
import os
import sys

import pyperclip


@dataclasses.dataclass(frozen = True)
class Vector:
    row: int
    col: int

    def __add__(self, other):
        return Vector(self.row + other.row, self.col + other.col)


NUMBER_PAD = tuple('789\n456\n123\n.0A'.split('\n'))
DIRECTION_PAD = tuple('.^A\n<v>'.split('\n'))
OFFSETS = {
    '^': Vector(-1, 0),
    'v': Vector(1, 0),
    '<': Vector(0, -1),
    '>': Vector(0, 1)
}


def is_dot(grid, curr) -> bool:
    """Return True if the curr position in grid is the dot"""
    return grid[curr.row][curr.col] == '.'


def is_valid_path(grid, origin, dest, path) -> bool:
    """Verify that path does not touch the ."""
    curr = origin
    if is_dot(grid, curr):
        return False
    for d in path:
        curr = curr + OFFSETS[d]
        if is_dot(grid, curr):
            return False
    return curr == dest


# Compute the paths in each grid
def compute_all_paths(grid):
    locations = dict()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != '.':
                locations[val] = Vector(r, c)

    all_paths = dict()
    for origin_val, origin_posn in locations.items():
        all_paths[origin_val] = dict()
        for dest_val, dest_posn in locations.items():
            all_paths[origin_val][dest_val] = list()
            # Shortest path between origin and dest will have same up/dn and lf/rt
            # We and do up/dn followed by lf/rt or lf/rt followed by up/dn
            # It is possible that a path might touch the . space, in which case it should be discarded
            dr = dest_posn.row - origin_posn.row
            dc = dest_posn.col - origin_posn.col
            updn = ('^' if dr < 0 else 'v') * abs(dr)
            lfrt = ('<' if dc < 0 else '>') * abs(dc)
            path1 = updn + lfrt
            if is_valid_path(grid, origin_posn, dest_posn, path1):
                # Add pressing A
                all_paths[origin_val][dest_val].append(path1 + 'A')
            path2 = lfrt + updn
            if path2 != path1 and is_valid_path(grid, origin_posn, dest_posn, path2):
                # Add pressing the A
                all_paths[origin_val][dest_val].append(path2 + 'A')
    return all_paths


NP_PATHS = compute_all_paths(NUMBER_PAD)
DP_PATHS = compute_all_paths(DIRECTION_PAD)


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        data = tuple(line.strip() for line in infile if line.strip())
    return data


def paths_between(device_name, prev_key, curr_key):
    """Return list of all the paths between prev_key and curr_key in the given device"""
    if device_name == 'np':
        return NP_PATHS[prev_key][curr_key]
    return DP_PATHS[prev_key][curr_key]


def translate(device_name, code):
    result = []
    # (index into code, acc)
    queue = collections.deque()
    queue.append((0, ''))
    while queue:
        i, acc = queue.popleft()
        if i >= len(code):
            result.append(''.join(acc))
        else:
            prev_key = 'A' if i == 0 else code[i-1]
            curr_key = code[i]
            for path in paths_between(device_name, prev_key, curr_key):
                queue.append((i+1, acc + path))
    return result


def compute_shortest_code(original_code, devices):
    curr_codes = [original_code]
    next_codes = []
    for device in devices:
        for code in curr_codes:
            next_codes.extend(translate(device, code))
        curr_codes, next_codes = next_codes, []
    return min(len(code) for code in curr_codes)


def test_shortest_code():
    devices = ['np', 'dp', 'dp']
    codes = ['029A', '980A', '179A', '456A', '379A']
    expected = [68, 60, 68, 64, 64]
    for code, ex in zip(codes, expected):
        assert compute_shortest_code(code, devices) == ex


def solve1(original_codes):
    soln = 0
    devices = ['np', 'dp', 'dp']
    for original_code in original_codes:
        shortest_code = compute_shortest_code(original_code, devices)
        numeric_code = int(original_code[:-1])
        soln += (shortest_code * numeric_code)
    return soln


def test_solve1():
    codes = ['029A', '980A', '179A', '456A', '379A']
    assert solve1(codes) == 126384


@functools.cache
def get_cost(prev_key, next_key, robot_level, keypad='dp'):
    keypad_paths = NP_PATHS if keypad == 'np' else DP_PATHS
    # Base Case: return the length of the shortest path between prev_key and next_key
    if robot_level == 0:
        return min(len(path) for path in keypad_paths[prev_key][next_key])
    # Recursive Case
    best_cost = math.inf
    for path in keypad_paths[prev_key][next_key]:
        # Start with A
        path = 'A' + path
        cost = 0
        for pk, nk in zip(path[:-1], path[1:]):
            cost += get_cost(pk, nk, robot_level - 1, 'dp')
        best_cost = min(best_cost, cost)
    return best_cost


def get_code_cost(code, robot_level, keypad):
    code = 'A' + code
    cost = 0
    for pk, nk in zip(code[:-1], code[1:]):
        cost += get_cost(pk, nk, robot_level, keypad)
    return cost


def solve2(codes, robot_level=2):
    soln = 0
    for code in codes:
        cost = get_code_cost(code, robot_level, 'np')
        soln += (cost * int(code[:-1]))
    return soln


def main():
    """Main program"""
    codes = parse_input(os.path.join('data', 'input21.txt'))
    soln = solve2(codes, 2)
    print('Part 1:', soln)
    assert soln == 211930
    soln = solve2(codes, 25)
    print('Part 2:', soln)
    assert soln == 263492840501566
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())
