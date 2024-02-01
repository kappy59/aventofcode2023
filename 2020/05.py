import main


def get_ids(lines):
    return [
        int(
            line.replace("F", "0")
            .replace("B", "1")
            .replace("L", "0")
            .replace("R", "1"),
            2,
        )
        for line in lines
    ]


@main.pretty_level
def part_1(lines):
    return max(get_ids(lines))


@main.pretty_level
def part_2(lines):
    ids = sorted(get_ids(lines))
    for i in range(1024):
        if i not in ids and i - 1 in ids and i + 1 in ids:
            return i
    return 0
