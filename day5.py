#!/usr/bin/env python3
import sys
import re
from pprint import pprint

test_inp = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def array_chunk(list, size):
    for i in range(0, len(list), size):
        yield list[i : i + size]


def part_1_steps_rec(inps: set[int], maps: list[tuple[int]], depth) -> int:
    acc = set()
    for inp in inps:
        inp_mapped = False
        for triple in maps[depth]:
            if not inp_mapped:
                dest_start, source_start, map_range = triple
                if inp in range(source_start, source_start + map_range):
                    acc.add(inp + dest_start - source_start)
                    inp_mapped = True
        if not inp_mapped:
            acc.add(inp)
    if depth == 6:
        return min(acc)
    return part_1_steps_rec(acc, maps, depth + 1)


def solve_part_1(inp: str) -> int:
    ints_re = re.compile(r"\d+")
    seeds_s, rest = inp.split("seed-to-soil map:")
    maps_s = rest.split("\n\n")
    seeds = set([int(x) for x in ints_re.findall(seeds_s)])
    map_vals = [
        [bla for bla in array_chunk([int(y) for y in ints_re.findall(x)], 3)]
        for x in maps_s
    ]
    return part_1_steps_rec(seeds, map_vals, 0)


def part_2_steps_rec(
    inp: int, maps: list[tuple[int]], depth, seed_pairs: tuple[int, int]
) -> bool:
    if depth == -1:
        return any(inp in range(seed[0], seed[0] + seed[1]) for seed in seed_pairs)
    val = None
    inp_mapped = False
    for triple in maps[depth]:
        dest_start, source_start, map_range = triple
        if inp in range(dest_start, dest_start + map_range):
            val = inp + source_start - dest_start
            inp_mapped = True
    if not inp_mapped:
        val = inp
    return part_2_steps_rec(val, maps, depth - 1, seed_pairs)


def solve_part_2(inp: str) -> int:
    ints_re = re.compile(r"\d+")
    seeds_s, rest = inp.split("seed-to-soil map:")
    maps_s = rest.split("\n\n")
    seed_pairs = [x for x in array_chunk([int(y) for y in ints_re.findall(seeds_s)], 2)]
    map_vals = [
        [bla for bla in array_chunk([int(y) for y in ints_re.findall(x)], 3)]
        for x in maps_s
    ]
    guess = 0
    while True:
        if part_2_steps_rec(guess, map_vals, 6, seed_pairs):
            return guess
        guess += 1


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 35
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    assert solve_part_2(test_inp) == 46
    print(f"{solve_part_2(inp) = }")
