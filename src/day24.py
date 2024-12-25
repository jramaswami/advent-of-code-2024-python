import collections
import dataclasses
import itertools
import operator
import os
import sys

import pyperclip


GATES = {
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor
}


@dataclasses.dataclass(frozen = False)
class Operation:
    left_device: str
    gate: str
    right_device: str
    output_device: str


def parse_input(filepath):
    device_values = dict()
    operations = []
    parsing_device_values = True
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if not line and parsing_device_values:
                parsing_device_values = False
            elif parsing_device_values:
                device, value = line.split(': ')
                device_values[device] = int(value)
            else:
                input_string, output_device = line.split(' -> ')
                left_device, gate, right_device = input_string.split()
                operations.append(Operation(left_device, gate, right_device, output_device))
    return device_values, operations


def solve1(original_device_values, operations):
    # Make a copy so we do not mutate the original device values
    device_values = {k: v for k, v in original_device_values.items()}

    # Make sure we have all devices in our memory
    for operation in operations:
        if operation.left_device not in device_values:
            device_values[operation.left_device] = None
        if operation.right_device not in device_values:
            device_values[operation.right_device] = None
        if operation.output_device not in device_values:
            device_values[operation.output_device] = None

    # Determine how many z devices have no value
    z_devices_with_no_value = 0
    for device in device_values:
        if device.startswith('z') and device_values[device] is None:
            z_devices_with_no_value += 1

    # Go until there are no more z devices with no value
    while z_devices_with_no_value:
        for operation in operations:
            left_value = device_values[operation.left_device]
            right_value = device_values[operation.right_device]
            if left_value is not None and right_value is not None:
                if operation.output_device.startswith('z') and device_values[operation.output_device] is None:
                    z_devices_with_no_value -= 1
                device_values[operation.output_device] = GATES[operation.gate](left_value, right_value)

    # Compute binary number produced by the z devices
    soln = 0
    for device in reversed(sorted(device_values)):
        if device.startswith('z'):
            soln = soln << 1
            soln += device_values[device]
    return soln


def test_solve1():
    device_values, operations = parse_input(os.path.join('data', 'test24a.txt'))
    assert solve1(device_values, operations) == 4
    device_values, operations = parse_input(os.path.join('data', 'test24b.txt'))
    # print(device_values)
    # print(operations)
    assert solve1(device_values, operations) == 2024


def pp(device, formulas, depth=0):
    # If device is an x or y device, print the formula
    # print(f'pp({device=}, ..., {depth=})')
    padding = ' ' * depth
    if device[0] in 'xy':
        return padding  + device
    # Otherwise, recurse
    op, x, y = formulas[device]
    return f'{padding}{op}({device})\n{pp(x, formulas, depth+1)}\n{pp(y, formulas, depth+1)}'


def interactive(formulas):
    print(sorted(formulas.keys()))
    device = input('Enter device:')
    while device:
        try:
            print(pp(device, formulas))
        except:
            print('Cannot find', device)
        device = input('Enter device: ')


def plot(operations):
    arrowheads = {
        'AND': 'diamond',
        'XOR': 'normal',
        'OR': 'dot'
    }
    with open('day24.dot', 'w') as outfile:
        outfile.write('digraph G {\n')
        for operation in operations:
            arrowhead = arrowheads[operation.gate]
            outfile.write(f'  {operation.left_device} -> {operation.output_device} [arrowhead={arrowhead}];\n')
            outfile.write(f'  {operation.right_device} -> {operation.output_device} [arrowhead={arrowhead}];\n')
        outfile.write('}')


def make_device(prefix, num):
    return f'{prefix}{num:02d}'


def vz(formulas, device, bit):
    """Verify device as z value for the given bit number"""
    # print('vz', device, bit)
    op, x, y = formulas[device]
    # A valid z value is x[n] XOR y[n] XOR carry[n-1]
    if op !='XOR':
        return False
    if bit == 0:
        # For the zero-th bit the valid z value is x[0] XOR y[0] because
        # there is no carry value to XOR
        return sorted([x,y]) == ['x00', 'y00']
    # We will call x[n] XOR y[n] an intermediate xor
    # The formula has only two inputs x, y
    # So x is x[n] XOR y[n] and y is a carry bit
    # or x is the carry bit and y is x[n] XOR y[n]
    return (
        (vix(formulas, x, bit) and vcb(formulas, y, bit))
        or
        (vcb(formulas, x, bit) and vix(formulas, y, bit))
    )


def vix(formulas, device, bit):
    """Verify intermediate xor"""
    # print('vix', device, bit)
    op, x, y = formulas[device]
    # Formula should be x[n] XOR y[n]
    if op != 'XOR':
        return False
    return sorted([x, y]) == [make_device('x', bit), make_device('y', bit)]


def vcb(formulas, device, bit):
    """Verify carry bit"""
    # print('vcb', device, bit)
    op, x, y = formulas[device]
    # For bit 1, the carry is from the zero-th bit which is just x[0] AND y[0]
    if bit == 1:
        if op != 'AND':
            return False
        return sorted([x, y]) == ['x00', 'y00']
    # For all other bits, the carry formula is:
    # ((x[n] XOR y[n]) AND carry[n-1]) OR (x[n] AND y[n])
    if op != 'OR':
        return False

    x_has_direct_carry = vdc(formulas, x, bit-1) and vrc(formulas, y, bit-1)
    y_has_direct_carry = vdc(formulas, y, bit-1) and vrc(formulas, x, bit-1)
    result = x_has_direct_carry or y_has_direct_carry
    return result


def vdc(formulas, device, bit):
    """Verify direct carry"""
    op, x, y = formulas[device]
    # Direct carry is x[n] AND y[n]
    if op != 'AND':
        return False
    return sorted([x, y]) == [make_device('x', bit), make_device('y', bit)]
    

def vrc(formulas, device, bit):
    """Verify recarry"""
    op, x, y = formulas[device]
    # Recarry is (x[n] XOR y[n]) AND carry[n]
    if op != 'AND':
        return False
    # So x is (x[n] XOR y[n]) and y is carry[n]
    # Or y is (x[n] XOR y[n]) and x is carry[n]
    return (
        (vix(formulas, x, bit) and vcb(formulas, y, bit))
        or
        (vix(formulas, y, bit) and vcb(formulas, x, bit))
    )


def verify(formulas, num):
    return vz(formulas, make_device('z', num), num)


def solve2(device_values, operations):
    """Use the v* functions to verify gates interactively to find devices
    not wired properly

    Verification functions came from HyperNeutrino's YouTube video:
    https://www.youtube.com/watch?v=SU6lp6wyd3I
    """
    # Convert operations into formulas
    swaps = {
        'kwb': 'z12',
        'z12': 'kwb',
        'qkf': 'z16',
        'z16': 'qkf',
        'tgr': 'z24',
        'z24': 'tgr',
        'jqn': 'cph',
        'cph': 'jqn',
    }
    formulas = {}
    for operation in operations:
        if operation.output_device in swaps:
            operation.output_device = swaps[operation.output_device]
        formulas[operation.output_device] = (operation.gate, operation.left_device, operation.right_device)
    
    ok = True
    n = 0
    while ok:
        ok = verify(formulas, n)
        n += 1

    return ','.join(sorted(swaps))


def main():
    """Main program"""
    device_values, operations = parse_input(os.path.join('data', 'input24.txt'))
    soln = solve1(device_values, operations)
    print('Part 1:', soln)
    assert soln == 52038112429798
    soln = solve2(device_values, operations)
    print('Part 2:', soln)
    assert soln == 'cph,jqn,kwb,qkf,tgr,z12,z16,z24'
    pyperclip.copy(soln)


if __name__ == '__main__':
    main()
