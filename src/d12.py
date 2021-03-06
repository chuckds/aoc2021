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
    def __init__(self, last_cave: Cave, small_caves_visited: frozenset[str],
                 visited_small_twice: bool = False) -> None:
        self.last_cave = last_cave
        self.small_caves_visited = small_caves_visited
        self.has_visited_small_twice = visited_small_twice

    def add_cave(self, cave: Cave) -> Path:
        has_visited_small_twice = self.has_visited_small_twice
        small_caves_visited = self.small_caves_visited
        if cave.issmall:
            if cave.name in self.small_caves_visited:
                has_visited_small_twice = True
            else:
                # Only create a new set if we need to
                small_caves_visited = small_caves_visited | frozenset([cave.name])

        return Path(cave, small_caves_visited, has_visited_small_twice)

    def can_visit(self, node: Cave) -> bool:
        if self.has_visited_small_twice and node.issmall and not node.isend:
            return node.name not in self.small_caves_visited
        else:
            return True


def graph_from_input(input_file: str) -> GraphType:
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
    return graph


def extend_path_to_end(path: Path) -> list[Path]:
    if path.last_cave.isend:
        return [path]

    paths_to_end = []
    for next_cave in path.last_cave.connects:
        if path.can_visit(next_cave):
            paths_to_end += extend_path_to_end(path.add_cave(next_cave))
    return paths_to_end


def p1p2(input_file: str) -> tuple[int, int]:
    graph = graph_from_input(input_file)
    complete_paths = extend_path_to_end(Path(Cave.from_name('start', graph),
                                        frozenset()))

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
