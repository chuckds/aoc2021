#!/bin/env python3
"""
Advent Of Code 2021 Day 12
"""

from __future__ import annotations

import sys
import time
import collections


class Path:
    def __init__(self, path: list[str], visited_lower_twice: bool = False) -> None:
        self.path = path
        self.visited_lower_twice = visited_lower_twice # Should really calculate this from the paths

    def add_node(self, node: str) -> Path:
        visited_lower_twice = self.visited_lower_twice or (node.islower() and node in self.path)
        return Path(self.path + [node], visited_lower_twice)

    def can_visit(self, node: str) -> bool:
        if self.visited_lower_twice and node.islower():
            return node not in self.path
        else:
            return True


def extend_paths_to_end(graph: dict[str, set[str]], from_node: str, paths: list[Path]) -> list[Path]:
    if not paths or from_node == 'end':
        return paths

    paths_to_end = []
    for next_node in graph[from_node]:
        if next_node == 'start':
            continue
        paths_to_extend = [p.add_node(next_node) for p in paths if p.can_visit(next_node)]
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
    
    complete_paths = extend_paths_to_end(graph, 'start', [Path(['start'])])

    return (len([p for p in complete_paths if not p.visited_lower_twice]),
            len(complete_paths))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))