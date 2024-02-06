import main


def part(lines, nb_iterations):
    input_numbers = [int(x) for x in lines[0].split(",")]
    numbers = {nb: [idx] for idx, nb in enumerate(input_numbers)}
    last_nb = input_numbers[-1]
    nb_numbers = len(input_numbers)

    while nb_numbers < nb_iterations:
        diff = (
            0
            if last_nb not in numbers or len(numbers[last_nb]) == 1
            else numbers[last_nb][-1] - numbers[last_nb][-2]
        )
        if diff not in numbers:
            numbers[diff] = [nb_numbers]
        else:
            numbers[diff] = [numbers[diff][-1], nb_numbers]
        last_nb = diff
        nb_numbers += 1
    return last_nb


@main.pretty_level
def part_1(lines):
    # numbers = [int(x) for x in lines[0].split(",")]
    # while len(numbers) < 2020:
    #     if numbers[-1] not in numbers[:-1]:
    #         numbers.append(0)
    #     else:
    #         numbers.append(1 + numbers[-2::-1].index(numbers[-1]))
    # return numbers[-1]

    return part(lines, 2020)


@main.pretty_level
def part_2(lines):
    return part(lines, 30000000)
