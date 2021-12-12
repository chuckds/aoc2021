#!/bin/env python3
"""
Advent Of Code 2021 Day 12
"""

from __future__ import annotations

import sys
import time

from typing import Optional

GraphType = dict[str, "Node"]


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.isstart = name == 'start'
        self.isend = name == 'end'
        self.islower = name.islower()
        self.connects: list[Node] = []

    def add_link(self, to_node: Node) -> None:
        self.connects.append(to_node)

    @classmethod
    def from_name(cls, name: str, graph: GraphType) -> Node:
        node = graph.get(name, None)
        if not node:
            node = cls(name)
            graph[name] = node
        return node


class Path:
    def __init__(self, lowercase_nodes_visited: set[str],
                 visited_lower_twice: bool = False) -> None:
        self.lowercase_nodes_visited = lowercase_nodes_visited
        self.visited_lower_twice = visited_lower_twice

    def add_node(self, node: Node) -> Path:
        visited_lower_twice = self.visited_lower_twice
        new_lowercase_nodes_visited = self.lowercase_nodes_visited
        if node.islower:
            if node.name in self.lowercase_nodes_visited:
                visited_lower_twice = True
            else:
                # Only create a new set if we need to
                new_lowercase_nodes_visited = new_lowercase_nodes_visited | set([node.name])

        return Path(new_lowercase_nodes_visited, visited_lower_twice)

    def can_visit(self, node: Node) -> bool:
        if self.visited_lower_twice and node.islower:
            return node.name not in self.lowercase_nodes_visited
        else:
            return True


def extend_paths_to_end(from_node: Node, paths: list[Path]) -> list[Path]:
    if not paths or from_node.isend:
        return paths

    paths_to_end = []
    for next_node in from_node.connects:
        paths_to_extend = [p.add_node(next_node) for p in paths if p.can_visit(next_node)]
        paths_to_end += extend_paths_to_end(next_node, paths_to_extend)
    return paths_to_end


def p1p2(input_file: str) -> tuple[int, int]:
    complete_paths = []
    graph: GraphType = {}
    with open(input_file) as f:
        for line in f:
            n1_name, n2_name = line.strip().split('-')
            n1 = Node.from_name(n1_name, graph)
            n2 = Node.from_name(n2_name, graph)
            if not n2.isstart and not n1.isend:
                # Don't add links back to start or out of end
                n1.add_link(n2)
            if not n1.isstart and not n2.isend:
                n2.add_link(n1)
    
    complete_paths = extend_paths_to_end(Node.from_name('start', graph),
                                         [Path(set())])

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