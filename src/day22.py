import os
import sys

import pyperclip


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        data = tuple(int(line.strip()) for line in infile if line.strip())
    return data


def evolve(n):
    MOD = 16777216
    x = n * 64
    n = n ^ x
    n %= MOD
    x = n // 32
    n = n ^ x
    n %= MOD
    x = n * 2048
    n = n ^ x
    n %= MOD
    return n


def transform(n, repeat=2000):
    for _ in range(repeat):
        n = evolve(n)
    return n


def test_transform():
    n = 123
    expecteds = [
        15887950, 16495136, 527345, 704524, 1553684,
        12683156, 11100544, 12249484, 7753432, 5908254
    ]
    for ex in expecteds:
        n = evolve(n)
        assert n == ex


def solve1(numbers):
    return sum(transform(n) for n in numbers)


def test_solve1():
    numbers = [1, 10, 100, 2024]
    assert solve1(numbers) == 37327623


def main():
    "Main program"
    numbers = parse_input(os.path.join('data', 'input22.txt'))
    soln = solve1(numbers)
    print('Part 1:', soln)
    assert soln == 16999668565
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())