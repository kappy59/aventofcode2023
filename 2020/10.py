import graphviz
from math import prod

import main


def visualize(jolts_outputs):
    viz = graphviz.Graph("Level 10")

    for idx, jolts_1 in enumerate(jolts_outputs[:-1]):
        for jolts_2 in jolts_outputs[idx + 1 : idx + 4]:
            if jolts_2 <= jolts_1 + 3:
                viz.edge(str(jolts_1), str(jolts_2))

    viz.render("lvl10.graf")


@main.pretty_level
def part_1(lines):
    # It seems that the connectors are not able to output a power lower than the input
    # The job here is reduced to ordering the output powers, sort them, compute the difference between neighbours and count 1s and 3s

    jolts_outputs = sorted([int(x) for x in lines])
    jolts_outputs = [0] + jolts_outputs + [jolts_outputs[-1] + 3]
    diffs = [b - a for a, b in zip(jolts_outputs, jolts_outputs[1:])]
    return diffs.count(1) * diffs.count(3)


@main.pretty_level
def part_2(lines):
    jolts_outputs = sorted([int(x) for x in lines])
    jolts_outputs = [0] + jolts_outputs + [jolts_outputs[-1] + 3]
    # More interesting now ! We allow different paths !!
    # But wait ! WHAT ! All the path keep the same behaviour as previously
    # Only difference is that we can bypass some connectors

    # visualize(jolts_outputs)

    # A quick visualization show us that we are likely to have single trails at some points, i.e. somewhere in the graph of connectors all paths will take the same subpath. We can therefore find these single traces, segment the all schbims in smaller chunks and compute all combinations for all smaller chunks. Then multiply everything.
    # A new chunk is found each time a jolt has only one possible predecessor with a diff of 3. (There are other of course but we can ignore them)

    chunks = [[0]]
    for idx in range(len(jolts_outputs) - 1):
        if jolts_outputs[idx + 1] - jolts_outputs[idx] == 3:
            chunks[-1].append(idx + 2)
            chunks.append([idx + 1])
    chunks.pop()  # Last element is not complete

    def get_nb_paths(jolts):
        if len(jolts) == 2 and jolts[1] - jolts[0] <= 3:
            return 1

        nb_paths = 0
        for idx in range(1, len(jolts)):
            if jolts[idx] - jolts[0] <= 3:
                nb_paths += get_nb_paths(jolts[idx:])

        return nb_paths

    return prod([get_nb_paths(jolts_outputs[chunk[0] : chunk[1]]) for chunk in chunks])
