import os
import sys

import pyperclip


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        data = tuple(infile.readline().strip().split())
    return data


def tick(stones):
    """Transform stones according to the rules
    """
    new_stones = []
    for stone in stones:
        if stone == '0':
            new_stones.append('1')
        elif len(stone) % 2 == 0:
            m = len(stone) // 2
            new_stones.append(str(int(stone[:m])))
            new_stones.append(str(int(stone[m:])))
        else:
            new_stones.append(str(int(stone) * 2024))
    return tuple(new_stones)


def test_tick():
    stones = tuple('0 1 10 99 999'.split())
    expected = tuple('1 2024 1 0 9 9 2021976'.split())
    assert tick(stones) == expected

    stones = tuple('125 17'.split())
    expected = (
        '253000 1 7',
        '253 0 2024 14168',
        '512072 1 20 24 28676032',
        '512 72 2024 2 0 2 4 2867 6032',
        '1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32',
        '2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2'
    )
    for ex in expected:
        stones = tick(stones)
        assert stones == tuple(ex.split())


def solve1(stones, ticks=25):
    for _ in range(ticks):
        stones = tick(stones)
    return len(stones)


def test_solve1():
    stones = tuple('125 17'.split())
    assert solve1(stones, 6) == 22
    assert solve1(stones) == 55312


def main():
    "Main program"
    stones = parse_input(os.path.join('data', 'input11.txt'))
    soln = solve1(stones)
    print('Part 1:', soln)
    assert soln == 189167

    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())