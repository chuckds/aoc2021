#!/bin/env python3
"""
Advent Of Code 2021 Day 14
"""

from __future__ import annotations

import sys
import time
import collections


class PatternNode:
    def __init__(self, patten: str) -> None:
        self.pattern = patten
        self.path_visits = 0
        self.paths = 0
        self.new_paths = 0
        self.connects: list[PatternNode] = []

    def __hash__(self) -> int:
        return hash(self.pattern)

    def score(self) -> dict[str, int]:
        score: dict[str, int] = collections.defaultdict(int)
        # paths is the number of times this pattern appears in the final string
        # so each char in this pattern gets that score
        for char in self.pattern:
            score[char] += self.paths
        # Every time this pattern has been "passed through" the middle characters
        # will have been double counted so remove those from the score
        for char in self.pattern[1:-1]:
            score[char] -= self.path_visits
        return score

    @classmethod
    def from_pattern(cls, pattern: str, graph: dict[str, PatternNode]) -> PatternNode:
        if pattern not in graph:
            graph[pattern] = cls(pattern)
        return graph[pattern]


class PolymerGraph:
    def __init__(self, head_pattern: str, polymer_mapping: dict[str, str]) -> None:
        self.head_pattern = head_pattern
        self.polymer_mapping = polymer_mapping
        self.graph: dict[str, PatternNode] = {}

    def construct(self) -> PatternNode:
        head_node = PatternNode.from_pattern(self.head_pattern, self.graph)
        nodes_to_walk = {head_node}
        while nodes_to_walk:
            node = nodes_to_walk.pop()
            # Loop through each character pair in this pattern and add a connection
            # to the resulting string
            for pair_num in range(len(node.pattern) - 1):
                connect_pattern = self.polymer_mapping[node.pattern[pair_num:pair_num + 2]]
                connect_node = PatternNode.from_pattern(connect_pattern, self.graph)
                node.connects.append(connect_node)
                if not connect_node.connects:
                    # Hasn't been walked yet so add it to the set to do so
                    nodes_to_walk.add(connect_node)
        return head_node

    def score(self) -> dict[str, int]:
        score: dict[str, int] = collections.defaultdict(int)
        for node in self.graph.values():
            score.update((char, score[char] + val)
                         for char, val in node.score().items())
        return score


def char_count_to_score(counter: dict[str, int]) -> int:
    counter_sorted = sorted((count for count in counter.values()))
    return counter_sorted[-1] - counter_sorted[0]


def p1p2(input_file: str) -> tuple[int, int]:
    polymer_mapping = {}
    with open(input_file) as f:
        polymer_template = next(f).strip()
        next(f)
        for line in f:
            pair, inserted_char = line.strip().split(' -> ')
            polymer_mapping[pair] = pair[0] + inserted_char + pair[1]

    graph = PolymerGraph(polymer_template, polymer_mapping)
    head = graph.construct()

    # Add the lonely single path to start
    head.paths += 1
    for step in range(40):
        for from_node in (n for n in graph.graph.values() if n.paths):
            # Some paths at this node waiting to finish
            # move them all on one step
            from_node.path_visits += from_node.paths
            for to_node in from_node.connects:
                to_node.new_paths += from_node.paths
        # Flip over to the new path counts for this step
        for node in graph.graph.values():
            node.paths = node.new_paths
            node.new_paths = 0
        if step == 9:
            p1_score = char_count_to_score(graph.score())

    return (p1_score, char_count_to_score(graph.score()))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))