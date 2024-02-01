import main


def nb_trees_for_slope(lines, dx, dy):
    x = y = 0
    nb_trees = 0
    while y < len(lines):
        if lines[y][x] == "#":
            nb_trees += 1
        x = (x + dx) % len(lines[0])
        y += dy
    return nb_trees


@main.pretty_level
def part_1(lines):
    return nb_trees_for_slope(lines, 3, 1)


@main.pretty_level
def part_2(lines):
    return (
        nb_trees_for_slope(lines, 1, 1)
        * nb_trees_for_slope(lines, 3, 1)
        * nb_trees_for_slope(lines, 5, 1)
        * nb_trees_for_slope(lines, 7, 1)
        * nb_trees_for_slope(lines, 1, 2)
    )
