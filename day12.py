#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from pprint import pprint
from itertools import combinations
from functools import cache

test_inp = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

pos_int_reg = re.compile(r"\d+")
contiguous_broken_reg = re.compile(r"#+")
mario_reg = re.compile(r"[?]")


@dataclass(frozen = True)
class Row:
    springs: str
    groups: tuple[int]


def count_valid(row: Row) -> int:
    acc = 0
    qidxs = []

    num_extra_broken_springs = sum(row.groups) - row.springs.count("#")

    for match in mario_reg.finditer(row.springs):
        qidxs.append(match.start())

    for combination in combinations(qidxs, num_extra_broken_springs):
        if row_is_valid_fast(row.springs, row.groups, frozenset(combination)):
            acc += 1
    return acc

mask_num = ord("#")

@cache
def row_is_valid_fast(lhs: str, rhs: tuple, combination: frozenset) -> bool:
    new_springs = bytearray(lhs, "ascii")
    for i in combination:
        new_new = new_springs
        new_new[i] = mask_num
    lens = tuple(len(match.group(0)) for match in contiguous_broken_reg.finditer(new_new.decode("ascii"))) 
    return lens == rhs

@cache
def row_is_valid(row: Row) -> bool:
    lens = tuple(len(match.group(0)) for match in contiguous_broken_reg.finditer(row.springs)) 
    return lens == row.groups


def solve_part_1(inp: str) -> int:
    rows = []
    acc = 0
    for line in inp.splitlines():
        lhs, rhs = line.split(" ")
        ints = [int(x) for x in pos_int_reg.findall(rhs)]
        rows.append(Row(lhs, tuple(ints)))
    
    for row in rows:
        acc += count_valid(row)
    return acc


def solve_part_2(inp: str) -> int:
    rows = []
    acc = 0
    for line in inp.splitlines():
        lhs, rhs = line.split(" ")
        ints = [int(x) for x in pos_int_reg.findall(rhs)]
        new_ints = tuple([*ints, *ints, *ints, *ints, *ints])

        new_lhs = f"{lhs}?{lhs}?{lhs}?{lhs}?{lhs}"

        rows.append(Row(new_lhs, new_ints))
    
    for row in rows:
        print(f"{row = }")
        acc += count_valid(row)
    return acc


if __name__ == "__main__":
    assert row_is_valid(Row("#.#.###", (1, 1, 3)))
    assert not row_is_valid(Row("##..###", (1, 1, 3)))

    assert solve_part_1(test_inp) == 21
    assert solve_part_2(test_inp) == 525152
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
