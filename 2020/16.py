import itertools
from math import prod
import regex as re


import main


def is_valid_value(value, fields):
    for field in fields.values():
        if value in field[0] or value in field[1]:
            return True
    return False


def parse(lines):
    input_sections = [
        list(group) for k, group in itertools.groupby(lines, lambda x: not x) if not k
    ]

    # fields
    fields = {}
    for line in input_sections[0]:
        groups = re.search(r"(\w+ ?\w+): (\d+)-(\d+) or (\d+)-(\d+)", line)
        fields[groups[1]] = [
            range(int(groups[2]), 1 + int(groups[3])),
            range(int(groups[4]), 1 + int(groups[5])),
        ]

    # myticket
    myticket = [int(x) for x in input_sections[1][1].split(",")]

    # other tickets
    other_tickets = []
    for line in input_sections[2][1:]:
        other_tickets.append([int(x) for x in line.split(",")])

    return fields, myticket, other_tickets


@main.pretty_level
def part_1(lines):
    fields, myticket, other_tickets = parse(lines)

    res = 0
    for ticket in other_tickets:
        for value in ticket:
            if not is_valid_value(value, fields):
                res += value

    return res


@main.pretty_level
def part_2(lines):
    # Parse input properly
    fields, myticket, other_tickets = parse(lines)

    # remove invalid tickets
    valid_other_tickets = []
    for ticket in other_tickets:
        if all([is_valid_value(value, fields) for value in ticket]):
            valid_other_tickets.append(ticket)

    # for all fields look at the each values of all the tickets.
    # create a correspondance table listing all position of values within tickets that are valid for each field in all tickets
    # that means: for each field, for each value_index through all tickets, if all are valid, then value_index is valid for the field name
    possible_positions_for_fields = {k: [] for k in fields.keys()}
    for field_name, field_ranges in fields.items():
        for idx in range(len(ticket)):
            if all(
                [
                    ticket[idx] in field_ranges[0] or ticket[idx] in field_ranges[1]
                    for ticket in valid_other_tickets
                ]
            ):
                possible_positions_for_fields[field_name].append(idx)

    # Then reduce the list to "validated correspondances"
    # fields that have only one possible position are "validated"
    # We simply add this information in a new correspondance table and remove the value_index from all other positions_for_fields
    # We can iterate until no "single position for a field" is found
    # Hopefully we will have reduced the entire set of fields names
    validated_positions_for_fields = {k: None for k in fields.keys()}
    while True:
        position = None
        for field_name, positions in possible_positions_for_fields.items():
            if len(positions) == 1:
                position = positions[0]
                validated_positions_for_fields[field_name] = position
                break
        if position is not None:
            for field_name, positions in possible_positions_for_fields.items():
                if position in possible_positions_for_fields[field_name]:
                    possible_positions_for_fields[field_name].remove(position)
        else:
            break

    return prod(
        [
            myticket[validated_positions_for_fields[field_name]]
            for field_name in fields.keys()
            if field_name[0:10] == "departure "
        ]
    )
