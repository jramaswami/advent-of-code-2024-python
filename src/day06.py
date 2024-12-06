import dataclasses
import os
import sys

import pyperclip
import tqdm


@dataclasses.dataclass(frozen=True)
class Vector:
    r: int
    c: int

    def __add__(self, other):
        return Vector(self.r + other.r, self.c + other.c)


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        grid = [list(line.strip()) for line in infile if line.strip()]
    return grid


def inbounds(grid, posn):
    return posn.r >= 0 and posn.r < len(grid) and posn.c >= 0 and posn.c < len(grid[posn.r])


def solve1(grid):
    # Find guard position.
    guard = None
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            if x == '^':
                guard = Vector(r, c)
    assert guard

    offsets = (Vector(-1, 0), Vector(0, 1), Vector(1, 0), Vector(0, -1))
    dirn = 0

    visited = [[0 for _ in row] for row in grid]
    while inbounds(grid, guard):
        visited[guard.r][guard.c] = 1
        guard0 = guard + offsets[dirn]
        while inbounds(grid, guard0) and grid[guard0.r][guard0.c] == '#':
            # turn
            dirn = dirn + 1
            dirn %= len(offsets)
            guard0 = guard + offsets[dirn]
        guard = guard0
    return sum(sum(row) for row in visited)


def test_solve1():
    grid = parse_input(os.path.join('data', 'test06a.txt'))
    assert solve1(grid) == 41


def show_grid(grid, visited):
    grid0 = [list(row) for row in grid]
    dirn_symbols = '^>v<'
    for posn, dirn in visited:
        grid0[posn.r][posn.c] = dirn_symbols[dirn]
    for row in grid0:
        print(''.join(row))
    print('*'*80)


class CycleDetected(Exception):
    pass


def simulate(grid, guard):
    offsets = (Vector(-1, 0), Vector(0, 1), Vector(1, 0), Vector(0, -1))
    dirn = 0
    visited = set()
    while inbounds(grid, guard):
        if (guard, dirn) in visited:
            raise CycleDetected(f'Cycle detected at {guard} {dirn}')
        visited.add((guard, dirn))
        guard0 = guard + offsets[dirn]
        while inbounds(grid, guard0) and grid[guard0.r][guard0.c] == '#':
            # turn
            dirn = dirn + 1
            dirn %= len(offsets)
            guard0 = guard + offsets[dirn]
        guard = guard0
    return visited


def solve2(grid):
    # Find guard position.
    guard = None
    for r, row in enumerate(grid):
        for c, x in enumerate(row):
            if x == '^':
                guard = Vector(r, c)
    assert guard

    soln = 0
    visited = simulate(grid, guard)
    posns_visited = set(p for p, _ in visited)
    for posn in tqdm.tqdm(posns_visited):
        prev_value = grid[posn.r][posn.c]
        grid[posn.r][posn.c] = '#'
        try:
            simulate(grid, guard)
        except CycleDetected as ex:
            soln += 1
        grid[posn.r][posn.c] = prev_value
    return soln


def test_solve2():
    grid = parse_input(os.path.join('data', 'test06a.txt'))
    assert solve2(grid) == 6


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input06.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 4711

    grid = parse_input(os.path.join('data', 'input06.txt'))
    # grid = parse_input(os.path.join('data', 'test06a.txt'))
    soln = solve2(grid)
    print('Part 2:', soln)
    assert soln == 1562

    pyperclip.copy(soln)


if __name__ == '__main__':
    main()