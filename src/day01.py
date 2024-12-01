import collections
import os
import sys


def parse_input(inputpath):
    left = []
    right = []
    with open(inputpath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:
                a, b = (int(t) for t in line.split())
                left.append(a)
                right.append(b)
    return left, right


def solve1(left0, right0):
    left = list(left0)
    right = list(right0)
    left.sort()
    right.sort()
    soln = sum(abs(a-b) for a, b in zip(left, right))
    return soln


def test_solve1():
    left, right = parse_input(os.path.join('data', 'test01a.txt'))
    assert solve1(left, right) == 11


def solve2(left, right):
    right_freqs = collections.Counter(right)
    return sum(a * right_freqs[a] for a in left)


def test_solve2():
    left, right = parse_input(os.path.join('data', 'test01a.txt'))
    assert solve2(left, right) == 31


def main():
    "Main program"
    import pyperclip
    left, right = parse_input(os.path.join('data', 'input01.txt'))
    soln = solve1(left, right)
    print('Part 1:', soln)
    assert soln == 765748

    soln = solve2(left, right)
    print('Part 2:', soln)
    assert soln == 27732508

    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())