import dataclasses
import os
import sys

import pyperclip


INF = pow(10, 10)


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
    min_cost = INF
    for a_pushes in range(101):
        claw_location = (claw_machine.button_a * a_pushes)
        delta = claw_machine.prize_location - claw_location
        b_pushes = delta.x // claw_machine.button_b.x
        if (claw_machine.button_b * b_pushes) == delta:
            min_cost = min(min_cost, (a_cost * a_pushes) + (b_cost * b_pushes))
    return min_cost


def solve1(claw_machines, a_cost=3, b_cost=1):
    soln = 0
    for claw_machine in claw_machines:
        cost = min_cost(claw_machine, a_cost, b_cost)
        if cost < INF:
            soln += cost
    return soln


def test_solve1():
    claw_machines = parse_input(os.path.join('data', 'test13a.txt'))
    assert solve1(claw_machines) == 480


def main():
    "Main program"
    claw_machines = parse_input(os.path.join('data', 'input13.txt'))
    soln = solve1(claw_machines)
    print('Part 1:', soln)
    assert soln == 29023
    pyperclip.copy(soln)


if __name__ == '__main__':
    main()