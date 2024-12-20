import collections
import dataclasses
import math
import os
import sys

import pyperclip


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


def cheat_neighbors(grid, posn):
    cheat_offsets = (
        Vector(1, 1), Vector(-1, 1), Vector(1, -1), Vector(-1, -1),
        Vector(2, 0), Vector(-2, 0), Vector(0, 2), Vector(0, -2)
    )
    for offset in cheat_offsets:
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


def bfs(grid, origin):
    distance = collections.defaultdict(lambda: math.inf)
    queue = collections.deque()
    distance[origin] = 0
    queue.append(origin)
    while queue:
        posn = queue.popleft()
        for posn0 in neighbors(grid, posn):
            if not is_wall(grid, posn0) and distance[posn] + 1 < distance[posn0]:
                distance[posn0] = distance[posn] + 1
                queue.append(posn0)
    return distance


def compute_cheat_distances(grid, distance_from_source, distance_to_sink, shortest_path):
    cheat_distances = []
    # For each cell, see how much is saved if we cheat
    for r, row in enumerate(grid):
        for c, val in enumerate(grid):
            posn = Vector(r, c)
            if not is_wall(grid, posn):
                # Get cheat neighbors
                for posn0 in cheat_neighbors(grid, posn):
                    if not is_wall(grid, posn0):
                        d = distance_from_source[posn] + 2 + distance_to_sink[posn0]
                        if d < shortest_path:
                            cheat_distances.append(d)
    return cheat_distances


def solve1(grid):
    source, sink = find_source_and_sink(grid)
    # BFS to compute the distance between each cell and the sink
    distance_from_source = bfs(grid, source)
    # BFS to compute the distance between each cell and the sink
    distance_to_sink = bfs(grid, sink)
    assert distance_from_source[sink] == distance_to_sink[source]
    shortest_path = distance_to_sink[source]
    # For each cell, compute the distance if you cheated from here
    cheat_distances = compute_cheat_distances(
        grid, distance_from_source, distance_to_sink, shortest_path
    )
    # Count the number of cheats that save 100+
    save_freqs = collections.Counter(shortest_path - d for d in cheat_distances)
    return sum(v for k, v in save_freqs.items() if k >= 100)


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input20.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 1378
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())