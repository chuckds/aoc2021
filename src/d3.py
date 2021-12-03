#!/bin/env python3
"""
Advent Of Code 2021 Day 3
"""

import sys
import time
import collections


def p2_find_val(bin_str_list, most_pop):
    for bit_i in range(1, len(bin_str_list[0])):
        by_bit_value = partition_by_char(bin_str_list, bit_i)
        if len(by_bit_value['0']) > len(by_bit_value['1']):
            bin_str_list = by_bit_value['0'] if most_pop else by_bit_value['1']
        else:
            bin_str_list = by_bit_value['1'] if most_pop else by_bit_value['0']
        if len(bin_str_list) == 1:
            return bin_str_list[0]


def partition_by_char(to_partition, char_i):
    by_char = collections.defaultdict(list)
    for string in to_partition:
        by_char[string[char_i]].append(string.strip())
    return by_char


def p2(input_file):
    # Split the input into lists depending on what the line starts with
    with open(input_file) as f:
        by_bit_value = partition_by_char(f, 0)

    # Assign the lists to oxygen or co2 based on populatarity
    if len(by_bit_value['0']) > len(by_bit_value['1']):
        oxygen_nums = by_bit_value['0']
        co2_nums = by_bit_value['1']
    else:
        oxygen_nums = by_bit_value['1']
        co2_nums = by_bit_value['0']
    
    # From now on oxygen and co2 are independent
    oxygen = int(p2_find_val(oxygen_nums, True), 2)
    co2 = int(p2_find_val(co2_nums, False), 2)

    print(f"{oxygen=} {co2=}")
    return oxygen * co2


def p1(input_file):
    counts = None

    with open(input_file) as f:
        for line in f:
            if counts is None:
                counts = [0] * len(line.strip())
            for i, bit in enumerate(line.strip()):
                counts[i] += 1 if int(bit) else -1

    gamma = int(''.join(['1' if count > 0 else '0' for count in counts]), 2)
    epsilon = int(''.join(['0' if count > 0 else '1' for count in counts]), 2)

    print(f"{gamma=} {epsilon=}")
    return gamma * epsilon


def main(cli_args):
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start}s")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))