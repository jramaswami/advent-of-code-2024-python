import os
import sys

import pyperclip


def grid_heights(grid):
    """Return the number of '#' in each column of grid"""
    heights = [0 for _ in grid[0]]
    for row in grid:
        for c, x in enumerate(row):
            if x == '#':
                heights[c] += 1
    return tuple(heights)


def parse_input(filepath):
    # Read grids from input file
    grids = []
    with open(filepath, 'r') as infile:
        grid = []
        for line in infile:
            line = line.strip()
            if line:
                grid.append(line)
            else:
                grids.append(grid)
                grid = []
        if grid:
            grids.append(grid)

    # Get the height of the first grid
    grid_height = len(grids[0])
    # Assert all heights are the same
    assert all(len(g) == grid_height for g in grids)

    # Sort grids into keys and locks
    key_grids = []
    lock_grids = []
    for grid in grids:
        if all(x == '#' for x in grid[0]):
            # Top row is all '#', this is a lock
            lock_grids.append(grid)
        else:
            assert all(x == '#' for x in grid[-1])
            # Bottom row is all '#', this is a key
            key_grids.append(grid)

    # Convert grids to heights
    keys = tuple(grid_heights(g) for g in key_grids)
    locks = tuple(grid_heights(g) for g in lock_grids)
    return grid_height, keys, locks,
    

def overlaps(key, lock, height):
    for k, l in zip(key, lock):
        if k + l > height:
            return True
    return False


def solve1(keys, locks, height):
    soln = 0
    for k in keys:
        for l in locks:
            if not overlaps(k, l, height):
                soln += 1
    return soln


def test_solve1():
    height, keys, locks = parse_input(os.path.join('data', 'test25a.txt'))
    assert solve1(keys, locks, height) == 3


def main():
    """Main program"""
    height, keys, locks = parse_input(os.path.join('data', 'input25.txt'))
    soln = solve1(keys, locks, height)
    print('Part 1:', soln)
    assert soln == 3397
    pyperclip.copy(soln)


if __name__ == '__main__':
    main()
