#!/bin/env python3
"""
Advent Of Code 2021 Day 24
"""

import sys
import time

from typing import Optional


x_adds = [12, 12, 15, -8, -4, 15, 14, 14, -13, -3, -7, 10, -6, -8]
y_adds = [ 1,  1, 16,  5,  9,  3,  2, 15,   5, 11,  7,  1, 10,  3]


def process_input(digit: int, z_val: int, input_num: int) -> Optional[int]:
    x = (z_val % 26) + x_adds[input_num]
    if x_adds[input_num] < 0:
        z_val = int(z_val / 26)
        if x != digit:
            # If x_adds is negative then it is possible to get a digit
            # that equals x, further to get z back to zero by the end we need
            # to take every opportuity to skip z being multiplied by 26 i.e
            # when possible digit must equal x. Since it doesn't signal that
            # this digit is a bad choice
            return None
    if x != digit:
        z_val = 26 * z_val + digit + y_adds[input_num]

    return z_val


def find_valid_model(num_digits: int, smallest: bool = False,
                     digit_idx: int = 0, z_val: int = 0) -> Optional[str]:
    res = None
    if digit_idx == num_digits:
        if z_val == 0:
            res = ""
    else:
        val_range = range(1, 10) if smallest else range(9, 0, -1)
        for digit_val in val_range:
            new_z = process_input(digit_val, z_val, digit_idx)
            if new_z is not None:
                res = find_valid_model(num_digits, smallest, digit_idx + 1, new_z)
                if res is not None:
                    res = str(digit_val) + res
                    break
    return res


def p1p2(input_file: str) -> tuple[int, int]:
    return (int(find_valid_model(14)), int(find_valid_model(14, True)))  # type: ignore


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
