import main


def parse_data(lines):
    empty_rows = set(range(len(lines[0])))
    empty_cols = set(range(len(lines[0])))
    galaxies = []

    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if lines[r][c] == "#":
                if c in empty_cols:
                    empty_cols.remove(c)
                if r in empty_rows:
                    empty_rows.remove(r)
                galaxies.append((r, c))

    return empty_rows, empty_cols, galaxies


def expand_galaxies(empty_rows, empty_cols, galaxies, stretch_factor):
    """Strech factor is: how many rows does one row become (similary for cols)"""
    expanded_galaxies = [
        (
            g[0] + sum([1 for r in empty_rows if r < g[0]]) * (stretch_factor - 1),
            g[1] + sum([1 for c in empty_cols if c < g[1]]) * (stretch_factor - 1),
        )
        for g in galaxies
    ]
    return expanded_galaxies


def get_total_distances(galaxies):
    total = 0
    for idx_1 in range(len(galaxies) - 1):
        for idx_2 in range(idx_1 + 1, len(galaxies)):
            total += abs(galaxies[idx_1][0] - galaxies[idx_2][0]) + abs(
                galaxies[idx_1][1] - galaxies[idx_2][1]
            )

    return total


@main.pretty_level
def part_1(lines):
    empty_rows, empty_cols, galaxies = parse_data(lines)
    galaxies = expand_galaxies(empty_rows, empty_cols, galaxies, 2)
    return get_total_distances(galaxies)


@main.pretty_level
def part_2(lines):
    empty_rows, empty_cols, galaxies = parse_data(lines)
    galaxies = expand_galaxies(empty_rows, empty_cols, galaxies, 1000000)
    print(galaxies)
    return get_total_distances(galaxies)
