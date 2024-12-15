import os
import logging
import sys

import pyperclip



def configure_logging(log_level):
    logger = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    fh = logging.FileHandler('log15.txt', 'w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.setLevel(log_level)


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        lines = [line.strip() for line in infile]

    grid = []
    instructions = []
    reading = 'grid'
    for line in lines:
        if not line:
            reading = 'instructions'
        elif reading == 'grid':
            grid.append(tuple(line))
        elif reading == 'instructions':
            instructions.extend(list(line))
    return tuple(grid), tuple(instructions)



def grid_to_string(grid, not_boxes, robot):
    grid0 = [['O' for _ in row] for row in grid]
    for r, c in not_boxes:
        if grid[r][c] == '#':
            grid0[r][c] = '#'
        else:
            grid0[r][c] = '.'
    grid0[robot[0]][robot[1]] = '@'
    return '\n'.join(''.join(row) for row in grid0)


def solve1(grid, instructions):
    logger = logging.getLogger()

    R, C = 0, 1
    N, M = len(grid), len(grid[0])

    not_boxes = set()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == '@':
                robot = r, c
            if val != 'O':
                not_boxes.add((r, c))

    logger.info('Initial grid:\n%s', grid_to_string(grid, not_boxes, robot))

    for i, instruction in enumerate(instructions):
        logger.debug('Robot currently located at %s', robot)
        logger.info('Instruction %d: %s', i, instruction)
        match instruction:
            case '>':
                # Find the least not box greater than the robot in the current row
                logger.debug('Not boxes in same row: %s', [nb for nb in not_boxes if nb[R] == robot[R]])
                target_posn = (robot[R], M-1)
                for not_box in not_boxes:
                    if not_box[R] == robot[R] and robot[C] < not_box[C]:
                        target_posn = min(target_posn, not_box)
                # If the target position is a space then swap the space to the
                # robot and move the robot
                logger.debug('Target posn = %s', target_posn)
                if grid[target_posn[R]][target_posn[C]] != '#':
                    not_boxes.remove(target_posn)
                    not_boxes.add(robot)
                    robot = (robot[R], robot[C]+1)
                    not_boxes.add(robot)
            case '<':
                # Find the greatest not box less than the robot in the current row
                logger.debug('Not boxes in same row: %s', [nb for nb in not_boxes if nb[R] == robot[R]])
                target_posn = (robot[R], 0)
                for not_box in not_boxes:
                    if not_box[R] == robot[R] and not_box[C] < robot[C]:
                        target_posn = max(target_posn, not_box)
                # If the target position is a space then swap the space to the
                # robot and move the robot
                if grid[target_posn[R]][target_posn[C]] != '#':
                    not_boxes.remove(target_posn)
                    not_boxes.add(robot)
                    robot = (robot[R], robot[C]-1)
                    not_boxes.add(robot)
            case '^':
                # Find the greatest not box less than robot in the current column
                target_posn = (0, robot[C])
                logger.debug('Not boxes in same column: %s', [nb for nb in not_boxes if nb[C] == robot[C]])
                for not_box in not_boxes:
                    if not_box[C] == robot[C] and not_box[R] < robot[R]:
                        target_posn = max(target_posn, not_box)
                logger.debug('Target posn = %s', target_posn)
                # If the target position is a space then swap the space to the
                # robot and move the robot
                if grid[target_posn[R]][target_posn[C]] != '#':
                    not_boxes.remove(target_posn)
                    not_boxes.add(robot)
                    robot = (robot[R]-1, robot[C])
                    not_boxes.add(robot)
            case 'v':
                # Find the least not box greater than robot in the current column
                target_posn = (N-1, robot[C])
                logger.debug('Not boxes in same column: %s', [nb for nb in not_boxes if nb[C] == robot[C]])
                for not_box in not_boxes:
                    if not_box[C] == robot[C] and robot[R] < not_box[R]:
                        target_posn = min(target_posn, not_box)
                # If the target position is a space then swap the space to the
                # robot and move the robot
                logger.debug('Target posn = %s %s', target_posn)
                if grid[target_posn[R]][target_posn[C]] != '#':
                    not_boxes.remove(target_posn)
                    not_boxes.add(robot)
                    robot = (robot[R]+1, robot[C])
                    not_boxes.add(robot)
            case other_instruction:
                raise ValueError(f'Unrecognized instruction: {other_instruction}')

        logger.info('Grid:\n%s', grid_to_string(grid, not_boxes, robot))

    soln = 0
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            if (r, c) not in not_boxes:
                # (r, c) is a box
                soln += (100 * r) + c
    return soln


def test_solve1():
    grid, instructions = parse_input(os.path.join('data', 'test15a.txt'))
    assert solve1(grid, instructions) == 2028
    grid, instructions = parse_input(os.path.join('data', 'test15b.txt'))
    assert solve1(grid, instructions) == 10092


def main():
    "Main program"
    # Configure logging
    configure_logging(logging.INFO)
    grid, instructions = parse_input(os.path.join('data', 'input15.txt'))
    soln = solve1(grid, instructions)
    print('Part 1:', soln)
    assert soln == 1509863
    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())