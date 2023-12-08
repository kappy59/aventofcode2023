import regex as re

import main


@main.pretty_level
def part_1(lines):
    limits = {"red": 12, "green": 13, "blue": 14}

    total = 0

    for l in lines:
        game_idx = int(re.split(" |:", l)[1])
        draws = [draw.strip() for draw in re.split(";|:", l)[1:]]

        ignore = False
        for draw in draws:
            for draw_color in [x.strip() for x in draw.split(",")]:
                for color in limits.keys():
                    if draw_color.endswith(color):
                        nb = int(draw_color.split(" ")[0])
                        if nb > limits[color]:
                            ignore = True
                            break

        if not ignore:
            total += game_idx

    return total


@main.pretty_level
def part_2(lines):
    total = 0

    for l in lines:
        draws = [draw.strip() for draw in re.split(";|:", l)[1:]]

        cubes = {"red": 0, "green": 0, "blue": 0}
        for draw in draws:
            for draw_color in [x.strip() for x in draw.split(",")]:
                for color in cubes.keys():
                    if draw_color.endswith(color):
                        cubes[color] = max(cubes[color], int(draw_color.split(" ")[0]))

        total += cubes["red"] * cubes["green"] * cubes["blue"]

    return total
