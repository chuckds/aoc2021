#!/bin/env python3
"""
Advent Of Code 2021 Day 20
"""

import sys
import time


char_to_bit = {'.': '0', '#': '1'}


def pixel_to_int(row: int, col: int, size: int, lines: list[str], default_char: str) -> int:
    bit_string = ""
    for vert_delta in (-1, 0, 1):
        for horiz_delta in (-1, 0, 1):
            new_row = row + vert_delta
            new_col = col + horiz_delta
            if (new_row >= 0 and new_col >= 0 and
                new_row < size and new_col < size):
                # get value from grid
                bit_string += char_to_bit[lines[new_row][new_col]]
            else:
                # Default char
                bit_string += char_to_bit[default_char]
    return int(bit_string, 2)


def enhance(image: list[str], ei_algo: str, default_char: str) -> list[str]:
    enhanced = []
    size = len(image[0])
    for row_num in range(size):
        new_row = ""
        for char_num in range(size):
            ei_algo_idx = pixel_to_int(row_num, char_num, size, image, default_char)
            new_row += ei_algo[ei_algo_idx]
        enhanced.append(new_row)
    return enhanced


def pad(image: list[str], char: str) -> list[str]:
    width = len(image[0]) + 2
    result = [char * width]
    result.extend([char + line + char for line in image])
    result.append(char * width)
    return result


def p1p2(input_file: str) -> tuple[int, int]:
    with open(input_file) as f:
        ei_algo = next(f).strip()
        assert len(ei_algo) == 512
        next(f)  # Blank line
        image = [line.strip() for line in f]

    default_char = "."
    for step in range(50):
        image = enhance(pad(image, default_char), ei_algo, default_char)
        if default_char == '.':
            if ei_algo[0] == '#':
                # Now the infiite expanse will have flipped to '#'
                default_char = '#'
        else:
            if ei_algo[-1] == '.':
                # Now the infiite expanse will have flipped to '.'
                default_char = '.'
        if step == 1:
            p1_lit = sum(line.count('#') for line in image)

    return (p1_lit, sum(line.count('#') for line in image))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
