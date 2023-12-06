#!/usr/bin/env python3

import sys
import re
from pprint import pprint
from functools import reduce

test_inp = """Time:      7  15   30
Distance:  9  40  200"""

num_regex = re.compile(r"\d+")


def solve_part_1(inp: str) -> int:
    lines = inp.splitlines()
    times = [int(x) for x in num_regex.findall(lines[0])]
    distances = [int(x) for x in num_regex.findall(lines[1])]
    races = [(times[x], distances[x]) for x in range(0, len(times))]
    acc = []
    for race in races:
        race_win_count = 0
        race_time, race_dist = race
        for hold_time in range(0, race_time):
            if hold_time * (race_time - hold_time) > race_dist:
                race_win_count += 1
        acc.append(race_win_count)
    return reduce(lambda x, y: x * y, acc)


def solve_part_2(inp: str) -> int:
    lines = inp.splitlines()
    time = int(reduce(lambda x, y: f"{x}{y}", num_regex.findall(lines[0])))
    distance = int(reduce(lambda x, y: f"{x}{y}", num_regex.findall(lines[1])))
    race = (time, distance)
    acc = 0
    race_time, race_dist = race
    have_started_winning = False
    for hold_time in range(0, race_time):
        if hold_time * (race_time - hold_time) > race_dist:
            have_started_winning = True
            acc += 1
        else:
            if have_started_winning:
                break
    return acc


if __name__ == "__main__":
    inp = sys.argv[1]
    assert solve_part_1(test_inp) == 288
    print(f"{solve_part_1(inp) = }")
    assert solve_part_2(test_inp) == 71503
    print(f"{solve_part_2(inp) = }")
