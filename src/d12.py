#!/bin/env python3
"""
Advent Of Code 2021 Day 11
"""

import sys
import time
import collections


def extend_paths_to_end(graph: dict[str, set[str]], from_node: str, paths: list[list[str]]) -> list[list[str]]:
    if not paths or from_node == 'end':
        return paths

    paths_to_end = []
    for next_node in graph[from_node]:
        if next_node.islower():
            paths_to_extend = [p + [next_node] for p in paths if next_node not in p]
        else:
            paths_to_extend = [p + [next_node] for p in paths]
        paths_to_end += extend_paths_to_end(graph, next_node, paths_to_extend)
    return paths_to_end


def p1p2(input_file: str) -> tuple[int, int]:
    graph = collections.defaultdict(set)
    complete_paths = []

    with open(input_file) as f:
        for line in f:
            n1, n2 = line.strip().split('-')
            graph[n1].add(n2)
            graph[n2].add(n1)
    
    complete_paths = extend_paths_to_end(graph, 'start', [['start']])

    return (len(complete_paths), 0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))