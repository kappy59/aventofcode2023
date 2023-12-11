import main


def parse_map(lines):
    """Transform input into a dict of pipe connectors (keys are the position of the links)

    Remark: for part 2 we may want to 'change the resolution' to get finer vision of passages between two adjancent non connected pipes from the input
    """
    pipe_links = {}
    start = None
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "S":
                start = (2 * r, 2 * c)
                pipe_links[start] = []
            elif char == ".":
                ...
            elif char == "|":
                pipe_links[(2 * r, 2 * c)] = [(2 * r - 2, 2 * c), (2 * r + 2, 2 * c)]
            elif char == "-":
                pipe_links[(2 * r, 2 * c)] = [(2 * r, 2 * c - 2), (2 * r, 2 * c + 2)]
            elif char == "L":
                pipe_links[(2 * r, 2 * c)] = [(2 * r - 2, 2 * c), (2 * r, 2 * c + 2)]
            elif char == "F":
                pipe_links[(2 * r, 2 * c)] = [(2 * r, 2 * c + 2), (2 * r + 2, 2 * c)]
            elif char == "J":
                pipe_links[(2 * r, 2 * c)] = [(2 * r, 2 * c - 2), (2 * r - 2, 2 * c)]
            elif char == "7":
                pipe_links[(2 * r, 2 * c)] = [(2 * r, 2 * c - 2), (2 * r + 2, 2 * c)]

    # define the map beneath S
    for pos, links in pipe_links.items():
        if start in links:
            pipe_links[start].append(pos)

    return pipe_links, start


def find_loop(pipe_links, start_pos):
    """Find the loop of connecting pipes starting at start_pos
    We don't care about which way it goes"""

    # Initialize
    current_pos = start_pos
    loop = [current_pos]

    # Just take the first option available in current_pos as the next
    # Then remove the 2 one-way relations between current_pos and next
    # And loop until we get back to the beginning
    while (next_pos := pipe_links[current_pos][0]) != start_pos:
        loop.append(next_pos)
        pipe_links[current_pos].remove(next_pos)
        pipe_links[next_pos].remove(current_pos)
        current_pos = next_pos

    # close the loop
    loop.append(start_pos)
    return loop


@main.pretty_level
def part_1(lines):
    pipe_links, start_pos = parse_map(lines)
    loop = find_loop(pipe_links, start_pos)
    return len(loop) // 2


@main.pretty_level
def part_2(lines):
    """We need this time to perform hole filling inside the loop.

    But how do we know our initial inside-the-loop point ? => We don't !
    Therefore, we will fill the exterior. We don't know any point in there either,
    but we can and a border of emptiness all around. This way (0, 0) is surely out
    of the loop.

    How do we find the narrow passage connecting oustide area that seems fitting inside ?
    => Raise the resolution !!!! With one extra position between 2 consecutives in the grid,
    we will be able to 'force' the passage from the clearly outside of the loop to the nested outside zones

    In the end, we will need to count all outside filled positions that were inside the original grid, substract the length of the loop and it should be good

    ATTENTION: This is not as smart as it seems!
    There are betters ways to achieve the result.
    When iterating through lines of the grid, a "cell" is within the loop if we have entered the loop and not exited yet, i.e. if the number of loop cells met so far on this line is odd.
    """
    # add border to the map
    lines = [
        "." * (len(lines[0]) + 2),
        *map(lambda l: "." + l + ".", lines),
        "." * (len(lines[0]) + 2),
    ]

    # find the loop
    pipe_links, start_pos = parse_map(lines)
    loop = find_loop(pipe_links, start_pos)

    # edit the loop so that it takes into account the "sub positions" introduced by the resolution change
    loop_ext = loop.copy()
    for x in range(len(loop) - 1):
        loop_ext.insert(
            1 + x * 2,
            ((loop[x][0] + loop[x + 1][0]) // 2, (loop[x][1] + loop[x + 1][1]) // 2),
        )

    max_col = 2 * len(lines[0]) - 1
    max_row = 2 * len(lines) - 1

    outside = set()
    new_outside_pos = set(
        [
            (0, 0),
        ]
    )
    while len(new_outside_pos):
        pos = new_outside_pos.pop()
        if (
            pos[0] > 0
            and (pos[0] - 1, pos[1]) not in outside
            and (pos[0] - 1, pos[1]) not in loop_ext
        ):
            new_outside_pos.add((pos[0] - 1, pos[1]))
        if (
            pos[0] < max_row
            and (pos[0] + 1, pos[1]) not in outside
            and (pos[0] + 1, pos[1]) not in loop_ext
        ):
            new_outside_pos.add((pos[0] + 1, pos[1]))
        if (
            pos[1] > 0
            and (pos[0], pos[1] - 1) not in outside
            and (pos[0], pos[1] - 1) not in loop_ext
        ):
            new_outside_pos.add((pos[0], pos[1] - 1))
        if (
            pos[1] < max_col
            and (pos[0], pos[1] + 1) not in outside
            and (pos[0], pos[1] + 1) not in loop_ext
        ):
            new_outside_pos.add((pos[0], pos[1] + 1))
        outside.add(pos)

    outside_reduced = set([x for x in outside if x[0] % 2 == 0 and x[1] % 2 == 0])
    return len(lines[0]) * len(lines) - len(outside_reduced) - len(loop) + 1
