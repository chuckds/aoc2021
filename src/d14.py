#!/bin/env python3
"""
Advent Of Code 2021 Day 14
"""

from __future__ import annotations

import sys
import time
import collections


def p1p2(input_file: str) -> tuple[int, int]:
    pair_insertion_rules = {}
    with open(input_file) as f:
        polymer_template = next(f).strip()
        next(f)
        for line in f:
            pair, inserted_char = line.strip().split(' -> ')
            pair_insertion_rules[pair] = inserted_char

    #steps = 40
    steps = 11
    p1_steps = 10
    polymer = list(polymer_template)
    for step in range(steps):
        start = time.perf_counter()
        if step == p1_steps:
            p1_polymer = polymer[:]
        next_polymer = []
        for pair_num in range(len(polymer) - 1):
            char_to_add = pair_insertion_rules.get(''.join(polymer[pair_num:pair_num + 2]), '')
            next_polymer.append(polymer[pair_num])
            next_polymer.append(char_to_add)
        next_polymer.append(polymer[-1])
        polymer = next_polymer
        print(f"Step {step}: len {len(polymer)} Elapsed: {time.perf_counter() - start:.6f}s")

    p1_char_counts_sorted = sorted((count for count in collections.Counter(p1_polymer).values()))
    char_counts_sorted = sorted((count for count in collections.Counter(polymer).values()))
    p2_result = char_counts_sorted[-1] - char_counts_sorted[0]
    return (p1_char_counts_sorted[-1] - p1_char_counts_sorted[0],
            0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))