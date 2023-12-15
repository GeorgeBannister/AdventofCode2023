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
    moving_rocks: set[Coord]
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
    return Grid(width, height, set(moving_rocks), solid_rocks)


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
                grid.moving_rocks.remove(coord)
                grid.moving_rocks.add(shadow_rock)

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


def move_rocks_part_2(grid: Grid) -> int:
    cycle = 0
    d = {}
    target_cycle = 1_000_000_000
    have_jumped = False

    while cycle < target_cycle:
        memo_item = frozenset(grid.moving_rocks)

        if not have_jumped and memo_item in d:
            have_jumped = True
            print(f"Can skip {cycle} {d[memo_item]}")
            jump_size = cycle - d[memo_item]
            print(f"{jump_size = }")
            turns_to_fin = target_cycle - cycle
            num_jumps = turns_to_fin // jump_size
            print(f"{num_jumps = }")
            cycle += num_jumps * jump_size

        d[memo_item] = cycle

        move_delta = Coord(0, -1)

        have_moved = True
        while have_moved:
            have_moved = False

            for y in range(grid.height):
                for x in range(grid.width):
                    coord = Coord(x, y)
                    if coord.y == 0 or coord not in grid.moving_rocks:
                        continue
                    shadow_rock = coord + move_delta
                    if (
                        shadow_rock not in grid.solid_rocks
                        and shadow_rock not in grid.moving_rocks
                    ):
                        have_moved = True
                        grid.moving_rocks.remove(coord)
                        grid.moving_rocks.add(shadow_rock)

        move_delta = Coord(-1, 0)

        have_moved = True
        while have_moved:
            have_moved = False

            for x in range(grid.width):
                for y in range(grid.height):
                    coord = Coord(x, y)
                    if coord.x == 0 or coord not in grid.moving_rocks:
                        continue
                    shadow_rock = coord + move_delta
                    if (
                        shadow_rock not in grid.solid_rocks
                        and shadow_rock not in grid.moving_rocks
                    ):
                        have_moved = True
                        grid.moving_rocks.remove(coord)
                        grid.moving_rocks.add(shadow_rock)

        move_delta = Coord(0, 1)

        have_moved = True
        while have_moved:
            have_moved = False

            for y in reversed(range(grid.height)):
                for x in range(grid.width):
                    coord = Coord(x, y)
                    if coord.y == grid.height - 1 or coord not in grid.moving_rocks:
                        continue
                    shadow_rock = coord + move_delta
                    if (
                        shadow_rock not in grid.solid_rocks
                        and shadow_rock not in grid.moving_rocks
                    ):
                        have_moved = True
                        grid.moving_rocks.remove(coord)
                        grid.moving_rocks.add(shadow_rock)

        move_delta = Coord(1, 0)

        have_moved = True
        while have_moved:
            have_moved = False

            for x in reversed(range(grid.width)):
                for y in range(grid.height):
                    coord = Coord(x, y)
                    if coord.x == grid.width - 1 or coord not in grid.moving_rocks:
                        continue
                    shadow_rock = coord + move_delta
                    if (
                        shadow_rock not in grid.solid_rocks
                        and shadow_rock not in grid.moving_rocks
                    ):
                        have_moved = True
                        grid.moving_rocks.remove(coord)
                        grid.moving_rocks.add(shadow_rock)

        print(cycle)

        cycle += 1
    acc = 0
    for y in range(grid.height):
        for x in range(grid.width):
            co = Coord(x, y)
            if co in grid.moving_rocks:
                acc += abs(y - grid.height)
    print(f"{acc = }")
    pretty_grid(grid)
    return acc


def solve_part_2(inp: str) -> int:
    grid = parse_input(inp)
    return move_rocks_part_2(grid)


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 136
    assert solve_part_2(test_inp) == 64
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
