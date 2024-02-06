from functools import lru_cache


import main


NB_ITER = 6


@lru_cache
def neighbours(x, y, z, w, max_x, max_y, max_z, max_w):
    res = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dw in [-1, 0, 1]:
                    res.add(
                        (
                            min(max_x - 1, max(0, x + dx)),
                            min(max_y - 1, max(0, y + dy)),
                            min(max_z - 1, max(0, z + dz)),
                            min(max_w - 1, max(0, w + dw)),
                        )
                    )
    res.remove((x, y, z, w))
    return res


def part(grid, size_x, size_y, size_z, size_w):
    for _ in range(NB_ITER):
        new_grid = [
            [
                [["." for _ in range(size_w)] for _ in range(size_z)]
                for _ in range(size_y)
            ]
            for _ in range(size_x)
        ]
        for x in range(size_x):
            for y in range(size_y):
                for z in range(size_z):
                    for w in range(size_w):
                        if grid[x][y][z][w] == "#" and sum(
                            [
                                grid[X][Y][Z][W] == "#"
                                for X, Y, Z, W in neighbours(
                                    x, y, z, w, size_x, size_y, size_z, size_w
                                )
                            ]
                        ) in [2, 3]:
                            new_grid[x][y][z][w] = "#"
                        if (
                            grid[x][y][z][w] == "."
                            and sum(
                                [
                                    grid[X][Y][Z][W] == "#"
                                    for X, Y, Z, W in neighbours(
                                        x, y, z, w, size_x, size_y, size_z, size_w
                                    )
                                ]
                            )
                            == 3
                        ):
                            new_grid[x][y][z][w] = "#"
        grid = new_grid

    return sum([sum([sum([z.count("#") for z in y]) for y in x]) for x in grid])


@main.pretty_level
def part_1(lines):
    size_x = NB_ITER + NB_ITER + len(lines)
    size_y = NB_ITER + NB_ITER + len(lines[0])
    size_z = NB_ITER + NB_ITER + 1
    size_w = 1

    grid = [
        [[["." for _ in range(size_w)] for _ in range(size_z)] for _ in range(size_y)]
        for _ in range(size_x)
    ]
    for l_idx, line in enumerate(lines):
        for c_idx, char in enumerate(line):
            grid[NB_ITER + l_idx][NB_ITER + c_idx][NB_ITER][0] = char

    return part(grid, size_x, size_y, size_z, size_w)


@main.pretty_level
def part_2(lines):
    size_x = NB_ITER + NB_ITER + len(lines)
    size_y = NB_ITER + NB_ITER + len(lines[0])
    size_z = NB_ITER + NB_ITER + 1
    size_w = NB_ITER + NB_ITER + 1

    grid = [
        [[["." for _ in range(size_w)] for _ in range(size_z)] for _ in range(size_y)]
        for _ in range(size_x)
    ]
    for l_idx, line in enumerate(lines):
        for c_idx, char in enumerate(line):
            grid[NB_ITER + l_idx][NB_ITER + c_idx][NB_ITER][NB_ITER] = char

    return part(grid, size_x, size_y, size_z, size_w)
