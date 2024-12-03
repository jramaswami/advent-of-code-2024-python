import os
import re
import sys

import pyperclip


def read_input(input_path):
    with open(input_path, 'r') as infile:
        data = infile.read()
    return data


def solve1(data):
    soln = 0
    for match in re.findall('mul\\(\\d+,\\d+\\)', data, re.M):
        a, b = (int(t) for t in match[4:-1].split(','))
        x = a * b
        soln += x
    return soln


def test_solve1():
    data = read_input(os.path.join('data', 'test03a.txt'))
    assert solve1(data) == 161


def solve2(data):
    soln = 0
    ok = True
    for match, do in re.findall('(mul\\(\\d+,\\d+\\))|(don?\'?t?)', data, re.M):
        if do == 'do':
            ok = True
        if do == "don't":
            ok = False
        if match and ok:
            a, b = (int(t) for t in match[4:-1].split(','))
            x = a * b
            soln += x
    return soln


def test_solve2():
    data = read_input(os.path.join('data', 'test03b.txt'))
    assert solve2(data) == 48


def main():
    "Main program"
    data = read_input(os.path.join('data', 'input03.txt'))
    soln = solve1(data)
    print('Part 1:', soln)
    assert soln == 157621318

    data = read_input(os.path.join('data', 'input03.txt'))
    soln = solve2(data)
    print('Part 2:', soln)
    assert soln == 79845780
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())