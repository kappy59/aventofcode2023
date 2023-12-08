from math import prod
import main


@main.pretty_level
def part_1(lines):
    times = [int(time) for time in lines[0].split(":")[1].split(" ") if time]
    records = [int(record) for record in lines[1].split(":")[1].split(" ") if record]
    nb_races = len(times)

    return prod(
        [
            sum(
                [1 for t in range(times[race]) if t * (times[race] - t) > records[race]]
            )
            for race in range(nb_races)
        ]
    )


@main.pretty_level
def part_2(lines):
    time = int(lines[0].split(":")[1].replace(" ", ""))
    record = int(lines[1].split(":")[1].replace(" ", ""))

    return sum([1 for t in range(time) if t * (time - t) > record])
