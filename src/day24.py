import dataclasses
import operator
import os
import sys

import pyperclip


GATES = {
    'AND': operator.and_,
    'OR': operator.or_,
    'XOR': operator.xor
}


@dataclasses.dataclass(frozen = True)
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
    print(device_values)
    print(operations)
    assert solve1(device_values, operations) == 2024


def main():
    """Main program"""
    device_values, operations = parse_input(os.path.join('data', 'input24.txt'))
    soln = solve1(device_values, operations)
    print('Part 1:', soln)
    assert soln == 52038112429798
    pyperclip.copy(soln)


if __name__ == '__main__':
    main()