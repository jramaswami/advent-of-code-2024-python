import collections
import dataclasses
import os
import sys

import pyperclip


@dataclasses.dataclass(frozen=True)
class FileBlock:
    block_id: int
    size: int


@dataclasses.dataclass(frozen=True)
class EmptySpace:
    size: int


def parse_input(filepath):
    with open(filepath, 'r') as infile:
        data = [int(x) for x in infile.read().strip()]
    return data


def S(n):
    """Return the sum of 1..n"""
    return (n * (n+1)) // 2


def parse_disk_map(disk_map):
    """Parse the disk map into FileBlocks and EmptySpace"""
    disk_map0 = collections.deque()
    for i, x in enumerate(disk_map):
        if i % 2:
            disk_map0.append(EmptySpace(x))
        else:
            disk_map0.append(FileBlock(i // 2, x))
    return disk_map0


def compress_disk_map1(disk_map0):
    """Compress the disk map according to the rules for first part of puzzle"""
    compressed_disk_map = []
    while disk_map0:
        curr_item = disk_map0.popleft()
        if isinstance(curr_item, FileBlock):
            compressed_disk_map.append(curr_item)
        else:
            # Fill empty space
            while curr_item.size > 0:
                if disk_map0:
                    itemr = disk_map0.pop()
                    if itemr.size <= curr_item.size:
                        # Fill as much space as possible with file blocks
                        compressed_disk_map.append(itemr)
                        # Reduce empty space by size of file blocks
                        curr_item = EmptySpace(curr_item.size - itemr.size)
                    else:
                        # Fill empty space
                        iteml = FileBlock(itemr.block_id, curr_item.size)
                        compressed_disk_map.append(iteml)
                        # Put remaining file blocks back
                        itemr = FileBlock(itemr.block_id, itemr.size - curr_item.size)
                        disk_map0.append(itemr)
                        # Set empty space to 0
                        curr_item = EmptySpace(0)

                    # Get rid of any empty space at the end
                    while disk_map0 and isinstance(disk_map0[-1], EmptySpace):
                        disk_map0.pop()
                else:
                    # We are out of file blocks
                    break
    return compressed_disk_map


def score_compressed_disk_map(compressed_disk_map):
    """Score the compressed disk map according to the rules"""
    score = 0
    curr_index = 0
    for item in compressed_disk_map:
        next_index = curr_index + item.size
        if isinstance(item, FileBlock):
            a = S(curr_index - 1)
            b = S(next_index - 1)
            item_score = (b-a) * item.block_id
            score += item_score
        curr_index = next_index
    return score


def solve1(disk_map):
    compressed_disk_map = compress_disk_map1(parse_disk_map(disk_map))
    return score_compressed_disk_map(compressed_disk_map)


def test_solve1():
    disk_map = parse_input(os.path.join('data', 'test09b.txt'))
    assert solve1(disk_map) == 1928


def find_space(disk_map, file_block):
    """Find the index of the leftmost EmptySpace that can hold the file_block

    Returns -1 if no EmptySpace is found
    """
    for i, item in enumerate(disk_map):
        if isinstance(item, EmptySpace) and file_block.size <= item.size:
            return i
    return -1


def move_file_block(disk_map, file_block, empty_space_index):
    """Create a new disk map with the file_block moved to the EmptySpace
    at empty_space_index
    """
    new_disk_map = collections.deque()
    for i, item in enumerate(disk_map):
        if i == empty_space_index:
            assert isinstance(item, EmptySpace)
            new_disk_map.append(file_block)
            if item.size - file_block.size > 0:
                new_disk_map.append(EmptySpace(item.size - file_block.size))
        else:
            new_disk_map.append(item)
    return new_disk_map


def compress_disk_map2(disk_map):
    """Compress the disk map according to the rules for second part of puzzle"""
    right_side = collections.deque()
    left_side = disk_map
    moved = set()
    while left_side:
        item = left_side.pop()
        if isinstance(item, EmptySpace):
            right_side.appendleft(item)
        else:
            if item.block_id in moved:
                right_side.appendleft(item)
            else:
                empty_space_index = find_space(left_side, item)
                if empty_space_index >= 0:
                    # Move file block
                    left_side = move_file_block(left_side, item, empty_space_index)
                    moved.add(item.block_id)
                    # Replace with empty space on right
                    right_side.appendleft(EmptySpace(item.size))
                else:
                    right_side.appendleft(item)
    return right_side


def solve2(disk_map):
    compressed_disk_map = compress_disk_map2(parse_disk_map(disk_map))
    return score_compressed_disk_map(compressed_disk_map)


def test_solve2():
    disk_map = parse_input(os.path.join('data', 'test09b.txt'))
    assert solve2(disk_map) == 2858


def main():
    "Main program"
    disk_map = parse_input(os.path.join('data', 'input09.txt'))
    soln = solve1(disk_map)
    print('Part 1:', soln)
    assert soln == 6283170117911

    soln = solve2(disk_map)
    print('Part 2:', soln)
    assert soln == 6307653242596

    pyperclip.copy(soln)


if __name__ == '__main__':
    sys.exit(main())