import collections
import functools
import os
import sys

import pyperclip


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        towel_patterns = tuple(next(infile).strip().split(', '))
        next(infile)  # Skip blank line
        designs = tuple(line.strip() for line in infile)
    return towel_patterns, designs


def can_make_design(towel_patterns, design):

    @functools.cache
    def rec(i):
        if i == len(design):
            return True

        result = False
        for p in towel_patterns:
            t = len(p)
            if design[i:i+t] == p:
                result = result or rec(i+t)
        return result

    return rec(0)


def test_can_make_design():
    towel_patterns, designs = parse_input(os.path.join('data', 'test19a.txt'))
    expected_results = [True, True, True, True, False, True, True, False]
    for design, expected in zip(designs, expected_results):
        result = can_make_design(towel_patterns, design)
        print(design, result)
        assert expected == result


def solve1(towel_patterns, designs):
    soln = 0
    for design in designs:
        if can_make_design(towel_patterns, design):
            soln += 1
    return soln


def test_solve1():
    towel_patterns, designs = parse_input(os.path.join('data', 'test19a.txt'))
    assert solve1(towel_patterns, designs) == 6


def ways_to_make_design(towel_patterns, design):

    @functools.cache
    def rec(i):
        if i == len(design):
            return 1

        result = 0
        for p in towel_patterns:
            t = len(p)
            if design[i:i+t] == p:
                result += rec(i+t)
        return result

    return rec(0)


def test_ways_to_make_design():
    towel_patterns, designs = parse_input(os.path.join('data', 'test19a.txt'))
    expected_results = [2, 1, 4, 6, 0, 1, 2, 0]
    for design, expected in zip(designs, expected_results):
        result = ways_to_make_design(towel_patterns, design)
        print(design, result)
        assert expected == result


def solve2(towel_patterns, designs):
    soln = 0
    for design in designs:
        soln += ways_to_make_design(towel_patterns, design)
    return soln


def test_solve1():
    towel_patterns, designs = parse_input(os.path.join('data', 'test19a.txt'))
    assert solve2(towel_patterns, designs) == 16


def main():
    "Main program"
    towel_patterns, designs = parse_input(os.path.join('data', 'input19.txt'))
    soln = solve1(towel_patterns, designs)
    print('Part 1:', soln)
    assert soln == 363
    soln = solve2(towel_patterns, designs)
    print('Part 2:', soln)
    assert soln == 642535800868438
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())