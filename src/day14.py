import collections
import dataclasses
import math
import os
import sys

import pyperclip


@dataclasses.dataclass(frozen = True)
class Vector:
    x: int
    y: int

    @staticmethod
    def from_input_string(input_string):
        assert input_string[0] in 'pv'
        assert input_string[1] == '='
        x, y = (int(n) for n in input_string[2:].split(','))
        return Vector(x, y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)

    def __mul__(self, scalar: int):
        return Vector(self.x * scalar, self.y * scalar)


@dataclasses.dataclass(frozen = True)
class Robot:
    position: Vector
    velocity: Vector

    def move(self, grid_limits: Vector, scalar = 1):
        return Robot(
            (self.position + (self.velocity * scalar)) % grid_limits,
            self.velocity
        )


def parse_input(filepath):
    robots = []
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            position_string, velocity_string = line.split(' ')
            robot = Robot(
                Vector.from_input_string(position_string),
                Vector.from_input_string(velocity_string)
            )
            robots.append(robot)
    return robots


def get_quadrant(robot, grid_limits: Vector) -> int:
    y_mid = grid_limits.y // 2
    x_mid = grid_limits.x // 2
    quadrant = ''
    if robot.position.y == y_mid:
        return 'None'
    elif robot.position.y > y_mid:
        quadrant += 'T'
    else:
        quadrant += 'B'
    if robot.position.x == x_mid:
        return 'None'
    elif robot.position.x > x_mid:
        quadrant += 'R'
    else:
        quadrant += 'L'
    return quadrant


def solve1(robots, grid_limits: Vector) -> int:
    robots0 = [robot.move(grid_limits, 100) for robot in robots]
    quadrants = collections.defaultdict(int)
    for robot in robots0:
        quadrants[get_quadrant(robot, grid_limits)] += 1
    return math.prod(x for q, x in quadrants.items() if q != 'None')


def test_solve1():
    robots = parse_input(os.path.join('data', 'test14a.txt'))
    assert solve1(robots, Vector(11, 7)) == 12


def print_grid(robots, grid_limits):
    grid = [[' ' for _ in range(grid_limits.x)] for _ in range(grid_limits.y)]
    for robot in robots:
        grid[robot.position.y][robot.position.x] = '#'
    print('\n'.join(''.join(row) for row in grid))


def solve2(robots, grid_limits: Vector):
    # All robots move through a cycle of length 10403
    # There are 500 robots
    # Most(?) of the robots are involved in the christmas tree
    most = len(robots) // 2
    soln = 10404
    for tick in range(10403):
        quadrants = collections.defaultdict(int)
        for robot in robots:
            quadrants[get_quadrant(robot, grid_limits)] += 1
        if any(x > most for q, x in quadrants.items() if q != 'None'):
            # print('*'*140)
            # print(tick)
            # print('*'*140)
            # print_grid(robots, grid_limits)
            return tick
        robots = [r.move(grid_limits,1) for r in robots]


def main():
    "Main program"
    robots = parse_input(os.path.join('data', 'input14.txt'))
    soln = solve1(robots, Vector(101, 103))
    print('Part 1:', soln)
    assert soln == 224969976
    soln = solve2(robots, Vector(101, 103))
    print('Part 2:', soln)
    assert soln == 7892
    pyperclip.copy(soln)



if __name__ == '__main__':
    main()