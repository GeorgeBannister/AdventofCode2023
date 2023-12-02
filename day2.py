#!/usr/bin/env python3
import sys
import re


def solve_part_1(inp: str) -> int:
    acc = 0
    red_reg = re.compile(r".*\s(\d+) red.*")
    green_reg = re.compile(r".*\s(\d+) green.*")
    blue_reg = re.compile(r".*\s(\d+) blue.*")
    for line in inp.splitlines():
        game_s, rest = line.split(":")
        game = int(game_s.replace("Game ", ""))
        sub_games = rest.split(";")
        game_is_valid = True
        for sub in sub_games:
            red_match = red_reg.match(sub)
            red_cnt = int(red_match.group(1)) if red_match else 0
            green_match = green_reg.match(sub)
            green_cnt = int(green_match.group(1)) if green_match else 0
            blue_match = blue_reg.match(sub)
            blue_cnt = int(blue_match.group(1)) if blue_match else 0
            if red_cnt > 12 or green_cnt > 13 or blue_cnt > 14:
                game_is_valid = False
        if game_is_valid:
            acc += game
    return acc


def solve_part_2(inp: str) -> int:
    acc = 0
    red_reg = re.compile(r".*\s(\d+) red.*")
    green_reg = re.compile(r".*\s(\d+) green.*")
    blue_reg = re.compile(r".*\s(\d+) blue.*")
    for line in inp.splitlines():
        game_s, rest = line.split(":")
        game = int(game_s.replace("Game ", ""))
        sub_games = rest.split(";")
        red_min = 0
        green_min = 0
        blue_min = 0
        for sub in sub_games:
            red_match = red_reg.match(sub)
            red_cnt = int(red_match.group(1)) if red_match else 0
            green_match = green_reg.match(sub)
            green_cnt = int(green_match.group(1)) if green_match else 0
            blue_match = blue_reg.match(sub)
            blue_cnt = int(blue_match.group(1)) if blue_match else 0
            red_min = max(red_min, red_cnt)
            green_min = max(green_min, green_cnt)
            blue_min = max(blue_min, blue_cnt)
        acc += red_min * blue_min * green_min
    return acc


test_part_1 = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n\
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n\
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n\
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n\
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"


if __name__ == "__main__":
    print(f"{solve_part_1(test_part_1) = }")
    inp = sys.argv[1]
    print(solve_part_1(inp))

    print(f"{solve_part_2(test_part_1) = }")
    print(solve_part_2(inp))
