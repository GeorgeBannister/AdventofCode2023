#!/usr/bin/env python3
import sys
import regex as re


def get_part_1_score(inp: str) -> int:
    score = 0
    for line in inp.splitlines():
        nums = re.findall(r"\d", line)
        if nums:
            score += int(nums[0] + nums[-1])
    return score


def get_part_2_score(inp: str) -> int:
    score = 0
    for line in inp.splitlines():
        nums = re.findall(r"(\d|one|two|three|four|five|six|seven|eight|nine)", line, overlapped=True)
        new_nums = [x.replace("one", "1")\
    .replace("two", "2")\
    .replace("three", "3")\
    .replace("four", "4")\
    .replace("five", "5")\
    .replace("six", "6")\
    .replace("seven", "7")\
    .replace("eight", "8")\
    .replace("nine", "9") for x in nums]
        if new_nums:
            score += int(new_nums[0] + new_nums[-1])
    return score


if __name__ == "__main__":
    inp = sys.argv[1]
    test_inp = "1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet"
    test_2_inp = "two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen"
    assert get_part_1_score(test_inp) == 142
    assert get_part_2_score(test_2_inp) == 281
    print(get_part_1_score(inp))
    print(f"{get_part_2_score(inp) = }")
