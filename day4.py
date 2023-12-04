#!/usr/bin/env python3

import sys
import re

test_inp = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

def solve_part_1(inp: str) -> int:
    nums_regex = re.compile(r"\d+")
    acc = 0
    for card_number, line in enumerate(inp.splitlines(), start=1):
        _, rest = line.split(":")
        lhs, rhs = rest.split("|")
        winning_nums = nums_regex.findall(lhs)
        scratch_nums = nums_regex.findall(rhs)
        to_add = 0
        for scratch in scratch_nums:
            if scratch in winning_nums:
                to_add = 1 if to_add == 0 else to_add * 2
        acc += to_add
    print(acc)
    return acc

def solve_part_2(inp: str) -> int:
    nums_regex = re.compile(r"\d+")
    count_dict: dict[int, int] = {
        x+1:1 for x in range(len(inp.splitlines())) 
    }
    for card_number, line in enumerate(inp.splitlines(), start=1):
        _, rest = line.split(":")
        lhs, rhs = rest.split("|")
        winning_nums = nums_regex.findall(lhs)
        scratch_nums = nums_regex.findall(rhs)
        win_count = 0
        for scratch in scratch_nums:
            if scratch in winning_nums:
                win_count += 1
        for x in range(1, win_count + 1):
            count_dict[x+ card_number] += count_dict[card_number]
    return sum(count_dict.values())

if __name__ == "__main__":
    inp = sys.argv[1]
    assert solve_part_1(test_inp) == 13
    assert solve_part_2(test_inp) == 30
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")