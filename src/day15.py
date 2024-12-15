import os
import sys

import pyperclip



def parse_input(filepath):
    grid = []
    with open(filepath, 'r') as infile:
        lines = [line.strip() for line in infile if line.strip()]

    for line in lines[:-1]:
        grid.append(tuple(line))
    instructions = tuple(lines[-1])
    return tuple(grid), instructions


def move_robot(grid, robot, instruction):
    match instruction:
        case '>':
            print('right')
            # Find the space greater than the robot in the current row
            r, c = robot
            c0 = c+1
            while c0 < M:
                if grid[r][c0] == '.':
                    break
                c0 += 1
            if c0 < M and grid[r][c0] == '.':
                print('space', r, c0)
                # Swap everything going backwards.
                for c1 in range(c0, c, -1):
                    grid[r][c1], grid[r][c1-1] = grid[r][c1-1], grid[r][c1]
        case '<':
            print('left')
            # Find the space less than the robot in the current row
            r, c = robot
            c0 = c-1
            while c0 >= 0:
                if grid[r][c0] == '.':
                    break
                c0 -= 1
            if c0 >= 0 and grid[r][c0] == '.':
                # Swap everything going backwards.
                for c1 in range(c0, c):
                    grid[r][c1], grid[r][c1+1] = grid[r][c1+1], grid[r][c1]
        case '^':
            print('up')
            # Find the space less than robot in the current column
            r, c = robot
            r0 = r-1
            while r0 >= 0:
                if grid[r0][c] == '.':
                    break
                r0 -= 1
            if r0 >= 0 and grid[r0][c] == '.':
                # Swap everything going backwards.
                for r1 in range(r0, r):
                    grid[r1][c], grid[r1+1][c] = grid[r1+1][c], grid[r1][c]
        case 'v':
            print('down')
            # Find the space less than robot in the current column
            r, c = robot
            r0 = r+1
            while r0 < N:
                if grid[r0][c] == '.':
                    break
                r0 += 1
            if r0 < N and grid[r0][c] == '.':
                # Swap everything going backwards.
                for r1 in range(r0, r, -1):
                    grid[r1][c], grid[r1-1][c] = grid[r1-1][c], grid[r1][c]
        case other_instruction:
            raise ValueError(f'Unrecognized instruction: {other_instruction}')


def solve1(grid0, instructions):
    # Create mutable grid
    grid = [list(row) for row in grid0]
    N = len(grid)
    M = len(grid[0])
    # Find the starting position robot
    robot = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '@':
                robot = (r, c)

    for instruction in instructions:
        robot = move_robot(grid, robot, instruction)
        for row in grid:
            print(''.join(row))


def main():
    "Main program"
    grid, instructions = parse_input(os.path.join('data', 'test15a.txt'))
    soln = solve1(grid, instructions)

if __name__ == '__main__':
    sys.exit(main())