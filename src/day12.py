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


def solve1(grid):
    soln = 0
    visited = [[False for _ in row] for row in grid]
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if not visited[r][c]:
                # BFS
                queue = collections.deque()
                queue.append((r, c))
                visited[r][c] = True
                field_label = grid[r][c]
                perimeter = 0
                area = 0
                while queue:
                    r, c = queue.popleft()
                    area += 1
                    for r0, c0 in neighbors(grid, r, c):
                        if not inbounds(grid, r0, c0):
                            perimeter += 1
                            print('perimeter', r, c, '->', r0, c0)
                        elif grid[r0][c0] != field_label:
                            perimeter += 1
                            print('perimeter', r, c, '->', r0, c0)
                        elif not visited[r0][c0]:
                            queue.append((r0, c0))
                            visited[r0][c0] = True
                print(field_label, area, perimeter)
                soln += (area * perimeter)
    return soln


def test_solve1():
    # grid = parse_input(os.path.join('data', 'test12a.txt'))
    # assert solve1(grid) == 772

    # grid = parse_input(os.path.join('data', 'test12b.txt'))
    # assert solve1(grid) == 1930

    # grid = parse_input(os.path.join('data', 'test12c.txt'))
    # assert solve1(grid) == 314

    grid = parse_input(os.path.join('data', 'test12d.txt'))
    assert solve1(grid) == 300



def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input12.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    # 1466700 is too low
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())