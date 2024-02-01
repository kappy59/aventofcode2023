import itertools

import main


@main.pretty_level
def part_1(lines):
    groups_anwsers = [
        list(group) for k, group in itertools.groupby(lines, lambda x: not x) if not k
    ]
    groups_combined_anwsers = [set("".join(ga)) for ga in groups_anwsers]
    return sum([len(g) for g in groups_combined_anwsers])


@main.pretty_level
def part_2(lines):
    groups_anwsers = [
        list(group) for k, group in itertools.groupby(lines, lambda x: not x) if not k
    ]
    all_anwsers = set("abcdefghijklmnopqrstuvwxyz")
    groups_crossed_anwsers = [all_anwsers.intersection(*ga) for ga in groups_anwsers]
    return sum([len(g) for g in groups_crossed_anwsers])
