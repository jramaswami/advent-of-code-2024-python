import collections
import operator
import os
import sys

import pyperclip


Calibration = collections.namedtuple('Calibration', ['test_value', 'numbers'])


def parse_input(filepath):
    calibrations = []
    with open(filepath, 'r') as infile:
        for line in infile:
            test_value, numbers = line.strip().split(': ')
            test_value = int(test_value)
            numbers = tuple(int(n) for n in numbers.split())
            calibrations.append(Calibration(test_value, numbers))
    return tuple(calibrations)


def is_true(calibration, operations):
    # (curr value, curr index)
    queue = collections.deque()
    queue.append((calibration.numbers[0], 1))
    while queue:
        curr_value, curr_index = queue.popleft()
        if curr_index == len(calibration.numbers):
            if curr_value == calibration.test_value:
                return True
        else:
            for operator in operations:
                queue.append((operator(curr_value, calibration.numbers[curr_index]), curr_index + 1))
    return False


def solve1(calibrations):
    operations = (operator.mul, operator.add)
    return sum(c.test_value for c in calibrations if is_true(c, operations))


def test_solve1():
    calibrations = parse_input(os.path.join('data', 'test07a.txt'))
    assert solve1(calibrations) == 3749


def concatenate(a, b):
    return int(str(a)+str(b))


def solve2(calibrations):
    operations = (operator.mul, operator.add, concatenate)
    return sum(c.test_value for c in calibrations if is_true(c, operations))


def test_solve2():
    calibrations = parse_input(os.path.join('data', 'test07a.txt'))
    assert solve2(calibrations) == 11387


def main():
    "Main program"
    calibrations = parse_input(os.path.join('data', 'input07.txt'))
    soln = solve1(calibrations)
    print('Part 1:', soln)
    assert soln == 303876485655
    soln = solve2(calibrations)
    print('Part 2:', soln)
    assert soln == 146111650210682

    pyperclip.copy(soln)


if __name__ == '__main__':
    main()