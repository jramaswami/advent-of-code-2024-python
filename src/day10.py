import collections
import os
import sys

import pyperclip


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        grid = tuple(tuple(int(x) for x in line.strip()) for line in infile if line.strip())
    return grid


def inbounds(grid, r, c):
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[r])


def neighbors(grid, r, c):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        r0, c0 = r + dr, c + dc
        if inbounds(grid, r0, c0):
            yield r0, c0


def find_peaks(grid, trailhead):
    """Return the peaks that can be reached from the given trailhead

    trailhead: tuple of ints representing the row and column index of trailhead
    """
    # BFS
    soln = []
    queue = collections.deque()
    queue.append(trailhead)
    visited = [[False for _ in row] for row in grid]
    visited[trailhead[0]][trailhead[1]] = True
    while queue:
        r, c = queue.popleft()
        x = grid[r][c]
        if x == 9:
            soln.append((r, c))
        for r0, c0 in neighbors(grid, r, c):
            y = grid[r0][c0]
            if x + 1 == y and not visited[r0][c0]:
                queue.append((r0, c0))
                visited[r0][c0] = True
    return soln


def solve1(grid):
    soln = 0
    trailheads = []
    # Find the start points.
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                trailheads.append((r, c))
    for trailhead in trailheads:
        peaks = find_peaks(grid, trailhead)
        soln += len(peaks)
    return soln


def test_solve1():
    grid = parse_input(os.path.join('data', 'test10a.txt'))
    assert solve1(grid) == 36


def find_trails(grid, trailhead):
    """Return the number of paths that reach a peak from the given trailhead

    trailhead: tuple of ints representing the row and column index of trailhead
    """
    # BFS
    soln = 0
    queue = collections.deque()
    queue.append(trailhead)
    while queue:
        r, c = queue.popleft()
        x = grid[r][c]
        if x == 9:
            soln += 1
        for r0, c0 in neighbors(grid, r, c):
            y = grid[r0][c0]
            if x + 1 == y:
                queue.append((r0, c0))
    return soln


def solve2(grid):
    trailheads = []
    # Find the start points.
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                trailheads.append((r, c))
    return sum(find_trails(grid, t) for t in trailheads)


def test_solve2():
    grid = parse_input(os.path.join('data', 'test10a.txt'))
    assert solve2(grid) == 81


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input10.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 717
    soln = solve2(grid)
    print('Part 2:', soln)
    assert soln == 1686
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())