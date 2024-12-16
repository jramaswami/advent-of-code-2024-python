import collections
import dataclasses
import heapq
import math
import os
import sys

import pyperclip


@dataclasses.dataclass(frozen = True)
class Vector:
    row: int
    col: int

    def opposite(self):
        return Vector(self.row * -1, self.col * -1)

    def __add__(self, other):
        return Vector(self.row + other.row, self.col + other.col)

    def __mul__(self, scalar):
        return Vector(self.row * scalar, self.col * scalar)

    def __lt__(self, other):
        if self.row == other.row:
            return self.col < other.col
        return self.row < other.row


DIRECTIONS = (
    Vector(0, 1),
    Vector(0, -1),
    Vector(-1, 0),
    Vector(1, 0)
)


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        grid = tuple(tuple(line.strip()) for line in infile if line.strip())
    return grid


def inbounds(grid, posn):
    return posn.row >= 0 and posn.row < len(grid) and posn.col >= 0 and posn.col < len(grid[posn.row])


def grid_get(grid, posn):
    return grid[posn.row][posn.col]


def neighbors(grid, posn, dirn):
    """Return tuple of neighbor posn, dirn, and cost
    """
    for offset in DIRECTIONS:
        # Do go backwards
        if offset == (dirn * -1):
            continue
        # Forward is same direction
        if offset == dirn:
            if grid_get(grid, posn + offset) != '#':
                yield posn + offset, offset, 1
        # Turns
        if grid_get(grid, posn + offset) != '#':
            # 1001 = 1000 (turn) + 1 (move)
            yield posn + offset, offset, 1001


def reconstruct_path(parents, source, sink, dirn):
    path = []
    curr = sink
    while curr != source:
        path.append((curr, dirn))
        curr, dirn = parents[(curr, dirn)]
    return tuple(reversed(path))


def dijkstra(grid):
    # Find start and end
    source = None
    sink = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if grid[r][c] == 'S':
                source = Vector(r, c)
            if grid[r][c] == 'E':
                sink = Vector(r, c)
    assert source
    assert sink

    parents = dict()
    distance = collections.defaultdict(lambda: math.inf)
    queue = []
    heapq.heappush(queue, (0, source, Vector(0, 1)))
    distance[(source, Vector(0,1))] = 0
    while queue:
        dist, posn, dirn = heapq.heappop(queue)
        if posn == sink:
            return dist, reconstruct_path(parents, source, sink, dirn)
        if distance[(posn, dirn)] == dist:
            for posn0, dirn0, cost in neighbors(grid, posn, dirn):
                dist0 = dist + cost
                if dist0 < distance[(posn0, dirn0)]:
                    distance[(posn0, dirn0)] = dist0
                    heapq.heappush(queue, (dist0, posn0, dirn0))
                    parents[(posn0, dirn0)] = (posn, dirn)


def display(grid, path):
    grid0 = [list(row) for row in grid]
    DS = {
        Vector(0, 1): '>',
        Vector(0, -1): '<',
        Vector(-1, 0): '^',
        Vector(1, 0): 'v'
    }
    for p, d in path:
        if grid_get(grid, p) == '.':
            grid0[p.row][p.col] = DS[d]
    return '\n'.join(''.join(row) for row in grid0)


def solve1(grid):
    dist, path = dijkstra(grid)
    # print(display(grid, path))
    return dist


def test_solve1():
    grid = parse_input(os.path.join('data', 'test16a.txt'))
    assert solve1(grid) == 7036
    grid = parse_input(os.path.join('data', 'test16b.txt'))
    assert solve1(grid) == 11048


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input16.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 65436
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())