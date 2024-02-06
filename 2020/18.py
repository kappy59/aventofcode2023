import re

import main


# Attention when replacing the smaller computation in the bigger expression:
# It can occur that the pattern to be replaced is present multiple time in the expression
# By default, str.replace replaces ALL the occurences found
# We should specify from where to begin the replacement
# At least can we assume that we always want to replace only 1 match ?
#   => it seems to validate the part #2
# But fixed anyway


@main.pretty_level
def part_1(lines):
    def evaluate(line):
        while match := next(re.finditer(r"(\([0-9 \+\*]+\))", line), None):
            line = (
                line[: match.start()]
                + evaluate(match.group()[1:-1])
                + line[match.end() :]
            )

        splitted = line.split(" ")
        res = int(splitted[0])
        splitted = splitted[1:]
        while len(splitted):
            if splitted[0] == "+":
                res += int(splitted[1])
            elif splitted[0] == "*":
                res *= int(splitted[1])
            splitted = splitted[2:]
        return str(res)

    return sum([int(evaluate(line)) for line in lines])


@main.pretty_level
def part_2(lines):
    def evaluate(line):
        while match := next(re.finditer(r"(\([0-9 \+\*]+\))", line), None):
            line = (
                line[: match.start()]
                + evaluate(match.group()[1:-1])
                + line[match.end() :]
            )

        while match := next(re.finditer(r"(([0-9]+) \+ ([0-9]+))", line), None):
            line = (
                line[: match.start()]
                + str(int(match.group(2)) + int(match.group(3)))
                + line[match.end() :]
            )

        while match := next(re.finditer(r"(([0-9]+) \* ([0-9]+))", line), None):
            line = (
                line[: match.start()]
                + str(int(match.group(2)) * int(match.group(3)))
                + line[match.end() :]
            )

        return line

    return sum([int(evaluate(line)) for line in lines])
