#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
from itertools import combinations

test_inp = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)


def pretty_print_galaxy_map(galaxy_map: dict[Coord, int]) -> None:
    max_x = 0
    max_y = 0
    for key in galaxy_map:
        max_x = max(max_x, key.x)
        max_y = max(max_y, key.y)

    for y in range(max_y + 1):
        line_str = ""
        for x in range(max_x + 1):
            coord = Coord(x, y)
            if coord in galaxy_map:
                line_str += "#"
            else:
                line_str += "."
        print(line_str)


def parse_input(inp: str, part_2=False) -> dict[Coord, int]:
    galaxy_map = {}

    num_x = len(inp.splitlines()[0])
    num_y = len(inp.splitlines())

    x_has_galaxy_map = {x: False for x in range(num_x)}
    y_has_galaxy_map = {y: False for y in range(num_y)}

    for idy, line in enumerate(inp.splitlines()):
        for idx, val in enumerate(line):
            if val == "#":
                x_has_galaxy_map[idx] = True
                y_has_galaxy_map[idy] = True

    curr_gal_num = 0

    for idy, line in enumerate(inp.splitlines()):
        for idx, val in enumerate(line):
            x_delta = len([x for x in range(idx) if not x_has_galaxy_map[x]])
            y_delta = len([y for y in range(idy) if not y_has_galaxy_map[y]])

            if part_2:
                x_delta *= 999_999
                y_delta *= 999_999

            if val == "#":
                galaxy_map[Coord(idx + x_delta, idy + y_delta)] = curr_gal_num
                curr_gal_num += 1

    return galaxy_map


def get_manhattan_distance_sum(galaxy_map: dict[Coord, int]) -> int:
    acc = 0
    for pair in combinations(galaxy_map, 2):
        coord_1, coord_2 = pair
        acc += abs(coord_1.x - coord_2.x)
        acc += abs(coord_1.y - coord_2.y)
    return acc


def solve_part_1(inp: str) -> int:
    galaxy_map = parse_input(inp)
    return get_manhattan_distance_sum(galaxy_map)


def solve_part_2(inp: str) -> int:
    galaxy_map = parse_input(inp, part_2=True)
    return get_manhattan_distance_sum(galaxy_map)


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 374
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
