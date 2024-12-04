import os
import sys
import pyperclip


OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


def inbounds(grid, r, c):
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[r])


def neighbors(grid, r0, c0, length=4):
    for dr, dc in OFFSETS:
        values = [grid[r0][c0]]
        r, c = r0, c0
        for _ in range(length-1):
            r, c = r + dr, c + dc
            if not inbounds(grid, r, c):
                break
            values.append(grid[r][c])
        yield ''.join(values)


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        grid = [line.strip() for line in infile.readlines()]
    return grid


def solve1(grid):
    soln = 0
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            for word in neighbors(grid, r, c):
                if word == 'XMAS':
                    soln += 1
    return soln


def test_solve1():
    grid = parse_input(os.path.join('data', 'test04a.txt'))
    assert solve1(grid) == 18


def main():
    grid = parse_input(os.path.join('data', 'input04.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 2462

    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())