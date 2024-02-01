import main


SIZE = 5
SIZE = 25


def is_valid(values):
    for idx_1, value_1 in enumerate(values[:-2]):
        for value_2 in values[idx_1 + 1 : -1]:
            if value_1 + value_2 == values[-1]:
                return True
    return False


@main.pretty_level
def part_1(lines):
    values = [int(x) for x in lines]
    for analyzed_idx in range(SIZE, len(values) - 1):
        if not is_valid(values[analyzed_idx - SIZE : analyzed_idx + 1]):
            return values[analyzed_idx]

    return 0


@main.pretty_level
def part_2(lines):
    values = [int(x) for x in lines]

    # Exact same thing from part 1
    for analyzed_idx in range(SIZE, len(values) - 1):
        if not is_valid(values[analyzed_idx - SIZE : analyzed_idx + 1]):
            invalid_nb = values[analyzed_idx]
            break

    # Search from the start a subsequence
    for start_idx in range(len(values) - 1):
        for end_idx in range(start_idx + 1, len(values)):
            # if equals invalid value => done
            if sum(values[start_idx:end_idx]) == invalid_nb:
                return min(values[start_idx:end_idx]) + max(values[start_idx:end_idx])
            # if too big => rage quit this subsequence and go to next one
            elif sum(values[start_idx:end_idx]) > invalid_nb:
                break

    return 0
