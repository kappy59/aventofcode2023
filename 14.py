from functools import lru_cache, cache
import main


@main.pretty_level
def part_1(lines):
    # turn lines into list to get [] operator
    lines = [list(line) for line in lines]

    lines = roll_north(lines)

    return sum([line.count("O") * (len(lines) - l) for l, line in enumerate(lines)])


def roll_north(lines):
    for c in range(len(lines[0])):
        next_available = None
        for r in range(len(lines)):
            if lines[r][c] == ".":
                next_available = r if next_available is None else next_available
            elif lines[r][c] == "#":
                next_available = None
            else:
                if next_available is not None:
                    lines[r][c] = "."
                    lines[next_available][c] = "O"
                    next_available += 1
    return lines


def roll_south(lines):
    for c in range(len(lines[0])):
        next_available = None
        for r in range(len(lines) - 1, -1, -1):
            if lines[r][c] == ".":
                next_available = r if next_available is None else next_available
            elif lines[r][c] == "#":
                next_available = None
            else:
                if next_available is not None:
                    lines[r][c] = "."
                    lines[next_available][c] = "O"
                    next_available -= 1
    return lines


def roll_west(lines):
    for r in range(len(lines)):
        next_available = None
        for c in range(len(lines[0])):
            if lines[r][c] == ".":
                next_available = c if next_available is None else next_available
            elif lines[r][c] == "#":
                next_available = None
            else:
                if next_available is not None:
                    lines[r][c] = "."
                    lines[r][next_available] = "O"
                    next_available += 1
    return lines


def roll_east(lines):
    for r in range(len(lines)):
        next_available = None
        for c in range(len(lines[0]) - 1, -1, -1):
            if lines[r][c] == ".":
                next_available = c if next_available is None else next_available
            elif lines[r][c] == "#":
                next_available = None
            else:
                if next_available is not None:
                    lines[r][c] = "."
                    lines[r][next_available] = "O"
                    next_available -= 1
    return lines


@main.pretty_level
def part_2(lines):
    # turn lines into list to get [] operator
    lines = [list(line) for line in lines]

    memory = {}
    loop_size = None
    start_of_loop = None
    for i in range(1, 1000000000 + 1):
        lines = roll_north(lines)
        lines = roll_west(lines)
        lines = roll_south(lines)
        lines = roll_east(lines)

        key = "".join(["".join(l) for l in lines])
        if key not in memory:
            memory[key] = i
        else:
            start_of_loop = memory[key]
            loop_size = i - memory[key]
            break

    # compute which idx we should get (knowing there is a loop)
    idx = (1000000000 - start_of_loop) % loop_size + start_of_loop

    # retreive key for this idx
    key = {v: k for k, v in memory.items()}[idx]
    lines = [key[i : i + len(lines[0])] for i in range(0, len(key), len(lines[0]))]

    return sum([line.count("O") * (len(lines) - l) for l, line in enumerate(lines)])
