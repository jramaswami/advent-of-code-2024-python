import collections
import dataclasses
import math
import os
import sys

import pyperclip


@dataclasses.dataclass(frozen=True)
class Antenna:
    label: str
    x: int
    y: int

    def slope(self, other):
        dy = self.y - other.y
        dx = self.x - other.x

        g = math.gcd(abs(dy), abs(dx))

        dy //= g
        dx //= g

        return dy, dx

    def move(self, dy, dx):
        return Antenna(self.label, self.x + dx, self.y + dy)


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        grid = [line.strip() for line in infile if line.strip()]
    return grid


def compute_antinodes(antenna1, antenna2):
    dx = antenna1.x - antenna2.x
    dy = antenna1.y - antenna2.y


def compute_antinodes(antenna1, antenna2):
    dx = antenna1.x - antenna2.x
    dy = antenna1.y - antenna2.y
    antinode1 = Antenna('-'+antenna1.label, antenna1.x + dx, antenna1.y + dy)
    antinode2 = Antenna('-'+antenna2.label, antenna2.x - dx, antenna2.y - dy)
    return antinode1, antinode2


def test_compute_antinode():
    antenna1 = Antenna('A', 6, 6)
    antenna2 = Antenna('A', 8, 3)
    expected = set([Antenna('-A', 4, 9), Antenna('-A', 10, 0)])
    assert set(compute_antinodes(antenna1, antenna2)) == expected

    antenna1 = Antenna('A', 8, 10)
    antenna2 = Antenna('A', 5, 7)
    expected = set([Antenna('-A', 2, 4), Antenna('-A', 11, 13)])
    assert set(compute_antinodes(antenna1, antenna2)) == expected


def inbounds(grid, antenna):
    return (
        antenna.y >= 0 and antenna.y < len(grid) and
        antenna.x >= 0 and antenna.x < len(grid[antenna.y])
    )


def solve1(grid):
    antennas = []
    Y = len(grid)
    X = len(grid[0])
    for r, row in enumerate(grid):
        y = Y - 1 - r
        for x, value in enumerate(row):
            if value != '.':
                antennas.append(Antenna(value, x, y))

    antinode_locations = set()
    for i, antenna1 in enumerate(antennas):
        for antenna2 in antennas[i+1:]:
            if antenna1.label == antenna2.label:
                antinode1, antinode2 = compute_antinodes(antenna1, antenna2)
                if inbounds(grid, antinode1):
                    antinode_locations.add((antinode1.x, antinode1.y))
                if inbounds(grid, antinode2):
                    antinode_locations.add((antinode2.x, antinode2.y))
    return len(antinode_locations)


def test_solve1():
    grid = parse_input(os.path.join('data', 'test08a.txt'))
    assert solve1(grid) == 14


def solve2(grid):
    antennas = []
    Y = len(grid)
    X = len(grid[0])
    for r, row in enumerate(grid):
        y = Y - 1 - r
        for x, value in enumerate(row):
            if value != '.':
                antennas.append(Antenna(value, x, y))

    antinode_locations = set(((a.x, a.y) for a in antennas))
    for i, antenna1 in enumerate(antennas):
        for antenna2 in antennas[i+1:]:
            if antenna1.label == antenna2.label:
                dy, dx = antenna1.slope(antenna2)
                antinode = antenna1.move(dy, dx)
                while inbounds(grid, antinode):
                    antinode_locations.add((antinode.x, antinode.y))
                    antinode = antinode.move(dy, dx)
                antinode = antenna1.move(-dy, -dx)
                while inbounds(grid, antinode):
                    antinode_locations.add((antinode.x, antinode.y))
                    antinode = antinode.move(-dy, -dx)

    return len(antinode_locations)


def test_solve2():
    grid = parse_input(os.path.join('data', 'test08b.txt'))
    assert solve2(grid) == 9

    grid = parse_input(os.path.join('data', 'test08a.txt'))
    assert solve2(grid) == 34


def main():
    "Main program"
    grid = parse_input(os.path.join('data', 'input08.txt'))
    soln = solve1(grid)
    print('Part 1:', soln)
    assert soln == 409

    soln = solve2(grid)
    print('Part 2:', soln)
    assert soln == 1308

    pyperclip.copy(soln)


if __name__ == '__main__':
    main()