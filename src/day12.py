import collections
import enum
import itertools
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


def is_boundary(grid, field_label, r, c):
    if not inbounds(grid, r, c):
        return True
    if field_label != grid[r][c]:
        return True
    return False


def find_fence_sections(grid, field):
    """Find the fence sections for each field.  Fence sections
    will have a half-coordinate so they fall between the rows
    and columns.
    """
    horizontal_fence_sections = []
    vertical_fence_sections = []
    for r, c in field:
        top_r, top_c = r - 1, c
        if is_boundary(grid, grid[r][c], top_r, top_c):
            horizontal_fence_sections.append((r - 0.5, c))
        bottom_r, bottom_c = r + 1, c
        if is_boundary(grid, grid[r][c], bottom_r, bottom_c):
            horizontal_fence_sections.append((r + 0.5, c))
        left_r, left_c = r, c - 1
        if is_boundary(grid, grid[r][c], left_r, left_c):
            vertical_fence_sections.append((r, c - 0.5))
        right_r, right_c = r, c + 1
        if is_boundary(grid, grid[r][c], right_r, right_c):
            vertical_fence_sections.append((r, c + 0.5))
    return horizontal_fence_sections, vertical_fence_sections


class UnionFind:
    def __init__(self, n):
        self.n = n
        self.id = list(range(n))
        self.size = [1 for _ in range(n)]

    def find(self, u):
        if self.id[u] != u:
            self.id[u] = self.find(self.id[u])
        return self.id[u]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.id[b] = a
            self.size[a] += self.size[b]
            self.n -= 1


def solve2(grid):
    for row in grid:
        print(''.join(row))

    soln = 0
    visited = [[False for _ in row] for row in grid]
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if not visited[r][c]:
                field = find_field(grid, visited, r, c)
                sides = 0
                horizontal_fence_sections, vertical_fence_sections = find_fence_sections(grid, field)
                uf = UnionFind(len(horizontal_fence_sections))
                for i, (r1, c1) in enumerate(horizontal_fence_sections):
                    for j, (r2, c2) in enumerate(horizontal_fence_sections[i+1:], start=i+1):
                        if r1 == r2 and abs(c1 - c2) == 1:
                            uf.union(i, j)
                sides += uf.n
                print('horiz', uf.n)
                uf = UnionFind(len(vertical_fence_sections))
                for i, (r1, c1) in enumerate(vertical_fence_sections):
                    for j, (r2, c2) in enumerate(vertical_fence_sections[i+1:], start=i+1):
                        if c1 == c2 and abs(r1 - r2) == 1:
                            uf.union(i, j)
                sides += uf.n
                print('vert', uf.n)
                area = len(field)
                print(f'{r=} {c=} {grid[r][c]} {sides=} {area=}')
                soln += (area * sides)
    return soln


def test_solve2():
    grid = parse_input(os.path.join('data', 'test12d.txt'))
    assert solve2(grid) == 80

    grid = parse_input(os.path.join('data', 'test12e.txt'))
    assert solve2(grid) == 236

    grid = parse_input(os.path.join('data', 'test12f.txt'))
    assert solve2(grid) == 368


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input12.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 1467094
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())