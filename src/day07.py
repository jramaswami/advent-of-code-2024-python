import collections
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


def is_true(calibration):
    # (curr value, curr index)
    queue = collections.deque()
    queue.append((calibration.numbers[0], 1))
    while queue:
        curr_value, curr_index = queue.popleft()
        if curr_index == len(calibration.numbers):
            if curr_value == calibration.test_value:
                return True
        else:
            queue.append((curr_value + calibration.numbers[curr_index], curr_index + 1))
            queue.append((curr_value * calibration.numbers[curr_index], curr_index + 1))
    return False


def solve1(calibrations):
    return sum(c.test_value for c in calibrations if is_true(c))


def test_solve1():
    calibrations = parse_input(os.path.join('data', 'test07a.txt'))
    assert solve1(calibrations) == 3749


def main():
    "Main program"
    calibrations = parse_input(os.path.join('data', 'input07.txt'))
    soln = solve1(calibrations)
    print('Part 1:', soln)
    assert soln == 303876485655

    pyperclip.copy(soln)


if __name__ == '__main__':
    main()