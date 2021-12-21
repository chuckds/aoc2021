#!/bin/env python3
"""
Advent Of Code 2021 Day 21
"""
from __future__ import annotations

import sys
import time
import collections
import dataclasses

from typing import NamedTuple, Iterable


def three_dice() -> Iterable[int]:
    for die_roll1 in (1, 2, 3):
        for die_roll2 in (1, 2, 3):
            for die_roll3 in (1, 2, 3):
                yield die_roll1 + die_roll2 + die_roll3


class Play(NamedTuple):
    position: int
    score: int = 0

    def with_roll(self, dice_roll: int) -> Play:
        new_pos = ((self.position - 1 + dice_roll) % 10) + 1
        return Play(new_pos, self.score + new_pos)


def p2(input_file: str) -> int:
    with open(input_file) as f:
        players = tuple([Play(int(line.strip().split()[-1])) for line in f])

    game_state_counts = collections.defaultdict(int)
    game_state_counts[(players[0], players[1]), 0] = 1
    p1_wins = 0
    dice_sums = collections.Counter(three_dice())
    while game_state_counts:
        next_round: collections.defaultdict[tuple[tuple[Play, Play], int], int] = collections.defaultdict(int)
        for (players, p1_index), count in game_state_counts.items():
            for dice_roll, dice_count in dice_sums.items():
                new_player = players[0].with_roll(dice_roll)
                if new_player.score >= 21:
                    if p1_index == 0:
                        p1_wins += count * dice_count
                else:
                    # Didn't win keep on playing
                    # Swap the players around keeping track of which one is p1
                    next_round[((players[1], new_player), int(not p1_index))] += count * dice_count
        game_state_counts = next_round

    return p1_wins


@dataclasses.dataclass
class Player:
    position: int
    score: int = 0

    def with_roll(self, dice_roll: int) -> None:
        self.position = ((self.position - 1 + dice_roll) % 10) + 1
        self.score += self.position


def p1(input_file: str) -> int:
    with open(input_file) as f:
        players = [Player(int(line.strip().split()[-1])) for line in f]

    die = iter(range(1, 1001))
    while all(player.score < 1000 for player in players):
        for player in players:
            player.with_roll(next(die) + next(die) + next(die))
            if player.score >= 1000:
                break

    loser_score = [player for player in players if player.score < 1000][0].score
    return loser_score * (next(die) - 1)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
