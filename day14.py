#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass

test_inp = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)


@dataclass
class Grid:
    width: int
    height: int
    moving_rocks: list[Coord]
    solid_rocks: set[Coord]


def parse_input(inp: str) -> Grid:
    solid_rocks = set()
    moving_rocks = []

    inp_lines = inp.splitlines()

    height = len(inp_lines)
    width = len(inp_lines[0])

    for y, line in enumerate(inp_lines):
        for x, char in enumerate(line):
            match char:
                case "O":
                    moving_rocks.append(Coord(x, y))
                case "#":
                    solid_rocks.add(Coord(x, y))
    return Grid(width, height, moving_rocks, solid_rocks)


def move_rocks(grid: Grid) -> bool:
    """Returns whether any rocks moved"""
    move_up_delta = Coord(0, -1)
    rock_has_moved = False

    max_y = max([co.y for co in grid.moving_rocks])
    max_x = max([co.x for co in grid.moving_rocks])

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            coord = Coord(x, y)
            if coord.y == 0 or coord not in grid.moving_rocks:
                continue
            shadow_rock = coord + move_up_delta
            if (
                shadow_rock not in grid.solid_rocks
                and shadow_rock not in grid.moving_rocks
            ):
                rock_has_moved = True
                for idx in range(len(grid.moving_rocks)):
                    if grid.moving_rocks[idx] == coord:
                        grid.moving_rocks[idx] = shadow_rock
    return rock_has_moved


def pretty_grid(g: Grid) -> None:
    for y in range(g.height):
        line_acc = ""
        for x in range(g.width):
            co = Coord(x, y)
            if co in g.solid_rocks:
                line_acc += "#"
            elif co in g.moving_rocks:
                line_acc += "O"
            else:
                line_acc += "."
        print(line_acc)


def solve_part_1(inp: str) -> int:
    grid = parse_input(inp)
    cont = True
    pretty_grid(grid)
    print()
    while cont:
        cont = move_rocks(grid)
    pretty_grid(grid)

    acc = 0

    for y in range(grid.height):
        for x in range(grid.width):
            co = Coord(x, y)
            if co in grid.moving_rocks:
                acc += abs(y - grid.height)

    return acc


def solve_part_2(inp: str) -> int:
    pass


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 136
    # assert solve_part_2(test_inp) ==
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
