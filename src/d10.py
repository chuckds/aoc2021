#!/bin/env python3
"""
Advent Of Code 2021 Day 10
"""

import sys
import time
import collections


open_2_close = {'(' : ')', '[' : ']', '{' : '}', '<' : '>'}
illegal_2_score = {')' : 3, ']' : 57, '}' : 1197, '>' : 25137}
complete_2_score = {')' : 1, ']' : 2, '}' : 3, '>' : 4}


def p1p2(input_file: str) -> tuple[int, int]:
    corrupt_score = 0
    complete_scores: list[int] = []
    with open(input_file) as f:
        for line in f:
            expected_closes: collections.deque[str] = collections.deque()
            corrupt = False
            for char in line.strip():
                expected_close = open_2_close.get(char, None)
                if expected_close:
                    # This char is an opening char, add the expected close to the deque
                    expected_closes.append(expected_close)
                else:
                    # This char is a closing char, expected or illegal?
                    expected_close = expected_closes.pop()
                    corrupt = expected_close != char
                    if corrupt:
                        corrupt_score += illegal_2_score[char]
                        break
            if not corrupt:
                # Incomplete line
                line_complete_score = 0
                while expected_closes:
                    char = expected_closes.pop()
                    line_complete_score *= 5
                    line_complete_score += complete_2_score[char]
                complete_scores.append(line_complete_score)

    print(f"{complete_scores=}")
    return (corrupt_score, sorted(complete_scores)[len(complete_scores) // 2])


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))