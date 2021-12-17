#!/bin/env python3
"""
Advent Of Code 2021 Day 16
"""

import sys
import math
import time
import dataclasses
from typing import Callable, ClassVar


@dataclasses.dataclass
class Packet:
    binary_string: str
    read_posn: int = 0

    type_map: ClassVar[dict[int, Callable[[list[int]], int]]] = {
        0: sum,
        1: math.prod,
        2: min,
        3: max,
        4: lambda pak_vals: pak_vals[0],
        5: lambda pak_vals: 1 if pak_vals[0] > pak_vals[1] else 0,
        6: lambda pak_vals: 1 if pak_vals[0] < pak_vals[1] else 0,
        7: lambda pak_vals: 1 if pak_vals[0] == pak_vals[1] else 0,
    }

    def read_str(self, len: int) -> str:
        result = self.binary_string[self.read_posn:self.read_posn + len]
        self.read_posn += len
        return result

    def read_int(self, len: int) -> int:
        return int(self.read_str(len), 2)


def get_packet_info(p: Packet) -> tuple[int, int]:
    version = p.read_int(3)
    pak_type = p.read_int(3)
    if pak_type == 4:
        # Literal number
        num_bin_string = ""
        last = False
        while not last:
            num_group = p.read_str(5)
            num_bin_string += num_group[1:]
            last = num_group[0] == "0"
        values = [int(num_bin_string, 2)]
    else:
        # Subpackets
        length_type_id = p.read_int(1)
        values = []
        if length_type_id == 0:
            len_sub_packets = p.read_int(15)
            sub_packets = Packet(p.read_str(len_sub_packets))
            while sub_packets.read_posn < len_sub_packets:
                subpack_version, subpack_value = get_packet_info(sub_packets)
                version += subpack_version
                values.append(subpack_value)
        else:
            num_sub_packets = p.read_int(11)
            for _ in range(num_sub_packets):
                subpack_version, subpack_value = get_packet_info(p)
                values.append(subpack_value)
                version += subpack_version

    return (version, Packet.type_map[pak_type](values))


def p1p2(input_file: str) -> tuple[list[int], list[int]]:
    version_sums: list[int] = []
    values: list[int] = []
    with open(input_file) as f:
        for line in f:
            hex_string = line.strip()
            bin_string = "".join([f"{int(char, 16):04b}"
                                  for char in hex_string])
            version_sum, value = get_packet_info(Packet(bin_string))
            version_sums.append(version_sum)
            values.append(value)
    return (version_sums, values)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
