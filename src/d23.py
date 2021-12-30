#!/bin/env python3
"""
Advent Of Code 2021 Day 23
"""
from __future__ import annotations

import sys
import time

from typing import NamedTuple, Iterable, Optional


Hallway = tuple[str, str, str, str, str, str, str]

room_map = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}


distances = [  # hallway then room
    [3, 5, 7, 9],
    [2, 4, 6, 8],
    [2, 2, 4, 6],
    [4, 2, 2, 4],
    [6, 4, 2, 2],
    [8, 6, 4, 2],
    [9, 7, 5, 3],
]


class AmphipodState(NamedTuple):
    hallway: Hallway
    rooms: tuple[tuple[str, str], tuple[str, str], tuple[str, str], tuple[str, str]]

    def reachable(self, hallway_posn: int, room: int) -> bool:
        if hallway_posn < room + 2:
            # Moving to the right to get there (hallway -> room)
            return all(self.hallway[idx] == '.' for idx in range(hallway_posn + 1, room + 2))
        else:
            # Moving to the left to get there (hallway -> room)
            return all(self.hallway[idx] == '.' for idx in range(room + 2, hallway_posn))

    def moves(self) -> Iterable[tuple[AmphipodState, int]]:
        for hallway_idx, amphipod in enumerate(self.hallway):
            if amphipod != '.':
                # These can only move into the correct room if that room has a
                # space
                amps_room = room_map[amphipod]
                if ('.' == self.rooms[amps_room][0] and self.rooms[amps_room][1] in ('.', amphipod) and
                    self.reachable(hallway_idx, amps_room)):
                    new_hallway = self.hallway[:hallway_idx] + ('.',) + self.hallway[hallway_idx + 1:]
                    distance = distances[hallway_idx][amps_room]
                    if self.rooms[amps_room][1] == '.':
                        new_room = ('.', amphipod)
                        distance += 1
                    else:
                        new_room = (amphipod, self.rooms[amps_room][1])
                    new_rooms = self.rooms[:amps_room] + (new_room,) + self.rooms[amps_room + 1:]
                    yield (AmphipodState(new_hallway, new_rooms), distance * (10 ** amps_room))  # type: ignore

        # For each room see which amphipods can move out
        for room_idx, amphipods_in_room in enumerate(self.rooms):
            for char_idx, amphipod in enumerate(amphipods_in_room):
                if amphipod != '.':
                    amps_room = room_map[amphipod]
                    if amps_room != room_idx or (char_idx == 0 and room_map[amphipods_in_room[1]] != room_idx):
                        # There's an amphipod in this room that shouldnt be here or
                        # it should be here but its blocking one in that shouldn't so move it
                        for hallway_idx, hallway_state in enumerate(self.hallway):
                            if hallway_state == '.' and self.reachable(hallway_idx, room_idx):
                                new_hallway = self.hallway[:hallway_idx] + (amphipod,) + self.hallway[hallway_idx + 1:]
                                distance = distances[hallway_idx][room_idx]
                                if char_idx == 1:  # Bottom amphipod
                                    new_room = ('.', '.')
                                    distance += 1
                                else:
                                    new_room = ('.', amphipods_in_room[1])
                                new_rooms = self.rooms[:room_idx] + (new_room,) + self.rooms[room_idx + 1:]
                                yield (AmphipodState(new_hallway, new_rooms), distance * (10 ** room_map[amphipod]))  # type: ignore
                    # Only the top amphipod can move so stop as soon as anyone
                    # has
                    break

    def __str__(self) -> str:
        return ("#" * 13 + f"\n#{self.hallway[0]}{self.hallway[1]}.{self.hallway[2]}.{self.hallway[3]}.{self.hallway[4]}.{self.hallway[5]}{self.hallway[6]}#\n" +
                f"###{self.rooms[0][0]}#{self.rooms[1][0]}#{self.rooms[2][0]}#{self.rooms[3][0]}###\n" +
                f"  #{self.rooms[0][1]}#{self.rooms[1][1]}#{self.rooms[2][1]}#{self.rooms[3][1]}#\n  " + "#" * 9 + "  ")


def p1p2(input_file: str) -> tuple[int, int]:
    with open(input_file) as f:
        rooms = []
        for line in f:
            amphipods = [char for char in line.strip() if char not in ('.', '#')]
            if amphipods:
                rooms.append(amphipods)

    init_state = AmphipodState(tuple('.' * 7), tuple(zip(*rooms)))  # type: ignore
    destination_state = AmphipodState(tuple('.' * 7), tuple(zip(tuple('ABCD'), tuple('ABCD'))))  # type: ignore
    reachable: dict[AmphipodState, tuple[int, Optional[AmphipodState]]] = {init_state: (0, None)}
    lowest_cost_known: dict[AmphipodState, tuple[int, Optional[AmphipodState]]] = {}
    while reachable:
        ap_state, (lowest_cost_so_far, previous_state) = sorted(reachable.items(), key=lambda x: x[1][0])[0]
        del reachable[ap_state]
        lowest_cost_known[ap_state] = (lowest_cost_so_far, previous_state)
        if ap_state == destination_state:
            break
        for new_state, additional_cost in ap_state.moves():
            if new_state not in lowest_cost_known:
                new_cost_to_state = lowest_cost_so_far + additional_cost
                cost_to_state_so_far, _ = reachable.get(new_state, (None, None))
                if (cost_to_state_so_far is None or
                    new_cost_to_state < cost_to_state_so_far):
                    reachable[new_state] = (new_cost_to_state, ap_state)

    path = [(destination_state, 0)]
    next_state = destination_state
    while next_state:
        lowest_cost_so_far, next_state = lowest_cost_known[next_state]  # type: ignore
        path.insert(0, (next_state, lowest_cost_so_far))
    for state, cost in path:
        print(f"{state}\n{cost}")

    return (lowest_cost_known[destination_state][0], 0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
