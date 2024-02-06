import re

import main


@main.pretty_level
def part_1(lines):
    values = {}
    mask = ""
    for line in lines:
        if line[0:7] == "mask = ":
            mask = line[7:]
        else:
            groups = re.search(r"mem\[(\d+)\] = (\d+)", line)
            address = int(groups[1])
            value = "{0:036b}".format(int(groups[2]))
            value = "".join([b if m == "X" else m for b, m in zip(value, mask)])
            values[address] = value
    return sum([int(x, 2) for x in values.values()])


@main.pretty_level
def part_2(lines):
    values = {}
    mask = ""
    floating_mask_values = set([0])
    for line in lines:
        if line[0:7] == "mask = ":
            mask = line[7:]
            floating_mask_values = set([0])
            for idx in range(36):
                if mask[idx] == "X":
                    new_floating_mask_values = set()
                    for value in floating_mask_values:
                        new_floating_mask_values.add(value)
                        new_floating_mask_values.add(value + pow(2, 35 - idx))
                    floating_mask_values = new_floating_mask_values
        else:
            groups = re.search(r"mem\[(\d+)\] = (\d+)", line)
            address = "{0:036b}".format(int(groups[1]))
            address = "".join(
                [
                    b if m == "0" else "1" if m == "1" else "0"
                    for b, m in zip(address, mask)
                ]
            )
            address = int(address, 2)
            value = int(groups[2])
            for mask_value in floating_mask_values:
                values[address + mask_value] = value
    return sum(values.values())
