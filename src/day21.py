import collections
import dataclasses
import os
import sys


@dataclasses.dataclass(frozen = True)
class Vector:
    row :int
    col :int

    def manhattan_distance(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)


################################### KEYPADS ####################################

NUMBER_PAD = tuple(tuple(row) for row in '789\n456\n123\n 0A'.split('\n'))
DIRECTION_PAD = tuple(tuple(row) for row in ' ^A\n<v>'.split('\n'))

NP_LOCATIONS = dict()
for r, row in enumerate(NUMBER_PAD):
    for c, val in enumerate(row):
        if val != ' ':
            NP_LOCATIONS[val] = Vector(r, c)

DP_LOCATIONS = dict()
for r, row in enumerate(DIRECTION_PAD):
    for c, val in enumerate(row):
        if val != ' ':
            DP_LOCATIONS[val] = Vector(r, c)

################################################################################


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        data = tuple(line.strip() for line in infile if line.strip())
    return data


def parse_expected(filepath):
    """Parse result file and return a dictionary where the key
    is the code and the value is the length of the expected sequence
    after three translations.
    """
    data = {}
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:
                code, sequence = line.split(': ')
                data[code] = len(sequence.strip())
    return data


def translate(code, keypad_locations):
    # Starts at 'A' button
    translation = []
    curr_key = keypad_locations['A']
    curr_key_val = 'A'
    for next_key_val in code:
        next_key = keypad_locations[next_key_val]
        dr = next_key.row - curr_key.row
        dc = next_key.col - curr_key.col
        extension = ''
        if dc < 0:
            extension += ('<'*abs(dc))
        elif dc > 0:
            extension += ('>'*abs(dc))
        if dr < 0:
            extension += ('^'*abs(dr))
        elif dr > 0:
            extension += ('v'*abs(dr))
        print('curr', curr_key, curr_key_val, 'next', next_key, next_key_val, f'{dr=} {dc=}', extension)
        translation.append(extension)
        curr_key = next_key
        curr_key_val = next_key_val
        # Press curr_key
        translation.append('A')
    return ''.join(translation)


def shortest_sequence_length(original_code, translations):
    code = original_code
    keypad_locations = NP_LOCATIONS
    print(code, len(code))
    for _ in range(translations):
        code = translate(code, keypad_locations)
        print(code, len(code))
        keypad_locations = DP_LOCATIONS
    return len(code)


def test_shortest_sequence_length():
    codes = parse_input(os.path.join('data', 'test21a.txt'))
    expected = parse_expected(os.path.join('data', 'expected21a.txt'))
    for code in codes:
        print('*' * 40, code, '*' * 40)
        assert shortest_sequence_length(code, 3) == expected[code]


def solve1(original_code, translations=3):
    pass

def main():
    "Main program"


if __name__ == '__main__':
    sys.exit(main())