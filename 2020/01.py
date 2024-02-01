import main


@main.pretty_level
def part_1(lines):
    numbers = [int(l) for l in lines]
    for idx, value_1 in enumerate(numbers[:-1]):
        for value_2 in numbers[idx + 1 :]:
            if value_1 + value_2 == 2020:
                return value_1 * value_2
    return 0


@main.pretty_level
def part_2(lines):
    numbers = [int(l) for l in lines]
    for idx_1, value_1 in enumerate(numbers[:-2]):
        for idx_2, value_2 in enumerate(numbers[idx_1 + 1 : -1]):
            for value_3 in numbers[idx_2 + 1 :]:
                if value_1 + value_2 + value_3 == 2020:
                    return value_1 * value_2 * value_3
    return 0
