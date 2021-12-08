#!/bin/env python3
"""
Advent Of Code 2021 Day 8
"""

import sys
import time
import collections
from typing import Set


all_segments_set = set('abcdefg')

per_number_segments = [
    'abcefg',   # 0
    'cf',       # 1
    'acdeg',    # 2
    'acdfg',    # 3
    'bcdf',     # 4
    'abdfg',    # 5
    'abdefg',   # 6
    'acf',      # 7
    'abcdefg',  # 8
    'abcdfg',   # 9
]

segments_to_number = {segments : number for number, segments in enumerate(per_number_segments)}


class WireSegment:
    def __init__(self) -> None:
        self.broken_to_real_seg: dict[str, str] = {}

    def solve(self, signal_patterns: list[str]) -> None:
        known_numbers: dict[int, set[str]] = {}
        real_to_broken_seg = {}
        signals_by_len = collections.defaultdict(list)
        for signal in signal_patterns:
            signals_by_len[len(signal)].append(signal)

        # Add the unique numbers
        known_numbers[1] = set(signals_by_len[2][0])
        known_numbers[4] = set(signals_by_len[4][0])
        known_numbers[7] = set(signals_by_len[3][0])

        # 'a' segment is the segment that is present in 7 but not 1
        real_to_broken_seg['a'] = (known_numbers[7] - known_numbers[1]).pop()

        # Find the segments that the signals of length 6 have in common
        # This translates to the numbers 0, 6 and 9
        # The true segments these have in common are a, b, f and g
        len6_in_common = set.intersection(*[set(signal) for signal in signals_by_len[6]])

        # Since 7 uses segments a, c and f taking out the above leaves segment c
        real_to_broken_seg['c'] = (known_numbers[7] - len6_in_common).pop()
        # Now 'c' is known the other segment for 1 is 'f'
        real_to_broken_seg['f'] = (known_numbers[1] - set(real_to_broken_seg['c'])).pop()

        # And so on...
        real_to_broken_seg['g'] = (len6_in_common - known_numbers[4] - set(real_to_broken_seg['a'])).pop()
        real_to_broken_seg['b'] = (len6_in_common - set(real_to_broken_seg.values())).pop()
        real_to_broken_seg['d'] = (known_numbers[4] - set(real_to_broken_seg.values())).pop()
        real_to_broken_seg['e'] = (all_segments_set - set(real_to_broken_seg.values())).pop()

        # Flip the mapping to something useful
        self.broken_to_real_seg = {broken : real for real, broken in real_to_broken_seg.items()}

    def decode(self, value: str) -> int:
        decoded_str = ''.join(sorted([self.broken_to_real_seg[segment] for segment in value]))
        return segments_to_number[decoded_str]


def p2(input_file: str) -> int:
    result = 0
    with open(input_file) as f:
        for line in f:
            signal_patterns, output_values = line.strip().split(' | ')
            wire_segment = WireSegment()
            wire_segment.solve(signal_patterns.split())
            output_val_str = ''
            for output_value in output_values.split():
                output_val_str += str(wire_segment.decode(output_value))
            result += int(output_val_str)

    return result


def p1(input_file: str) -> int:
    unique_display_lens = {2, 3, 4, 7}
    unique_count = 0
    with open(input_file) as f:
        for line in f:
            signal_patterns, output_value = line.strip().split(' | ')
            for display in output_value.split():
                if len(display) in unique_display_lens:
                    unique_count += 1

    return unique_count


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))