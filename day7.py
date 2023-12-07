#!/usr/bin/env python3

import sys

test_inp = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

score_map = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

score_map_2 = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

labels = "AKQJT98765432"


def get_significant_score(hand: str) -> int:
    acc = [hand.count(char) for char in labels if hand.count(char) != 0]
    acc.sort()
    match acc:
        case [5]:
            return 7_000_000
        case [1, 4]:
            return 6_000_000
        case [2, 3]:
            return 5_000_000
        case [1, 1, 3]:
            return 4_000_000
        case [1, 2, 2]:
            return 3_000_000
        case [1, 1, 1, 2]:
            return 2_000_000
    return 1_000_000


def hand_to_score(hand: str) -> int:
    """7 = Full house, 1 = one of each"""
    acc = get_significant_score(hand)
    for i in range(5):
        acc += pow(14, i) * score_map[hand[-(i + 1)]]
    return acc


def solve_part_1(inp: str) -> int:
    bets = {}
    hand_acc = []
    for line in inp.splitlines():
        lhs, rhs = line.split()
        hand_acc.append(lhs)
        bets[lhs] = int(rhs)
    hand_acc.sort(key=hand_to_score)
    to_ret = 0
    for idx, hand in enumerate(hand_acc, start=1):
        to_ret += idx * bets[hand]
    return to_ret


def get_significant_score_2(hand: str) -> int:
    jokers = hand.count("J")
    hand = hand.replace("J", "")
    acc = [hand.count(char) for char in labels if hand.count(char) != 0]
    if len(acc) == 0:
        acc.append(0)
    biggest = max(acc)
    i = acc.index(biggest)
    acc[i] += jokers
    acc.sort()
    match acc:
        case [5]:
            return 7_000_000
        case [1, 4]:
            return 6_000_000
        case [2, 3]:
            return 5_000_000
        case [1, 1, 3]:
            return 4_000_000
        case [1, 2, 2]:
            return 3_000_000
        case [1, 1, 1, 2]:
            return 2_000_000
    return 1_000_000


def hand_to_score_2(hand: str) -> int:
    """7 = Full house, 1 = one of each"""
    acc = get_significant_score_2(hand)
    for i in range(5):
        acc += pow(14, i) * score_map_2[hand[-(i + 1)]]
    return acc


def solve_part_2(inp: str) -> int:
    bets = {}
    hand_acc = []
    for line in inp.splitlines():
        lhs, rhs = line.split()
        hand_acc.append(lhs)
        bets[lhs] = int(rhs)
    hand_acc.sort(key=hand_to_score_2)
    to_ret = 0
    for idx, hand in enumerate(hand_acc, start=1):
        to_ret += idx * bets[hand]
    return to_ret


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 6440
    assert solve_part_2(test_inp) == 5905
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
