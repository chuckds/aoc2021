#!/bin/env python3
"""
Advent Of Code 2021 Day 12
"""

from __future__ import annotations

import sys
import time

GraphType = dict[str, "Cave"]


class Cave:
    def __init__(self, name: str) -> None:
        self.name = name
        self.isstart = name == 'start'
        self.isend = name == 'end'
        self.issmall = name.islower()
        self.connects: list[Cave] = []

    def add_link(self, to_node: Cave) -> None:
        self.connects.append(to_node)

    @classmethod
    def from_name(cls, name: str, graph: GraphType) -> Cave:
        node = graph.get(name, None)
        if not node:
            node = cls(name)
            graph[name] = node
        return node


class Path:
    def __init__(self, small_caves_visited: set[str],
                 visited_small_twice: bool = False) -> None:
        self.small_caves_visited = small_caves_visited
        self.has_visited_small_twice = visited_small_twice

    def add_node(self, node: Cave) -> Path:
        has_visited_small_twice = self.has_visited_small_twice
        small_caves_visited = self.small_caves_visited
        if node.issmall:
            if node.name in self.small_caves_visited:
                has_visited_small_twice = True
            else:
                # Only create a new set if we need to
                small_caves_visited = small_caves_visited | set([node.name])

        return Path(small_caves_visited, has_visited_small_twice)

    def can_visit(self, node: Cave) -> bool:
        if self.has_visited_small_twice and node.issmall:
            return node.name not in self.small_caves_visited
        else:
            return True


def extend_path_to_end(from_node: Cave, path: Path) -> list[Path]:
    if from_node.isend:
        return [path]

    paths_to_end = []
    for next_cave in from_node.connects:
        if path.can_visit(next_cave):
            paths_to_end += extend_path_to_end(next_cave, path.add_node(next_cave))
    return paths_to_end


def p1p2(input_file: str) -> tuple[int, int]:
    graph: GraphType = {}
    with open(input_file) as f:
        for line in f:
            n1_name, n2_name = line.strip().split('-')
            n1 = Cave.from_name(n1_name, graph)
            n2 = Cave.from_name(n2_name, graph)
            # Don't add links back to start or out of end
            if not n2.isstart and not n1.isend:
                n1.add_link(n2)
            if not n1.isstart and not n2.isend:
                n2.add_link(n1)
    
    complete_paths = extend_path_to_end(Cave.from_name('start', graph),
                                        Path(set()))

    return (len([p for p in complete_paths if not p.has_visited_small_twice]),
            len(complete_paths))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))