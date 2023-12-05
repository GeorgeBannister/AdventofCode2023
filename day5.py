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
    yield list[i:i + size]

def solve_part_1(inp: str) -> int:
    ints_re = re.compile(r"\d+")
    seeds_s, rest = inp.split("seed-to-soil map:")
    maps_s = rest.split("\n\n")
    seeds = [int(x) for x in ints_re.findall(seeds_s)]
    map_vals = [ [bla for bla in array_chunk( [int(y) for y in ints_re.findall(x)] ,3)] for x in maps_s ]

    location_vals = []

    for seed in seeds:
        for step in map_vals:

    pprint(seeds)
    pprint(map_vals)



if __name__ == "__main__":
    assert solve_part_1(test_inp) == 35