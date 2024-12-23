import collections
import itertools
import os
import sys

import pyperclip


def parse_input(filepath):
    graph = collections.defaultdict(set)
    with open(filepath, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line:
                u, v = (x.strip() for x in line.split('-'))
                graph[u].add(v)
                graph[v].add(u)
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


def solve2(graph):
    """Find the maximal clique"""
    max_clique = None
    max_clique_length = 0
    nodes = list(graph.keys())
    visited = set()
    for root in nodes:
        if root not in visited:
            # Try to find a maximal clique from here
            clique = set()
            clique.add(root)
            for node in nodes:
                if graph[node].issuperset(clique):
                    clique.add(node)
            visited.update(clique)
            if len(clique) > max_clique_length:
                max_clique = clique
                max_clique_length = len(clique)
    return ','.join(sorted(max_clique))


def test_solve2():
    graph = parse_input(os.path.join('data', 'test23a.txt'))
    assert solve2(graph) == 'co,de,ka,ta'


def main():
    """Main program"""
    graph = parse_input(os.path.join('data', 'input23.txt'))
    soln = solve1(graph)
    print('Part 1:', soln)
    assert soln == 1370
    soln = solve2(graph)
    print('Part 2:', soln)
    pyperclip.copy(soln)
    assert soln == 'am,au,be,cm,fo,ha,hh,im,nt,os,qz,rr,so'


if __name__ == '__main__':
    sys.exit(main())