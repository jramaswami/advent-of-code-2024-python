import collections
import os
import sys

import pyperclip


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        grid = tuple(tuple(line.strip()) for line in infile if line.strip())
    return grid


def inbounds(grid, r, c):
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[r])


def neighbors(grid, r, c):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        r0, c0 = r + dr, c + dc
        yield r0, c0


def compute_perimeter(grid, field):
    perimeter = 0
    for r, c in field:
        for r0, c0 in neighbors(grid, r, c):
            if not inbounds(grid, r0, c0):
                perimeter += 1
            elif grid[r0][c0] != grid[r][c]:
                perimeter += 1
    return perimeter


def find_field(grid, visited, origin_r, origin_c):
    # BFS
    queue = collections.deque()
    queue.append((origin_r, origin_c))
    visited[origin_r][origin_c] = True
    field_label = grid[origin_r][origin_c]
    field = set()
    while queue:
        r, c = queue.popleft()
        field.add((r, c))
        for r0, c0 in neighbors(grid, r, c):
            if inbounds(grid, r0, c0) and not visited[r0][c0] and grid[r0][c0] == field_label:
                queue.append((r0, c0))
                visited[r0][c0] = True
    return field


def solve1(grid):
    soln = 0
    visited = [[False for _ in row] for row in grid]
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if not visited[r][c]:
                field = find_field(grid, visited, r, c)
                area = len(field)
                perimeter = compute_perimeter(grid, field)
                soln += (area * perimeter)
    return soln


def test_solve1():
    grid = parse_input(os.path.join('data', 'test12a.txt'))
    assert solve1(grid) == 772

    grid = parse_input(os.path.join('data', 'test12b.txt'))
    assert solve1(grid) == 1930

    grid = parse_input(os.path.join('data', 'test12c.txt'))
    assert solve1(grid) == 314


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input12.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 1467094
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())