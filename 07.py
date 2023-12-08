from functools import cmp_to_key
import main


class Hand(object):
    COMBINATION_FIVE_OF_A_KIND = {"desc": "five of a kind", "order": 1}
    COMBINATION_FOUR_OF_A_KIND = {"desc": "four of a kind", "order": 2}
    COMBINATION_FULL_HOUSE = {"desc": "full house", "order": 3}
    COMBINATION_THREE_OF_A_KIND = {"desc": "three of a kind", "order": 4}
    COMBINATION_TWO_PAIRS = {"desc": "two pairs", "order": 5}
    COMBINATION_ONE_PAIR = {"desc": "one pair", "order": 6}
    COMBINATION_NOTHING = {"desc": "nothing", "order": 7}
    CARDS_ORDER = ""

    def __init__(self, line: str):
        line = line.split(" ")
        self.cards = line[0]
        self.bid = int(line[1])

        self.compute_combination()

    def compute_combination(self):
        ...

    @classmethod
    def compare(cls, x, y):
        if x.combination == y.combination:
            for i in range(5):
                if x.cards[i] != y.cards[i]:
                    return (
                        -1
                        if cls.CARDS_ORDER.find(x.cards[i])
                        < cls.CARDS_ORDER.find(y.cards[i])
                        else 1
                    )
            return 0
        else:
            return -1 if x.combination["order"] < y.combination["order"] else 1

    def __str__(self) -> str:
        return f"{self.cards} => comb={self.combination} | bid={self.bid}"


class Hand_part_1(Hand):
    CARDS_ORDER = "AKQJT98765432"

    def compute_combination(self):
        cards_dict = {i: self.cards.count(i) for i in set(self.cards)}
        cards_dict = sorted(cards_dict.values(), reverse=True)

        if cards_dict[0] == 5:
            self.combination = Hand.COMBINATION_FIVE_OF_A_KIND
        elif cards_dict[0] == 4:
            self.combination = Hand.COMBINATION_FOUR_OF_A_KIND
        elif cards_dict[0] == 3 and cards_dict[1] == 2:
            self.combination = Hand.COMBINATION_FULL_HOUSE
        elif cards_dict[0] == 3:
            self.combination = Hand.COMBINATION_THREE_OF_A_KIND
        elif cards_dict[0] == 2 and cards_dict[1] == 2:
            self.combination = Hand.COMBINATION_TWO_PAIRS
        elif cards_dict[0] == 2:
            self.combination = Hand.COMBINATION_ONE_PAIR
        else:
            self.combination = Hand.COMBINATION_NOTHING


class Hand_part_2(Hand):
    CARDS_ORDER = "AKQT98765432J"

    def compute_combination(self):
        cards_dict = {i: self.cards.count(i) for i in set(self.cards)}
        nb_jokers = cards_dict.pop("J", 0)
        cards_dict = sorted(cards_dict.items(), key=lambda x: x[1], reverse=True)

        if nb_jokers == 5 or cards_dict[0][1] + nb_jokers == 5:
            self.combination = Hand.COMBINATION_FIVE_OF_A_KIND
        elif cards_dict[0][1] + nb_jokers == 4:
            self.combination = Hand.COMBINATION_FOUR_OF_A_KIND
        elif cards_dict[0][1] + nb_jokers == 3 and cards_dict[1][1] == 2:
            self.combination = Hand.COMBINATION_FULL_HOUSE
        elif cards_dict[0][1] + nb_jokers == 3:
            self.combination = Hand.COMBINATION_THREE_OF_A_KIND
        elif cards_dict[0][1] + nb_jokers == 2 and cards_dict[1][1] == 2:
            self.combination = Hand.COMBINATION_TWO_PAIRS
        elif cards_dict[0][1] + nb_jokers == 2:
            self.combination = Hand.COMBINATION_ONE_PAIR
        else:
            self.combination = Hand.COMBINATION_NOTHING


@main.pretty_level
def part_1(lines):
    hands = [Hand_part_1(line) for line in lines if line]
    hands = sorted(hands, key=cmp_to_key(Hand_part_1.compare))
    weights = range(len(hands), 0, -1)
    return sum([i.bid * j for (i, j) in zip(hands, weights)])


@main.pretty_level
def part_2(lines):
    hands = [Hand_part_2(line) for line in lines if line]
    hands = sorted(hands, key=cmp_to_key(Hand_part_2.compare))
    weights = range(len(hands), 0, -1)
    return sum([i.bid * j for (i, j) in zip(hands, weights)])
