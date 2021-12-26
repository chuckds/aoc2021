#!/bin/env python3
"""
Advent Of Code 2021 Day 25
"""

import sys
import time
import dataclasses


@dataclasses.dataclass
class SeaCumcumber:
    row: int
    col: int

    def can_move(self, grid: list[list[bool]], width: int, height: int) -> bool:
        return False

    def move(self, grid: list[list[bool]], width: int, height: int) -> None:
        pass


class EastSC(SeaCumcumber):
    def can_move(self, grid: list[list[bool]], width: int, _: int) -> bool:
        return not grid[self.row][(self.col + 1) % width]

    def move(self, grid: list[list[bool]], width: int, _: int) -> None:
        grid[self.row][self.col] = False
        self.col = (self.col + 1) % width
        grid[self.row][self.col] = True


class SouthSC(SeaCumcumber):
    def can_move(self, grid: list[list[bool]], _: int, height: int) -> bool:
        return not grid[(self.row + 1) % height][self.col]

    def move(self, grid: list[list[bool]], _: int, height: int) -> None:
        grid[self.row][self.col] = False
        self.row = (self.row + 1) % height
        grid[self.row][self.col] = True


def p1p2(input_file: str) -> tuple[int, int]:
    grid: list[list[bool]] = []
    east_sc: list[SeaCumcumber] = []
    south_sc: list[SeaCumcumber] = []
    with open(input_file) as f:
        for row_idx, line in enumerate(f):
            row = []
            for col_idx, char in enumerate(line.strip()):
                if char == '.':
                    row.append(False)
                else:
                    row.append(True)
                    if char == '>':
                        sc_list = east_sc
                        sc_type = EastSC
                    else:
                        sc_list = south_sc
                        sc_type = SouthSC  # type: ignore
                    sc_list.append(sc_type(row_idx, col_idx))
            if row:
                grid.append(row)

    width, height = len(grid[0]), len(grid)
    sc_moved = True
    generations = 0
    while sc_moved:
        sc_moved = False
        for sc_list in (east_sc, south_sc):
            sc_can_move = [sc for sc in sc_list if sc.can_move(grid, width, height)]
            sc_moved |= bool(sc_can_move)
            for sc in sc_can_move:
                sc.move(grid, width, height)
        generations += 1

    return (generations, 0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
