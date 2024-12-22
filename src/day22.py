import collections
import itertools
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


class Record:
    def __init__(self, secret):
        self.secret = secret
        self.price = secret % 10
        self.change = None
        self.window = None

    def __str__(self):
        return f"{self.secret} {self.price} {self.change} {self.window}"


class Monkey:
    def __init__(self, secret):
        self.records = []
        self.records.append(Record(secret))
        for _ in range(2000):
            secret = evolve(secret)
            self.records.append(Record(secret))

        for i, _ in enumerate(self.records[1:], start=1):
            self.records[i].change = self.records[i].price - self.records[i-1].price

        for i, _ in enumerate(self.records[4:], start=4):
            self.records[i].window = tuple(x.change for x in self.records[i-3:i+1])

        # Cache
        self.cache = dict()
        for record in self.records:
            if record.window not in self.cache:
                self.cache[record.window] = record.price

    def bananas_for(self, target_window):
        return self.cache.get(target_window, 0)


def solve2(numbers):
    monkeys = [Monkey(n) for n in numbers]
    possible = set()
    for monkey in monkeys:
        for record in monkey.records:
            if record.window:
                possible.add(record.window)
    soln = 0
    for target in possible:
        soln = max(soln, sum(monkey.bananas_for(target) for monkey in monkeys))
    return soln


def main():
    "Main program"
    numbers = parse_input(os.path.join('data', 'input22.txt'))
    soln = solve1(numbers)
    print('Part 1:', soln)
    assert soln == 16999668565
    soln = solve2(numbers)
    print('Part 2:', soln)
    assert soln == 1898
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())