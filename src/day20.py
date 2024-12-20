import collections
import dataclasses
import os
import sys

import pyperclip


sys.setrecursionlimit(pow(10, 6))


@dataclasses.dataclass(frozen=True)
class Vector:
    row: int
    col: int

    def __add__(self, other):
        return Vector(self.row + other.row, self.col + other.col)



def parse_input(filepath):
    grid = []
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            grid.append(tuple(line))
    return tuple(grid)



def inbounds(grid, posn):
    return (
        posn.row >= 0 and posn.row < len(grid) and
        posn.col >= 0 and posn.col < len(grid[posn.row])
    )


def neighbors(grid, posn):
    for offset in (Vector(0, 1), Vector(0, -1), Vector(1, 0), Vector(-1, 0)):
        posn0 = posn + offset
        if inbounds(grid, posn0):
            yield posn0


def is_wall(grid, posn):
    return grid[posn.row][posn.col] == '#'


def find_source_and_sink(grid):
    source = None
    sink = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 'S':
                source = Vector(r, c)
            elif val == 'E':
                sink = Vector(r, c)
    assert source
    assert sink
    return source, sink


def solve1(grid):
    source, sink = find_source_and_sink(grid)

    visited = set()
    path_lengths = []
    def dfs(posn, cheat, distance):
        if posn == sink:
            path_lengths.append((distance, cheat))
        else:
            visited.add(posn)
            for posn0 in neighbors(grid, posn):
                if posn0 in visited:
                    continue
                if is_wall(grid, posn0) and not cheat:
                    dfs(posn0, True, distance+1)
                else:
                    dfs(posn0, cheat, distance+1)
            visited.remove(posn)

    dfs(source, False, 0)
    print(path_lengths)


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'test20a.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())