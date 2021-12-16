#!/bin/env python3
"""
Advent Of Code 2021 Day 8
"""

import sys
import time
import collections
import dataclasses


num_to_unique_num_segments = {
    1: 2,
    4: 4,
    7: 3,
    8: 7,
}


@dataclasses.dataclass
class WireSegment:
    txt_to_num: dict[str, int] = dataclasses.field(default_factory=dict)
    known_num: dict[int, set[str]] = \
        dataclasses.field(default_factory=dict)

    def add_num_to_txt(self, num: int, txt: set[str]) -> None:
        self.txt_to_num[''.join(sorted(txt))] = num
        self.known_num[num] = txt

    def solve(self, signal_patterns: list[str]) -> None:
        real_to_broken_seg = {}
        signals_by_len = collections.defaultdict(list)
        for signal_str in signal_patterns:
            signals_by_len[len(signal_str)].append(set(signal_str))

        # Add the numbers with unique number of segments used: 1, 4, 7 and 8
        for number, num_segments in num_to_unique_num_segments.items():
            self.add_num_to_txt(number, signals_by_len[num_segments][0])

        # Find the segments that the signals of length 6 have in common
        # This translates to the numbers 0, 6 and 9
        # The true segments these have in common are a, b, f and g
        len6_in_common = set.intersection(
                                     *[signal for signal in signals_by_len[6]])

        # Since 7 uses segments a, c and f taking out the above leaves
        # segment c
        real_to_broken_seg['c'] = (
                  self.known_num[7] - len6_in_common).pop()
        # Now 'c' is known the other segment for 1 is 'f'
        real_to_broken_seg['f'] = (
                  self.known_num[1] - set(real_to_broken_seg['c'])).pop()
        # Segments in 4 not used by 1 are b and d - of these only b is in
        # len6_in_common leaving d
        real_to_broken_seg['d'] = (
                  self.known_num[4] - self.known_num[1] - len6_in_common).pop()

        # Identify the 3 numbers that use 5 segments (2, 3 and 5)
        for signal in signals_by_len[5]:
            if real_to_broken_seg['c'] not in signal:
                # Only 5 doesn't use segment c
                self.add_num_to_txt(5, signal)
            elif real_to_broken_seg['f'] not in signal:
                # Only 2 doesn't use segment f
                self.add_num_to_txt(2, signal)
            else:
                # Only 3 uses both c and f
                self.add_num_to_txt(3, signal)

        # Identify the 3 numbers that use 6 segments (0, 6 and 9)
        for signal in signals_by_len[6]:
            if real_to_broken_seg['c'] not in signal:
                # Only 6 doesn't use c
                self.add_num_to_txt(6, signal)
            elif real_to_broken_seg['d'] not in signal:
                # Only 0 doesn't use d
                self.add_num_to_txt(0, signal)
            else:
                # Only 9 uses both c and d
                self.add_num_to_txt(9, signal)

    def decode(self, value: str) -> int:
        return self.txt_to_num[''.join(sorted(value))]


def p1p2(input_file: str) -> tuple[int, int]:
    unique_count = 0
    output_value_sum = 0
    with open(input_file) as f:
        for line in f:
            signal_patterns, output_values = line.strip().split(' | ')
            wire_segment = WireSegment()
            wire_segment.solve(signal_patterns.split())
            # Concatenate each digit in a string to get the actual value
            output_val_str = ''
            for output_value in output_values.split():
                num = wire_segment.decode(output_value)
                # Part 1 work
                unique_count += 1 if num in num_to_unique_num_segments else 0
                output_val_str += str(num)
            output_value_sum += int(output_val_str)

    return unique_count, output_value_sum


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
