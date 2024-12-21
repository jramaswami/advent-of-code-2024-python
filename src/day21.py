import collections
import dataclasses
import math
import os
import sys



@dataclasses.dataclass(frozen = True)
class Vector:
    row :int
    col :int

    def __add__(self, other):
        return Vector(self.row + other.row, self.col + other.col)


NUMBER_PAD = tuple(tuple(row) for row in '789\n456\n123\n 0A'.split('\n'))
DIRECTION_PAD = tuple(tuple(row) for row in ' ^A\n<v>'.split('\n'))
OFFSETS = {
    '^': Vector(-1, 0),
    'v': Vector(1, 0),
    '<': Vector(0, -1),
    '>': Vector(0, 1)
}


def inbounds(grid, p):
    return p.row >= 0 and p.row < len(grid) and p.col >= 0 and p.col < len(grid[p.row])


def neighbors(grid, p):
    for _, o in OFFSETS.items():
        p0 = p + o
        if inbounds(grid, p0) and grid[p0.row][p0.col] != ' ':
            yield p0


def all_paths(grid):

    def bfs(origin):
        dist = collections.defaultdict(lambda: math.inf)
        queue = collections.deque()
        dist[origin] = 0
        queue.append(origin)
        while queue:
            p = queue.popleft()
            for p0 in neighbors(grid, p):
                if dist[p] + 1 < dist[p0]:
                    dist[p0] = dist[p] + 1
                    queue.append(p0)
        return dist

    paths = dict()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != ' ':
                origin = Vector(r, c)
                x = grid[origin.row][origin.col]
                dist = bfs(origin)
                paths[x] = dict()
                for p, d in dist.items():
                    y = grid[p.row][p.col]
                    paths[x][y] = d
    return paths

def main():
    "Main program"
    numeric_paths = all_paths(NUMBER_PAD)
    for k in numeric_paths:
        print(k, '->', numeric_paths[k])


if __name__ == '__main__':
    sys.exit(main())