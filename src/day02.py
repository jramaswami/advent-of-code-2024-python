import math
import os
import sys
import pyperclip


def read_data(filepath):
    data = []
    with open(filepath, 'r') as infile:
        for line in infile:
            data.append([int(t) for t in line.strip().split()])
    return data


def is_safe(report):
    sign = -1.0
    if report[0] > report[1]:
        sign = 1.0
    for a, b in zip(report[:-1], report[1:]):
        # The levels are either all increasing or all decreasing.
        if math.copysign(1, a-b) != sign:
            return False
        if not (1 <= abs(a-b) <= 3):
            return False
    return True


def solve1(data):
    return sum(is_safe(report) for report in data)


def test_solve1():
    data = read_data(os.path.join('data', 'test02a.txt'))
    assert solve1(data) == 2


def module_dampener(report):
    report0 = list(report)
    yield tuple(report0)
    for i in range(len(report)):
        yield tuple(report0[:i] + report[i+1:])


def solve2(data):
    return sum(any(is_safe(r) for r in module_dampener(report)) for report in data)


def test_solve2():
    data = read_data(os.path.join('data', 'test02a.txt'))
    assert solve2(data) == 4


def main():
    "Main program"
    data = read_data(os.path.join('data', 'input02.txt'))
    soln = solve1(data)
    print('Part 1:', soln)
    assert soln == 598
    soln = solve2(data)
    print('Part 2:', soln)
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())