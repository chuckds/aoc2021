#!/bin/env python3
"""
Advent Of Code 2021 Day 4
"""

import sys
import time
import collections


class BingoBoard:
    def __init__(self, rows: list[list[int]]) -> None:
        self.size: int = len(rows)
        self.unmarked_numbers: dict[int, list[tuple[int, int]]] = collections.defaultdict(list)
        self.marked_rows: dict[int, int] = collections.defaultdict(int)
        self.marked_cols: dict[int, int] = collections.defaultdict(int)
        for row_i, row in enumerate(rows):
            for col_i, number in enumerate(row):
                # Assume it is possible for the same number to appear more than once
                self.unmarked_numbers[number].append((row_i, col_i))

    def mark_number(self, number: int) -> None:
        for row_i, col_i in self.unmarked_numbers.pop(number, []):
            self.marked_rows[row_i] += 1
            self.marked_cols[col_i] += 1

    def has_won(self) -> bool:
        return (any(marked_count == self.size for marked_count in self.marked_rows.values()) or
                any(marked_count == self.size for marked_count in self.marked_cols.values()))

    def sum_unmarked_get(self) -> int:
        return sum(number * len(indicies) for number, indicies in self.unmarked_numbers.items())

    @classmethod
    def from_lines(cls, lines: list[str]) -> BingoBoard:
        rows = []
        for line in lines:
            rows.append([int(val) for val in line.strip().split()])
        return cls(rows)


def parse_calls_and_boards(input_file: str) -> tuple[list[int], list[BingoBoard]]:
    bingo_boards: list[BingoBoard] = []

    with open(input_file) as f:
        calls = [int(val) for val in next(f).strip().split(',')]
        board_lines = []
        for line in f:
            line = line.strip()
            if line:
                board_lines.append(line)
            elif board_lines:
                bingo_boards.append(BingoBoard.from_lines(board_lines))
                board_lines = []
    if board_lines:
        bingo_boards.append(BingoBoard.from_lines(board_lines))
    return calls, bingo_boards


def p2(input_file: str) -> int:
    calls, bingo_boards = parse_calls_and_boards(input_file)

    for call in calls:
        for board in bingo_boards:
            board.mark_number(call)
        
        if len(bingo_boards) == 1 and bingo_boards[0].has_won():
            # Last board has won
            loser = bingo_boards[0]
            break

        # Get rid of the boards that have won
        bingo_boards = [b for b in bingo_boards if not b.has_won()]

    sum_unmarked = loser.sum_unmarked_get()

    print(f"{call=} {sum_unmarked=}")
    return call * sum_unmarked


def p1(input_file: str) -> int:
    calls, bingo_boards = parse_calls_and_boards(input_file)

    for call in calls:
        for board in bingo_boards:
            board.mark_number(call)
        winners = [b for b in bingo_boards if b.has_won()]
        if winners:
            break
    
    # What if there's more than one?
    sum_unmarked = winners[0].sum_unmarked_get()

    print(f"{call=} {sum_unmarked=}")
    return call * sum_unmarked


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))