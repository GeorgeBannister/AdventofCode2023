#!/usr/bin/env python3
import sys
from dataclasses import dataclass
import re

test_inp = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592..206
......755.
...$.*....
.664.598.."""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other) -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Num:
    value: int
    coords: frozenset[Coord]

    def is_adjacent_to_symbol(self, symbol_list: set[Coord]) -> bool:
        for coord in self.coords:
            for adj_delta in (
                Coord(-1, -1),
                Coord(-1, 0),
                Coord(-1, 1),
                Coord(0, -1),
                Coord(0, 1),
                Coord(1, -1),
                Coord(1, 0),
                Coord(1, 1),
            ):
                new_coord = coord + adj_delta
                if new_coord in symbol_list:
                    return True
        return False


def pretty_print_grid(grid: str, nums: list[Num], symbols: set[Coord]) -> None:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    RESET = "\033[0m"
    for y, line in enumerate(grid.splitlines()):
        for x, char in enumerate(line):
            coord = Coord(x, y)
            if any(coord in num.coords for num in nums):
                print(f"{GREEN}{char}{RESET}", end="")
                if coord in symbols:
                    raise RecursionError("aaa")
            elif coord in symbols:
                print(f"{RED}{char}{RESET}", end="")
            else:
                print(char, end="")
        print("")


def solve_part_1(inp: str) -> int:
    num_regex = re.compile(r"\d+", re.ASCII)
    non_symbol_chars = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}
    symbols: set[Coord] = set()
    nums: list[Num] = []
    for y, line in enumerate(inp.split("\n")):
        matches = num_regex.finditer(line)
        for match in matches:
            nums.append(
                Num(
                    int(match.group(0)),
                    frozenset(
                        {Coord(idx, y) for idx in range(match.start(0), match.end(0))}
                    ),
                )
            )

        for x, char in enumerate(line):
            if char not in non_symbol_chars:
                symbols.add(Coord(x, y))

    to_ret = 0
    for num in nums:
        if num.is_adjacent_to_symbol(symbols):
            to_ret += num.value
    return to_ret


def gear_to_num(gear: Coord, nums: list[Num]) -> int:
    gear_set = set([gear])
    if len([num for num in nums if num.is_adjacent_to_symbol(gear_set)]) != 2:
        return 0
    acc = 1
    for num in nums:
        if num.is_adjacent_to_symbol(gear_set):
            acc *= num.value
    return acc


def solve_part_2(inp: str) -> int:
    num_regex = re.compile(r"\d+", re.ASCII)
    gears: set[Coord] = set()
    nums: list[Num] = []
    for y, line in enumerate(inp.split("\n")):
        matches = num_regex.finditer(line)
        for match in matches:
            nums.append(
                Num(
                    int(match.group(0)),
                    frozenset(
                        {Coord(idx, y) for idx in range(match.start(0), match.end(0))}
                    ),
                )
            )

        for x, char in enumerate(line):
            if char == "*":
                gears.add(Coord(x, y))

    to_ret = 0
    for gear in gears:
        to_ret += gear_to_num(gear, nums)
    return to_ret


if __name__ == "__main__":
    inp = sys.argv[1]
    assert solve_part_1(test_inp) == 4361
    assert solve_part_2(test_inp) == 467835
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
