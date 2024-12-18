import collections
import dataclasses
import heapq
import math
import os
import sys
from typing import Set, List

import pyperclip


@dataclasses.dataclass(frozen=True)
class Vector:
    r: int
    c: int

    def __add__(self, other):
        return Vector(self.r + other.r, self.c + other.c)

    def __sub__(self, other):
        return Vector(self.r - other.r, self.c - other.c)

    def __lt__(self, other):
        return self.r < other.r


@dataclasses.dataclass(frozen=True)
class Grid:
    rows: int
    columns: int
    blocks: Set[Vector]

    def inbounds(self, posn: Vector) -> bool:
        return (
            posn.r >= 0 and posn.r <= self.rows and
            posn.c >= 0 and posn.c <= self.columns
        )

    def corrupted(self, posn: Vector) -> bool:
        return posn in self.blocks

    def neighbors(self, posn: Vector) -> List[Vector]:
        for dp in (Vector(0, 1), Vector(0, -1), Vector(1, 0), Vector(-1, 0)):
            posn0 = posn + dp
            if self.inbounds(posn0) and not self.corrupted(posn0):
                yield posn0


def parse_input(filepath):
    blocks = []
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:
                r, c = (int(n) for n in line.split(','))
                blocks.append(Vector(r, c))
    return blocks


def solve1(blocks, grid_rows, grid_columns, blocks_to_use):
    blocks0 = set(blocks[:blocks_to_use])
    grid = Grid(grid_rows, grid_columns, blocks0)
    origin = Vector(0, 0)
    queue = []
    heapq.heappush(queue, (0, origin))
    distance = collections.defaultdict(lambda: math.inf)
    distance[origin] = 0
    while queue:
        d, p = heapq.heappop(queue)
        if distance[p] == d:
            for p0 in grid.neighbors(p):
                if d + 1 < distance[p0]:
                    distance[p0] = d + 1
                    heapq.heappush(queue, (d + 1, p0))
    return distance[Vector(grid_rows, grid_columns)]


def test_solve1():
    blocks = parse_input(os.path.join('data', 'test18a.txt'))
    assert solve1(blocks, 6, 6, 12) == 22


def solve2(blocks, grid_rows, grid_columns):
    # Binary search the answer
    lo = 0
    hi = len(blocks)
    soln = len(blocks)
    while lo <= hi:
        blocks_to_use = lo + ((hi - lo) // 2)
        shortest_path = solve1(blocks, grid_rows, grid_columns, blocks_to_use)
        if shortest_path == math.inf:
            soln = min(soln, blocks_to_use)
            hi = blocks_to_use - 1
        else:
            lo = blocks_to_use + 1
    return blocks[soln-1]


def test_solve2():
    blocks = parse_input(os.path.join('data', 'test18a.txt'))
    assert solve2(blocks, 6, 6) == Vector(6,1)


def main():
    "Main program"
    blocks = parse_input(os.path.join('data', 'input18.txt'))
    soln = solve1(blocks, 70, 70, 1024)
    print('Part 1:', soln)
    assert soln == 356
    soln = solve2(blocks, 70, 70)
    print('Part 2:', soln)
    assert soln == Vector(r=22, c=33)
    pyperclip.copy(f'{soln.r},{soln.c}')


if __name__ == '__main__':
    sys.exit(main())