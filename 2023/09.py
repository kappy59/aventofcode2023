import main


def reduce(line):
    if all(x == 0 for x in line):
        return [
            line,
        ]
    return [line, *reduce([j - i for i, j in zip(line[:-1], line[1:])])]


def expand_r(reduction):
    reduction[-1].append(0)
    for i in range(len(reduction) - 2, -1, -1):
        reduction[i].append(reduction[i][-1] + reduction[i + 1][-1])
    return reduction


def expand_l(reduction):
    reduction[-1] = [0, *reduction[-1]]
    for i in range(len(reduction) - 2, -1, -1):
        reduction[i] = [reduction[i][0] - reduction[i + 1][0], *reduction[i]]
    return reduction


@main.pretty_level
def part_1(lines):
    return sum(
        expand_r(reduce([int(x) for x in line.split(" ") if x]))[0][-1]
        for line in lines
    )


@main.pretty_level
def part_2(lines):
    return sum(
        expand_l(reduce([int(x) for x in line.split(" ") if x]))[0][0] for line in lines
    )
