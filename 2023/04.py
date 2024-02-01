import regex as re
from math import floor
import main


@main.pretty_level
def part_1(lines):
    cards_scores = []

    for l in lines:
        winning_numbers = [
            int(x) for x in l.split(":")[1].split("|")[0].split(" ") if x
        ]
        my_numbers = [int(x) for x in l.split("|")[1].split(" ") if x]
        cards_scores.append(len(set(winning_numbers) & set(my_numbers)))

    return sum([pow(2, score - 1) for score in cards_scores if score])


@main.pretty_level
def part_2(lines):
    cards_scores = []

    for l in lines:
        winning_numbers = [
            int(x) for x in l.split(":")[1].split("|")[0].split(" ") if x
        ]
        my_numbers = [int(x) for x in l.split("|")[1].split(" ") if x]
        cards_scores.append(len(set(winning_numbers) & set(my_numbers)))

    cards_nb = [1] * len(cards_scores)
    for idx, nb in enumerate(cards_scores):
        for i in range(cards_scores[idx]):
            cards_nb[idx + i + 1] += cards_nb[idx]

    return sum(cards_nb)
