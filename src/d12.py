#!/bin/env python3
"""
Advent Of Code 2021 Day 12
"""

from __future__ import annotations

import sys
import time
import collections

from typing import Optional

GraphType = dict[str, "Node"]


class Node:
    all: GraphType = {}

    def __init__(self, name: str) -> None:
        self.name = name
        self.isstart = name == 'start'
        self.isend = name == 'end'
        self.islower = name.islower()
        self.connects: list[Node] = []

    def add_link(self, to_node: Node) -> None:
        self.connects.append(to_node)

    @classmethod
    def from_name(cls, name: str) -> Node:
        node = cls.all.get(name, None)
        if not node:
            node = cls(name)
            cls.all[name] = node
        return node


class Path:
    def __init__(self, path: list[str],
                 visited_lower_twice: bool = False,
                 unique_nodes: Optional[set[str]] = None) -> None:
        self.path = path
        self.visited_lower_twice = visited_lower_twice # Should really calculate this from the paths
        self.unique_nodes = unique_nodes if unique_nodes else set(self.path)

    def add_node(self, node: Node) -> Path:
        visited_lower_twice = self.visited_lower_twice or (node.islower and node.name in self.unique_nodes)
        return Path(self.path + [node.name], visited_lower_twice, self.unique_nodes | set([node.name]))

    def can_visit(self, node: Node) -> bool:
        if self.visited_lower_twice and node.islower:
            return node.name not in self.unique_nodes
        else:
            return True


def extend_paths_to_end(graph: GraphType, from_node: Node, paths: list[Path]) -> list[Path]:
    if not paths or from_node.isend:
        return paths

    paths_to_end = []
    for next_node in from_node.connects:
        if next_node.isstart:
            continue
        paths_to_extend = [p.add_node(next_node) for p in paths if p.can_visit(next_node)]
        paths_to_end += extend_paths_to_end(graph, next_node, paths_to_extend)
    return paths_to_end


def p1p2(input_file: str) -> tuple[int, int]:
    complete_paths = []
    Node.all = {}
    with open(input_file) as f:
        for line in f:
            n1_name, n2_name = line.strip().split('-')
            n1 = Node.from_name(n1_name)
            n2 = Node.from_name(n2_name)
            n1.add_link(n2)
            n2.add_link(n1)
    
    complete_paths = extend_paths_to_end(Node.all,  Node.from_name('start'), [Path(['start'])])

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