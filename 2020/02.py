import main


@main.pretty_level
def part_1(lines):
    counter = 0
    for line in lines:
        rule, password = [x.strip() for x in line.split(":")]
        rule_occurences, rule_letter = [x.strip() for x in rule.split(" ")]
        rule_min, rule_max = [int(x) for x in rule_occurences.split("-")]
        if rule_min <= password.count(rule_letter) <= rule_max:
            counter += 1
    return counter


@main.pretty_level
def part_2(lines):
    counter = 0
    for line in lines:
        rule, password = [x.strip() for x in line.split(":")]
        positions, rule_letter = [x.strip() for x in rule.split(" ")]
        positions = [int(x) for x in positions.split("-")]
        if sum([password[x - 1] == rule_letter for x in positions]) == 1:
            counter += 1

    return counter
