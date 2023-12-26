#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
import itertools
# import matplotlib.pyplot as plt


test_inp = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def list_neighbors(self) -> list[Coord]:
        return [
            self + x
            for x in [
                Coord(0, 1),
                Coord(0, -1),
                Coord(1, 0),
                Coord(-1, 0),
            ]
        ]


def parse_inp(inp: str) -> tuple[set[Coord], set[Coord], Coord, int, int]:
    start_coord: Coord = Coord(0, 0)
    rocks: set[Coord] = set()
    garden_plots: set[Coord] = set()
    height = len(inp.splitlines())
    width = len(inp.splitlines()[0])
    for idy, line in enumerate(inp.splitlines()):
        for idx, char in enumerate(line):
            coord = Coord(idx, idy)
            match char:
                case ".":
                    garden_plots.add(coord)
                case "#":
                    rocks.add(coord)
                case "S":
                    print(f"S = {coord}")
                    start_coord = coord
                    garden_plots.add(coord)
    print(f"{height = } {width = }")
    return (garden_plots, rocks, start_coord, height, width)


def solve_part_1(inp: str, num_turns: int) -> int:
    garden_plots, rocks, start_coord, _, _ = parse_inp(inp)
    coords = set([start_coord])
    turn = 0
    while turn < num_turns:
        coord_acc = set()
        for coord in coords:
            for neighbor in coord.list_neighbors():
                if neighbor in garden_plots:
                    coord_acc.add(neighbor)
        coords = coord_acc
        turn += 1
        print(f"after {turn} turns = {len(coords)}")
    return len(coords)


def solve_part_2(inp: str) -> int:
    num_steps = 26_501_365
    garden_plots, rocks, start_coord, height, width = parse_inp(inp)

    # Start is in the middle:
    period: int = start_coord.x

    #                          #
    #                #        ###
    #        #      ###      #####
    #  # -> ### -> ##### -> #######
    #        #      ###      #####
    #                #        ###
    #                          #
    #
    #  1     5       13       25
    #
    # (1, 1), (2, 5), (3, 13), (4,25)
    # Jump increases by 4 each time
    # = 2n^2 -2n + 1
    coords = set([start_coord])
    turn = 0
    counts = []

    print(f"{(num_steps - 65) % 131 = }")

    while turn < 1250:
        coord_acc = set()
        for coord in coords:
            for neighbor in coord.list_neighbors():
                inf_grid_neighbor = Coord(neighbor.x % width, neighbor.y % height)

                if inf_grid_neighbor in garden_plots:
                    coord_acc.add(neighbor)
        coords = coord_acc
        turn += 1
        counts.append((turn, len(coords)))

    for x in counts:
        turn, num = x
        if turn == 65 or (turn - 65) % 131 == 0:
            print(f"{turn}: {num}")

    return 0


if __name__ == "__main__":
    assert solve_part_1(test_inp, 6) == 16
    inp = sys.argv[1]
    print(f"{solve_part_1(inp, 200) = }")
    # print(f"{solve_part_2(test_inp) = }")
    print(f"{solve_part_2(inp) = }")
