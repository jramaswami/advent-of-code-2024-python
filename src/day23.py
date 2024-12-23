import collections
import itertools
import os
import sys

import pyperclip


def parse_input(filepath):
    graph = collections.defaultdict(list)
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:
                u, v = (x.strip() for x in line.split('-'))
                graph[u].append(v)
                graph[v].append(u)
    return graph


def solve1(graph):
    nodes = list(graph.keys())
    triplets = 0
    for a, b, c in itertools.combinations(nodes, 3):
        if any(x.startswith('t') for x in (a, b, c)):
            if b in graph[a] and c in graph[b] and c in graph[a]:
                triplets += 1
    return triplets


def test_solve1():
    graph = parse_input(os.path.join('data', 'test23a.txt'))
    assert solve1(graph) == 7


def main():
    """Main program"""
    graph = parse_input(os.path.join('data', 'input23.txt'))
    soln = solve1(graph)
    print('Part 1:', soln)
    pyperclip.copy(soln)
    assert soln == 1370


if __name__ == '__main__':
    sys.exit(main())