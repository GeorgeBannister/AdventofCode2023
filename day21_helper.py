#!/usr/bin/env python3

# %%

xs = [
    65,
    196,
    327,
    458,
    589,
    720,
    851,
    982,
    1113,
    1244,
]
ys = [
    3847,
    34165,
    94697,
    185443,
    306403,
    457577,
    638965,
    850567,
    1092383,
    1364413,
]

# %%

# 3847 = a (65)^2 + 65 b + c
# 34165 = a (196)^2 + 196 b + c
# 94697 = a (327)^2 + 327 b + c

# %%

print(f"{65 * 65 = }")
print(f"{196 * 196 = }")
print(f"{327 * 327 = }")
# %%

# 3847 = a 4225+ 65 b
# 34165 = a 38416 + 196 b
# 94697 = a 106929 + 327 b


def solve_from_x(x: int) -> int:
    return (323777 / 17161) + x * (28731 / 17161) + x * x * (15107 / 17161)


# %%
for x in xs:
    print(f"{x = } {solve_from_x(x) = }")
# %%
print(f"{solve_from_x(26_501_365) = }")
