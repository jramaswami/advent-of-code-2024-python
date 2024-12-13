import dataclasses
import math
import os
import sys

import pyperclip


@dataclasses.dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


@dataclasses.dataclass(frozen=True)
class ClawMachine:
    button_a: Vector
    button_b: Vector
    prize_location: Vector


def parse_input(filepath):
    claw_machines = []
    with open(filepath, 'r') as infile:
        while 1:
            # Button A
            line = infile.readline().strip()
            if not line:
                break
            x_index = line.index('X')
            comma_index = line.index(',', x_index)
            x_value = int(line[x_index+1:comma_index])
            y_index = line.index('Y', comma_index)
            y_value = int(line[y_index+1:])
            button_a = Vector(x_value, y_value)
            # Button B
            line = infile.readline().strip()
            x_index = line.index('X')
            comma_index = line.index(',', x_index)
            x_value = int(line[x_index+1:comma_index])
            y_index = line.index('Y', comma_index)
            y_value = int(line[y_index+1:])
            button_b = Vector(x_value, y_value)
            # Prize Location
            line = infile.readline().strip()
            x_index = line.index('X')
            comma_index = line.index(',', x_index)
            x_value = int(line[x_index+2:comma_index])
            y_index = line.index('Y', comma_index)
            y_value = int(line[y_index+2:])
            prize_location = Vector(x_value, y_value)
            claw_machines.append(ClawMachine(button_a, button_b, prize_location))
            # Empty line
            line = infile.readline()
        return claw_machines


def min_cost(claw_machine, a_cost=3, b_cost=1):
    ax, ay = claw_machine.button_a.x, claw_machine.button_a.y
    bx, by = claw_machine.button_b.x, claw_machine.button_b.y
    px, py = claw_machine.prize_location.x, claw_machine.prize_location.y

    # ax(x) + bx(x) = px
    # ay(y) + by(y) = py

    # Eliminate a pushes
    l = math.lcm(ax, ay)
    bx_ = bx * (l // ax)
    by_ = by * (l // ay)
    px_ = px * (l // ax)
    py_ = py * (l // ay)

    # Solve for b pushes
    b0 = bx_ - by_
    p0 = px_ - py_
    b_pushes = p0 / b0

    # Solve for a pushes
    # ax = tx - bx
    a_pushes = (px - (b_pushes * bx)) / ax

    # Only return integer solutions
    a_pushes, b_pushes = int(a_pushes), int(b_pushes)
    if (a_pushes * ax) + (b_pushes * bx) == px and (a_pushes * ay) + (b_pushes * by) == py:
        return (a_cost * a_pushes) + (b_cost * b_pushes)
    return None


def solve1(claw_machines, a_cost=3, b_cost=1):
    soln = 0
    for claw_machine in claw_machines:
        cost = min_cost(claw_machine, a_cost, b_cost)
        if cost is not None:
            soln += cost
    return soln


def test_solve1():
    claw_machines = parse_input(os.path.join('data', 'test13a.txt'))
    assert solve1(claw_machines) == 480


def solve2(claw_machines, a_cost=3, b_cost=1, delta=10000000000000):
    delta_vector = Vector(delta, delta)
    soln = 0
    for claw_machine in claw_machines:
        claw_machine0 = ClawMachine(
            claw_machine.button_a, claw_machine.button_b,
            claw_machine.prize_location + delta_vector
        )
        cost = min_cost(claw_machine0, a_cost, b_cost)
        if cost is not None:
            soln += cost
    return soln


def main():
    "Main program"
    claw_machines = parse_input(os.path.join('data', 'input13.txt'))
    soln = solve1(claw_machines)
    print('Part 1:', soln)
    assert soln == 29023
    soln = solve2(claw_machines)
    print('Part 2:', soln)
    assert soln == 96787395375634
    pyperclip.copy(soln)


if __name__ == '__main__':
    main()