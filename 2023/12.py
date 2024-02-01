from functools import lru_cache
import main


@lru_cache
def get_nb_possibles(row, series):
    # If the row is empty and series are empty => break point (1)
    if len(row) == 0 and len(series) == 0:
        return 1

    # If the remaining row is not enough for the remaining series => break point (0)
    if len(row) < sum(series) + len(series) - 1:
        return 0

    # If all broken series are done but we STILL have broken symbols => break point (0)
    # If all broken series are done but we NO MORE have broken symbols => break point (1)
    if len(series) == 0:
        return row.count("#") == 0

    # If row starts with '.' we can strip them and recurse
    if row[0] == ".":
        return get_nb_possibles(row.lstrip("."), series)

    # If row start with a new serie of broken
    if row[0] == "#":
        # If we have a end-of-serie char before the actual end of the serie => break point (0)
        if "." in row[0 : series[0]]:
            return 0

        # If this is the last series and the row ends perfectly at the end of the series => break point (1)
        if len(row) == series[0] and len(series) == 1:
            return 1

        # If after the serie is ended we still have a broken symbol '#' => break point (0)
        if "#" == row[series[0]]:
            return 0

        # Remove the serie from the start of the row and from the series list and iterate
        return get_nb_possibles(row[series[0] + 1 :], series[1:])

    # If the row starts with an interogation => iterate separately on each possible values '.' and '#'
    if row[0] == "?":
        return get_nb_possibles("#" + row[1:], series) + get_nb_possibles(
            "." + row[1:], series
        )

    # We should never be there => break point (0)
    return 0


@main.pretty_level
def part_1(lines):
    total = 0
    for line in lines:
        row = line.split(" ")[0]
        series = tuple([int(x) for x in line.split(" ")[1].split(",")])
        total += get_nb_possibles(row, series)
    return total


@main.pretty_level
def part_2(lines):
    total = 0
    for line in lines:
        row = "?".join([line.split(" ")[0]] * 5)
        series = tuple([int(x) for x in line.split(" ")[1].split(",")]) * 5
        total += get_nb_possibles(row, series)
    return total
