import logging
import os
import sys

import pyperclip


#
# Configure logging
#
def configure_logging():
    logger = logging.getLogger()
    fh = logging.FileHandler('log17.txt', 'w')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

configure_logging()


A, B, C = 0, 1, 2


def parse_register(line):
    _, value_token = (t.strip() for t in line.split(':'))
    return int(value_token)


def parse_program(line):
    _, opcodes_token = (t.strip() for t in line.split(':'))
    return tuple(int(x) for x in opcodes_token.split(','))


def parse_input(filepath):
    registers = []
    program = []
    with open(filepath, 'r') as infile:
        lines = [line.strip() for line in infile if line.strip()]
    for line in lines[:3]:
        registers.append(parse_register(line))
    program = parse_program(lines[-1])
    return registers, program


class Computer:
    def __init__(self, registers, program):
        self.original_registers = list(registers)
        self.registers = list(registers)
        self.program = program
        self.output = []
        self.ip = 0
        self.opcodes = [
            self.adv, self.bxl, self.bst, self.jnz,
            self.bxc, self.out, self.bdv, self.cdv
        ]

    def get_combo_value(self, operand):
        logging.debug('Retrieving value for combo operand %d', operand)
        if operand <= 3:
            return operand
        elif operand <= 6:
            return self.registers[operand-4]
        else:
            raise ValueError(f'Invalid combo operand: {operand}')

    def adv(self):
        logging.debug('adv @ %d', self.ip)
        operand = self.program[self.ip+1]
        numerator = self.registers[A]
        denominator = pow(2, self.get_combo_value(operand))
        result = numerator // denominator
        logging.debug('%d // %d = %d', numerator, denominator, result)
        logging.debug('Writing %d to register A', result)
        self.registers[A] = result
        self.ip += 2

    def bxl(self):
        logging.debug('bxl @ %d', self.ip)
        operand = self.program[self.ip+1]
        result = self.registers[B] ^ operand
        logging.debug('%d ^ %d = %d', self.registers[B], operand, result)
        logging.debug('Writing %d to register B', result)
        self.registers[B] = result
        self.ip += 2

    def bst(self):
        logging.debug('bst @ %d', self.ip)
        operand = self.program[self.ip+1]
        x = self.get_combo_value(operand)
        result = x % 8
        logging.debug('%d mod 8 = %d', x, result)
        logging.debug('Writing %d to register B', result)
        self.registers[B] = result
        self.ip += 2

    def jnz(self):
        logging.debug('jnz @ %d', self.ip)
        operand = self.program[self.ip+1]
        logging.debug('Register A = %d', self.registers[A])
        if self.registers[A] != 0:
            logging.debug('Jumping to %d', operand)
            self.ip = operand
        else:
            logging.debug('Proceeding to next instruction')
            self.ip += 2

    def bxc(self):
        logging.debug('bxc @ %d', self.ip)
        result = self.registers[B] ^ self.registers[C]
        logging.debug('%d ^ %d = %d', self.registers[B], self.registers[C], result)
        logging.debug('Writing %d to register B', result)
        self.registers[B] = result
        self.ip += 2

    def out(self):
        logging.debug('out @ %d', self.ip)
        operand = self.program[self.ip+1]
        x = self.get_combo_value(operand)
        result = x % 8
        logging.debug('%d mod 8 = %d', x, result)
        logging.debug('Writing %d to output', result)
        self.output.append(result)
        self.ip += 2

    def bdv(self):
        logging.debug('bdv @ %d', self.ip)
        operand = self.program[self.ip+1]
        numerator = self.registers[A]
        x = self.get_combo_value(operand)
        denominator = pow(2, x)
        logging.debug('Computing denominator 2 ^ %d = %d', x, denominator)
        result = numerator // denominator
        logging.debug('%d // %d = %d', numerator, denominator, result)
        logging.debug('Writing %d to register B', result)
        self.registers[B] = result
        self.ip += 2

    def cdv(self):
        logging.debug('cdv @ %d', self.ip)
        operand = self.program[self.ip+1]
        numerator = self.registers[A]
        x = self.get_combo_value(operand)
        denominator = pow(2, x)
        logging.debug('Computing denominator 2 ^ %d = %d', x, denominator)
        result = numerator // denominator
        logging.debug('%d // %d = %d', numerator, denominator, result)
        logging.debug('Writing %d to register C', result)
        self.registers[C] = result
        self.ip += 2

    def reset(self):
        self.registers = list(self.original_registers)
        self.ip = 0
        self.output = []

    def run(self):
        self.reset()
        logging.debug('Starting run ...')
        logging.debug('Registers = %s', self.registers)
        logging.debug('Program = %s', self.program)
        while self.ip < len(self.program):
            logging.debug('Executing instruction %d', self.ip)
            opcode = self.program[self.ip]
            self.opcodes[opcode]()
        logging.debug('Program halted %d', self.ip)


def test_computer():
    computer = Computer([0, 0, 9], (2, 6))
    computer.run()
    assert computer.registers[B] == 1

    computer = Computer([10, 0, 0], (5,0,5,1,5,4))
    computer.run()
    assert computer.output == [0, 1, 2]

    computer = Computer([2024, 0, 0], (0,1,5,4,3,0))
    computer.run()
    assert computer.output == [4,2,5,6,7,7,7,7,3,1,0]
    assert computer.registers[A] == 0

    computer = Computer([0, 29, 0], (1,7))
    computer.run()
    assert computer.registers[B] == 26

    computer = Computer([0, 2024, 43690], (4, 0))
    computer.run()
    assert computer.registers[B] == 44354


def solve1(registers, program):
    computer = Computer(registers, program)
    computer.run()
    return ','.join(str(x) for x in computer.output)


def test_solve1():
    registers, program = parse_input(os.path.join('data', 'test17a.txt'))
    assert solve1(registers, program) == '4,6,3,5,6,3,5,2,1,0'


def main():
    "Main program"
    registers, program = parse_input(os.path.join('data', 'input17.txt'))
    soln = solve1(registers, program)
    print('Part 1:', soln)
    assert soln == '7,3,0,5,7,1,4,0,5'
    pyperclip.copy(soln)


if __name__ == '__main__':
    main()