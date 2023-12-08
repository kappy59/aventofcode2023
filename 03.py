import regex as re

import main


class Nb(object):
    gears = {}

    def __init__(self, row, match, lines):
        self.row = row
        self.pos = match.span()
        self.match = match
        self.adjacent_symbols = []

        for r in range(row - 1, row + 2):
            for c in range(self.pos[0] - 1, self.pos[1] + 1):
                if lines[r][c] not in ".0123456789":
                    self.adjacent_symbols.append((lines[r][c], r, c))

    def value(self):
        return int(self.match.group())


@main.pretty_level
def part_1(lines):
    lines = ["." + l + "." for l in lines]
    lines = ["." * len(lines[0]), *lines, "." * len(lines[0])]

    numbers = []
    for row, l in enumerate(lines):
        matches = list(re.finditer("(\d+)", l))
        if matches:
            numbers.extend([Nb(row, match, lines) for match in matches])

    return sum([nb.value() for nb in numbers if nb.adjacent_symbols])


@main.pretty_level
def part_2(lines):
    lines = ["." + l + "." for l in lines]
    lines = ["." * len(lines[0]), *lines, "." * len(lines[0])]

    numbers = []
    gears = {}
    for row, l in enumerate(lines):
        matches = list(re.finditer("(\d+)", l))
        for match in matches:
            nb = Nb(row, match, lines)
            numbers.append(nb)
            for x in nb.adjacent_symbols:
                if x[0] == "*":
                    if x in gears:
                        gears[x].append(nb.value())
                    else:
                        gears[x] = [
                            nb.value(),
                        ]

    return sum([x[0] * x[1] for x in gears.values() if len(x) == 2])
