import regex as re

import main

"""WARNING: we can have situations like eightwo where eight and two overlap!
Therefore we cannot use re as a regex operator directly because it does not support overlaps
=> Using regex (with import as re) and the overlapped=True parameter in finditer
"""


@main.pretty_level
def part_1(lines):
    total = 0
    for l in lines:
        f = list(filter(str.isdigit, l))
        total += 10 * int(f[0]) + int(f[-1])
    return total


@main.pretty_level
def part_2(lines):
    litterals = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }

    total = 0
    for l in lines:
        matches = list(
            re.finditer(
                "(one|two|three|four|five|six|seven|eight|nine|\d)",
                l,
                overlapped=True,
            )
        )
        digits = sorted(matches, key=lambda m: m.pos)
        total += 10 * litterals[digits[0].group()] + litterals[digits[-1].group()]

    return total
