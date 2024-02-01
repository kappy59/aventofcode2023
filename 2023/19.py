import regex as re
from math import prod

import main


def apply_rule(rule, x, m, a, s):
    loc = {"x": x, "m": m, "a": a, "s": s}
    exec(rule, globals(), loc)
    return loc["newrule"]


@main.pretty_level
def part_1(lines):
    """I made this with exec. It can be changed to mutualise code with part 2.
    I'm keeping it this way to serve as an example for further usage.
    ATTENTION: before exec anything we should always prune the input !!! Never trust 3rd party input !!!
    """
    rules = {}
    total = 0
    for line in lines:
        if not len(line):
            continue
        if line[0] == "{":
            x, m, a, s = [int(i) for i in re.split("[,=]", line[1:-1])[1::2]]
            rule = "in"
            while rule not in ["A", "R"]:
                rule = apply_rule(rules[rule], x, m, a, s)
            if rule == "A":
                total += x + m + a + s
        else:
            groups = re.match(r"^(?P<name>\w+){(?P<conds>.*),(?P<default>\w+)}$", line)
            rules[groups["name"]] = []
            for tmp in groups["conds"].split(","):
                cond, dest = tmp.split(":")
                rules[groups["name"]].append(f'if {cond}:\n    newrule = "{dest}"\n')
            rules[groups["name"]] = "el".join(rules[groups["name"]])
            rules[groups["name"]] += f"else:\n    newrule = \"{groups['default']}\""

    return total


@main.pretty_level
def part_2(lines):
    # Parse the rules
    rules = {}
    for line in lines:
        if not len(line):
            break

        groups = re.match(r"^(?P<name>\w+){(?P<conds>.*),(?P<default>\w+)}$", line)
        rules[groups["name"]] = []
        conds = []
        for tmp in groups["conds"].split(","):
            cond, dest = tmp.split(":")
            rules[groups["name"]].append({"dest": dest, "conds": [cond, *conds]})
            conds.append(cond.replace("<", "!=").replace(">", "<=").replace("!=", ">="))
        rules[groups["name"]].append({"dest": groups["default"], "conds": conds})

    # Find all conditions combination that gives final "A"
    pathes = [{"path": ["in"], "conds": []}]
    accepted_conds = []
    # While there are still pathes to analyse
    while pathes:
        path = pathes[0]
        # what can be added at the end of the path
        for rule in rules[path["path"][-1]]:
            # if it is an accepted node, add the cumulated conditions of this path to the memory
            if rule["dest"] == "A":
                accepted_conds.append(path["conds"] + rule["conds"])
            # else if it is not a rejected node, append the node to the path and save it as a new path to analyse, keep trace of cumulated conds too
            elif rule["dest"] != "R":
                pathes.append(
                    {
                        "path": path["path"] + rule["dest"],
                        "conds": path["conds"] + rule["conds"],
                    }
                )
        # current path is dealt with, remove it from list of pathes to analyse
        pathes.pop(0)

    total = 0
    for conds in accepted_conds:
        # Compute the ranges of x, m, a, s that are allowed in the current accepted set of conditions
        ranges = {
            "x": [1, 4000],
            "m": [1, 4000],
            "a": [1, 4000],
            "s": [1, 4000],
        }
        for cond in conds:
            if cond[1:3] == ">=":
                ranges[cond[0]][0] = max(ranges[cond[0]][0], int(cond[3:]))
            elif cond[1] == ">":
                ranges[cond[0]][0] = max(ranges[cond[0]][0], int(cond[2:]) + 1)
            elif cond[1:3] == "<=":
                ranges[cond[0]][1] = min(ranges[cond[0]][1], int(cond[3:]))
            elif cond[1] == "<":
                ranges[cond[0]][1] = min(ranges[cond[0]][1], int(cond[2:]) - 1)

        # compute total
        total += prod([1 + ranges[k][1] - ranges[k][0] for k in "xmas"])

    return total
