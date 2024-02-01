import heapq
import main

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def get_neighbors(grid, pos, dir_idx, min_steps=1, max_steps=3):
    neighbors = []
    allowed_dirs = [(dir_idx + 1) % 4, (dir_idx - 1) % 4]

    r, c = pos
    for dir_idx in allowed_dirs:
        for i in range(min_steps, max_steps + 1):
            dr, dc = DIRS[dir_idx]
            new_pos = (r + i * dr, c + i * dc)
            if new_pos in grid:
                neighbors.append(
                    (
                        new_pos,
                        dir_idx,
                        sum([grid[(r + k * dr, c + k * dc)] for k in range(1, i + 1)]),
                    )
                )

    return neighbors


def dijkstra(grid, start, end, min_steps=1, max_steps=3):
    # Queue elements are
    # ( cost , pos , dir_idx )
    queue = [(0, start, dir_idx) for dir_idx in range(len(DIRS))]
    heapq.heapify(queue)
    dists = {}

    while queue:
        cost, pos, dir_idx = heapq.heappop(queue)
        if (pos, dir_idx) in dists:  # and dists[((pos, dir_idx))][0] < cost:
            continue
        dists[(pos, dir_idx)] = cost

        if pos == end:
            for i in range(4):
                if (pos, i) in dists:
                    return dists[(pos, i)]
            return []

        for neighbor in get_neighbors(grid, pos, dir_idx, min_steps, max_steps):
            v, v_dir, v_cost = neighbor
            if v in grid and v not in dists:
                heapq.heappush(queue, (cost + v_cost, v, v_dir))

    return []


@main.pretty_level
def part_1(lines):
    # grid
    nodes = {
        (r, c): int(cost) for r, line in enumerate(lines) for c, cost in enumerate(line)
    }
    max_r = max(r for r, _ in nodes.keys())
    max_c = max(c for _, c in nodes.keys())

    cost = dijkstra(nodes, (0, 0), (max_r, max_c), 1, 3)

    return cost


@main.pretty_level
def part_2(lines):
    # grid
    nodes = {
        (r, c): int(cost) for r, line in enumerate(lines) for c, cost in enumerate(line)
    }
    max_r = max(r for r, _ in nodes.keys())
    max_c = max(c for _, c in nodes.keys())

    cost = dijkstra(nodes, (0, 0), (max_r, max_c), 4, 10)

    return cost
