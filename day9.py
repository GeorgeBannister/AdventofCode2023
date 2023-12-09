#!/usr/bin/env python3

import sys
import re
from itertools import pairwise

test_inp = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

ints_regex = re.compile(r"[\d-]+")


def solve_part_1(inp: str) -> int:
    acc_score = 0
    for line in inp.splitlines():
        ints: list[int] = [int(x) for x in ints_regex.findall(line)]
        seqs: list[list[int]] = [ints]
        while not all(x == 0 for x in seqs[-1]):
            seqs.append([pair[1] - pair[0] for pair in pairwise(seqs[-1])])
        seqs[-1].append(0)
        for idx in range(len(seqs) - 2, -1, -1):
            seqs[idx].append(seqs[idx][-1] + seqs[idx + 1][-1])
        acc_score += seqs[0][-1]
    return acc_score


def solve_part_2(inp: str) -> int:
    acc_score = 0
    for line in inp.splitlines():
        ints: list[int] = [int(x) for x in ints_regex.findall(line)]
        ints.reverse()
        seqs: list[list[int]] = [ints]
        while not all(x == 0 for x in seqs[-1]):
            seqs.append([pair[1] - pair[0] for pair in pairwise(seqs[-1])])
        seqs[-1].append(0)
        for idx in range(len(seqs) - 2, -1, -1):
            seqs[idx].append(seqs[idx][-1] + seqs[idx + 1][-1])
        acc_score += seqs[0][-1]
    return acc_score


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 114
    assert solve_part_2(test_inp) == 2
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
