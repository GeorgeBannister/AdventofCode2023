#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum
import itertools

test_inp = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


class Dir(Enum):
    up = 0
    down = 1
    left = 2
    right = 3


dir_map = {
    "U": Dir.up,
    "D": Dir.down,
    "L": Dir.left,
    "R": Dir.right,
}


@dataclass(frozen=True)
class Instruction:
    direction: Dir.up | Dir.down | Dir.left | Dir.right
    length: int


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Coord(self.x * other, self.y * other)


delta_map = {
    Dir.up: Coord(0, 1),
    Dir.down: Coord(0, -1),
    Dir.left: Coord(-1, 0),
    Dir.right: Coord(1, 0),
}


def shoelace(coords: list[Coord]) -> int:
    coords.append(coords[0])
    acc = 0
    for pair in itertools.pairwise(coords):
        co1, co2 = pair
        acc += co1.x * co2.y - co1.y * co2.x
    return abs(acc // 2)


def count_hole_size(instructions: list[Instruction]) -> int:
    """
    Blown up 3x.
    The shoelace area (from X to X) doesn't capture the full area of the squares it's measured from the middle of the squares.
    Each square on a perimeter line needs plus 1/2
    Each inner corner square is worth 1/4
    Each outer corner square is worth 3/4

    As this is a loop:
        There is a matching outer corner for each inner corner. (These balance out in area to 1/2 each)
        There are 4 extra outer corners. (an extra 1 area on top of the default 1/2)

    This adds up to the total area being:
        "shoelace area + perimeter area // 2 + 1"


    #####################
    #X-----------------X#
    #|#################|#
    #|#...............#|#
    #|#...............#|#
    #|#...............#|#
    #|#######.........#|#
    #X-----X#.........#|#
    #######|#.........#|#
    ......#|#.........#|#
    ......#|#.........#|#
    ......#|#.........#|#
    ......#|#.........#|#
    ......#|#.........#|#
    ......#|#.........#|#
    #######|#...#######|#
    #X-----X#...#X-----X#
    #|#######...#|#######
    #|#.........#|#......
    #|#.........#|#......
    #|#.........#|#......
    #|####......#|#######
    #X--X#......#X-----X#
    ####|#......#######|#
    ...#|#............#|#
    ...#|#............#|#
    ...#|#............#|#
    ...#|##############|#
    ...#X--------------X#
    ...##################
    """
    curr_coord = Coord(0, 0)
    coords = [curr_coord]
    perim_acc = 1
    for ins in instructions:
        delta = delta_map[ins.direction]
        curr_coord = curr_coord + (delta * ins.length)
        if curr_coord in coords:
            perim_acc -= 1
        coords.append(curr_coord)
        perim_acc += ins.length
    return shoelace(coords) + (perim_acc // 2 + 1)


def parse_input(inp: str) -> list[Instruction]:
    acc = []
    for line in inp.splitlines():
        d, l, _ = line.split()
        acc.append(Instruction(dir_map[d], int(l)))
    return acc


def parse_input_2(inp: str) -> list[Instruction]:
    acc = []
    for line in inp.splitlines():
        _, _, hexa = line.split()
        hexa = hexa.replace("#", "").replace(")", "").replace("(", "")
        direction = (
            Dir.right
            if hexa[-1] == "0"
            else Dir.down
            if hexa[-1] == "1"
            else Dir.left
            if hexa[-1] == "2"
            else Dir.up
        )
        num = int(hexa[:5], 16)
        acc.append(Instruction(direction, num))
    return acc


def solve_part_1(inp: str) -> int:
    instructions = parse_input(inp)
    return count_hole_size(instructions)


def solve_part_2(inp: str) -> int:
    instructions = parse_input_2(inp)
    return count_hole_size(instructions)


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 62
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    assert solve_part_2(test_inp) == 952408144115
    print(f"{solve_part_2(inp) = }")
