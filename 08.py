import regex as re
from math import lcm

import main


@main.pretty_level
def part_1(lines):
    instructions = lines[0]

    mapping = {
        x[0]: (x[1], x[2])
        for line in lines[2:]
        if line
        for x in re.findall(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
    }
    cnt = 0
    position = "AAA"
    while position != "ZZZ":
        position = (
            mapping[position][0]
            if instructions[cnt % len(instructions)] == "L"
            else mapping[position][1]
        )
        cnt += 1
    return cnt


@main.pretty_level
def part_2(lines):
    instructions = lines[0]

    mapping = {
        x[0]: (x[1], x[2])
        for line in lines[2:]
        if line
        for x in re.findall(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
    }

    starters = [x for x in mapping.keys() if x.endswith("A")]
    enders = [x for x in mapping.keys() if x.endswith("Z")]

    cnts = []
    for position in starters:
        cnt = 0
        while position not in enders:
            position = (
                mapping[position][0]
                if instructions[cnt % len(instructions)] == "L"
                else mapping[position][1]
            )
            cnt += 1
        cnts.append(cnt)
    return lcm(*cnts)
