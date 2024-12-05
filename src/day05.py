import collections
import os
import sys

import pyperclip


def parse_input(filepath):
    edges = []
    updates = []
    with open(filepath, 'r') as infile:
        for line in infile:
        # Parse edges first
            line = line.strip()
            if not line:
                break
            edge = tuple(int(x.strip()) for x in line.split('|'))
            edges.append(edge)
        # Parse updates
        for line in infile:
            line = line.strip()
            if line:
                update = tuple(int(i) for i in line.split(','))
                updates.append(update)
        return edges, updates


def is_in_order(edges, update):
        # Filter to just the edges containing only nodes in current update
        graph = collections.defaultdict(list)
        indegree = collections.defaultdict(int)
        for u, v in edges:
            if u in update and v in update:
                graph[u].append(v)
                indegree[v] += 1

        # For each update in the order, when take then page should
        # have indegree of zero
        for u in update:
            if indegree[u] > 0:
                return False
            # Remove all edges starting with u
            for v in graph[u]:
                indegree[v] -= 1
        return True


def test_is_in_order():
    edges, updates = parse_input(os.path.join('data', 'test05a.txt'))
    expected_results = [True, True, True, False, False, False]
    for update, expected in zip(updates, expected_results):
        result = is_in_order(edges, update)
        assert result == expected


def solve1(edges, updates):
    soln = 0
    for update in updates:
        if is_in_order(edges, update):
            i = len(update) // 2
            middle_value = update[i]
            soln += middle_value
    return soln


def test_solve1():
    edges, updates = parse_input(os.path.join('data', 'test05a.txt'))
    assert solve1(edges, updates) == 143


def main():
    "Main program"
    # edges, updates = parse_input(os.path.join('data', 'test05a.txt'))
    edges, updates = parse_input(os.path.join('data', 'input05.txt'))
    soln = solve1(edges, updates)
    print('Part 1:', soln)
    assert soln == 5964

    pyperclip.copy(soln)


if __name__ == '__main__':
    main()