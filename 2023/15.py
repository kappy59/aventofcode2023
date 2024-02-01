from functools import reduce
from collections import OrderedDict

import main


def hash(msg):
    return reduce(lambda total, c: (total + ord(c)) * 17 % 256, msg, 0)


@main.pretty_level
def part_1(lines):
    msgs = [x for x in lines[0].split(",") if x]
    return sum([hash(msg) for msg in msgs])


@main.pretty_level
def part_2(lines):
    msgs = [x for x in lines[0].split(",") if x]
    boxes = [OrderedDict() for _ in range(256)]
    for msg in msgs:
        if msg[-1] == "-":
            label = msg[:-1]
            box_idx = hash(label)
            boxes[box_idx].pop(label, None)
        else:
            label, focale = msg.split("=")
            focale = int(focale)
            box_idx = hash(label)
            boxes[box_idx][label] = focale

    total = 0
    for box_idx, box in enumerate(boxes):
        for slot_idx, slot in enumerate(boxes[box_idx]):
            total += (box_idx + 1) * (slot_idx + 1) * box[slot]

    return total
