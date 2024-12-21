import collections
import dataclasses
import functools
import heapq
import math
import os
import sys


@dataclasses.dataclass(frozen = True)
class Vector:
    row :int
    col :int

    def __add__(self, other):
        return Vector(self.row + other.row, self.col + other.col)


################################### KEYPADS ####################################

NUMBER_PAD = tuple(tuple(row) for row in '789\n456\n123\n 0A'.split('\n'))
DIRECTION_PAD = tuple(tuple(row) for row in ' ^A\n<v>'.split('\n'))

NP_LOCATIONS = dict()
for r, row in enumerate(NUMBER_PAD):
    for c, val in enumerate(row):
        if val != ' ':
            NP_LOCATIONS[val] = Vector(r, c)

DP_LOCATIONS = dict()
for r, row in enumerate(DIRECTION_PAD):
    for c, val in enumerate(row):
        if val != ' ':
            DP_LOCATIONS[val] = Vector(r, c)

################################################################################

OFFSETS = (
    (Vector(-1, 0), '^'),
    (Vector(1, 0), 'v'),
    (Vector(0, -1), '<'),
    (Vector(0, 1), '>')
)


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


def inbounds(grid, p):
    return (
        p.row >= 0 and p.row < len(grid) and
        p.col >= 0 and p.col < len(grid[p.row])
    )


def neighbors(grid, p):
    for off, d in OFFSETS:
        p0 = p + off
        if inbounds(grid, p0) and grid[p0.row][p0.col] != ' ':
            yield p0, d


def compute_paths_between(grid, origin, dest):
    """Return all paths from origin to dest that are equal in
    length to the shortest path

    The shortest path is the manhattan distance between the points.
    """
    paths = []
    visited = set()
    max_length = abs(origin.row - dest.row) + abs(origin.col - dest.col)
    def dfs(p, acc):
        if p == dest and len(acc) == max_length:
            paths.append(''.join(acc))
            return

        visited.add(p)
        for p0, d in neighbors(grid, p):
            if p0 not in visited:
                acc.append(d)
                dfs(p0, acc)
                acc.pop()
        visited.remove(p)

    dfs(origin, [])
    return paths


def compute_all_paths_on_grid(grid):
    locations = {}
    all_values = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != ' ':
                all_values.append(val)
                locations[val] = Vector(r, c)
    all_paths_on_grid = dict()
    for origin_value in all_values:
        origin = locations[origin_value]
        all_paths_on_grid[origin_value] = dict()
        for dest_value in all_values:
            dest = locations[dest_value]
            all_paths_on_grid[origin_value][dest_value] = compute_paths_between(grid, origin, dest)
    return all_paths_on_grid


def shortest_paths_number_pad(code, all_paths_on_number_pad):
    curr_queue = set([''])
    next_queue = set()
    curr_key = 'A'
    for next_key in code:
        for p in curr_queue:
            for q in all_paths_on_number_pad[curr_key][next_key]:
                next_queue.add(p + q + 'A')
        curr_key = next_key
        curr_queue, next_queue = next_queue, set()
    return curr_queue


def shortest_paths_on_direction_pad(code, all_paths_on_direction_pad):
    curr_queue = set([''])
    next_queue = set()
    # We are always returning to the A key!
    for next_key in code:
        # First go to that key
        paths_to_next_key = all_paths_on_direction_pad['A'][next_key]
        # Then go back to A key
        paths_to_a_key = all_paths_on_direction_pad[next_key]['A']
        for p in curr_queue:
            for q in paths_to_next_key:
                for r in paths_to_a_key:
                    next_queue.add(p + q + r + 'A')
        curr_queue, next_queue = next_queue, set()
    return curr_queue



def code_sequence_length(code, all_paths_on_number_pad, all_paths_on_direction_pad):
    robot1 = shortest_paths_number_pad(code, all_paths_on_number_pad)

    @functools.cache
    def cost(direction_key, level):
        # print(f'cost({direction_key=}, {level=})')
        if level == 0:
            # Just count the key itself, because this is *my* directional keypad
            return 1
        else:
            result = math.inf
            # Go from A to directon_key
            best_p = math.inf
            for p in all_paths_on_direction_pad['A'][direction_key]:
                # print('Recursing on', p)
                p_cost = 0
                for dk in p:
                    p_cost += cost(dk, level-1)
                best_p = min(p_cost, best_p)
            # print('A ->', direction_key, 'costs', best_p)
            # Push button
            press_button = cost('A', level-1)
            # print ('Pressing button costs', press_button)
            best_p += press_button
            # Go from direction_key to A
            best_q = math.inf
            for q in all_paths_on_direction_pad[direction_key]['A']:
                q_cost = 0
                for dk in q:
                    q_cost += cost(dk, level-1)
                best_q = min(q_cost, best_q)
            # print(direction_key, '-> A', 'costs', best_q)
            # Push button
            best_q += press_button
            # print ('Pressing button costs', press_button)
            result = min(result, best_p + best_q)
        return result

    soln = math.inf
    for p in robot1:
        cost_p = 0
        for a, b in zip(p[:-1], p[1:]):
            min_cost_a_to_b = math.inf
            for a_to_b in all_paths_on_direction_pad[a][b]:
                cost_a_to_b = 0
                for pk in a_to_b:
                    cost_a_to_b += cost(pk, 1)
                min_cost_a_to_b = min(min_cost_a_to_b, cost_a_to_b)
            cost_p += min_cost_a_to_b
        soln = min(soln, cost_p)
    return soln


def solve1(codes):
    all_paths_on_number_pad = compute_all_paths_on_grid(NUMBER_PAD)
    all_paths_on_direction_pad = compute_all_paths_on_grid(DIRECTION_PAD)
    for code in codes:
        soln = code_sequence_length(code, all_paths_on_number_pad, all_paths_on_direction_pad)
        print(code, soln)


def main():
    "Main program"
    codes = parse_input(os.path.join('data', 'test21a.txt'))
    soln = solve1(codes)
    print('Part 1:', soln)


if __name__ == '__main__':
    sys.exit(main())