import main

from timeit import default_timer as timer


class Coord(object):
    def __init__(self, x, y, z):
        self["x"] = x
        self["y"] = y
        self["z"] = z


class Brick(object):
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.start = {"x": x1, "y": y1, "z": z1}
        self.end = {"x": x2, "y": y2, "z": z2}
        self.ranges = {
            "x": range(min(x1, x2), max(x1, x2) + 1),
            "y": range(min(y1, y2), max(y1, y2) + 1),
            "z": range(min(z1, z2), max(z1, z2) + 1),
        }
        self.over = set()
        self.under = set()


def parse_bricks(lines):
    # parse bricks
    bricks = [Brick(*list(map(int, l.replace("~", ",").split(",")))) for l in lines]

    # define a grid of bricks positions
    # Start by finding ranges in which they lay in (x, y, z)
    mins = {"x": 1000, "y": 1000, "z": 1000}
    maxs = {"x": 0, "y": 00, "z": 000}
    for brick in bricks:
        for c in "xyz":
            mins[c] = min(mins[c], brick.start[c], brick.end[c])
            maxs[c] = max(maxs[c], brick.start[c], brick.end[c])
    # Create the grid
    grid = [
        [[None for _ in range(maxs["z"] + 2)] for _ in range(maxs["y"] + 1)]
        for _ in range(maxs["x"] + 1)
    ]
    # Fill it
    for idx, brick in enumerate(bricks):
        for x in brick.ranges["x"]:
            for y in brick.ranges["y"]:
                for z in brick.ranges["z"]:
                    grid[x][y][z] = idx

    # Fall the bricks
    while True:
        no_more_fall = True
        for idx, brick in enumerate(bricks):
            while all(
                z > 1 and grid[x][y][z - 1] in [None, idx]
                for x in brick.ranges["x"]
                for y in brick.ranges["y"]
                for z in brick.ranges["z"]
            ):
                no_more_fall = False
                for x in brick.ranges["x"]:
                    for y in brick.ranges["y"]:
                        for z in brick.ranges["z"]:
                            grid[x][y][z - 1] = idx
                            grid[x][y][z] = None

                brick.start["z"] -= 1
                brick.end["z"] -= 1
                brick.ranges["z"] = range(
                    brick.ranges["z"].start - 1, brick.ranges["z"].stop - 1
                )
        if no_more_fall:
            break

    # Now we can parse for each brick, which other bricks lay over and which other bricks support it
    for idx, brick in enumerate(bricks):
        for x in brick.ranges["x"]:
            for y in brick.ranges["y"]:
                for z in brick.ranges["z"]:
                    brick.over.add(grid[x][y][z + 1])
                    brick.under.add(grid[x][y][z - 1])

        if idx in brick.over:
            brick.over.remove(idx)
        if idx in brick.under:
            brick.under.remove(idx)
        if None in brick.under:
            brick.under.remove(None)
        if None in brick.over:
            brick.over.remove(None)

    return bricks


@main.pretty_level
def part_2(lines):
    bricks = parse_bricks(lines)

    # For all bricks if it only supports bricks that have multiple support, we can add destroy it
    nb_removable = sum(
        [all([len(bricks[b].under) > 1 for b in brick.over]) for brick in bricks]
    )

    return nb_removable


@main.pretty_level
def part_2(lines):
    bricks = parse_bricks(lines)

    total = 0

    for idx in range(len(bricks)):
        del_bricks = set([idx])
        while True:
            new_del_bricks = set([idx])
            for del_idx in del_bricks:
                for b in bricks[del_idx].over:
                    if bricks[b].under.intersection(del_bricks) == bricks[b].under:
                        new_del_bricks.add(b)

            if len(new_del_bricks) == len(del_bricks):
                break
            del_bricks = new_del_bricks

        total += len(del_bricks) - 1

    return total
