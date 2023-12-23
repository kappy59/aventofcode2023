import graphviz

import main


def get_neighbors(pos, grid, no_slopes=True):
    neighbors = set()

    if no_slopes:
        if pos[0] > 0 and grid[pos[0] - 1][pos[1]] != "#":
            neighbors.add((pos[0] - 1, pos[1]))
        if pos[0] < len(grid) - 1 and grid[pos[0] + 1][pos[1]] != "#":
            neighbors.add((pos[0] + 1, pos[1]))
        if pos[1] > 0 and grid[pos[0]][pos[1] - 1] != "#":
            neighbors.add((pos[0], pos[1] - 1))
        if pos[1] < len(grid[0]) - 1 and grid[pos[0]][pos[1] + 1] != "#":
            neighbors.add((pos[0], pos[1] + 1))
    else:
        if pos[0] > 0 and grid[pos[0] - 1][pos[1]] in ".^":
            neighbors.add((pos[0] - 1, pos[1]))
        if pos[0] < len(grid) - 1 and grid[pos[0] + 1][pos[1]] in ".v":
            neighbors.add((pos[0] + 1, pos[1]))
        if pos[1] > 0 and grid[pos[0]][pos[1] - 1] in ".<":
            neighbors.add((pos[0], pos[1] - 1))
        if pos[1] < len(grid[0]) - 1 and grid[pos[0]][pos[1] + 1] in ".>":
            neighbors.add((pos[0], pos[1] + 1))

    if pos in neighbors:
        neighbors.remove(pos)

    return neighbors


def visualize(nodes, nodes_dists):
    graph = graphviz.Graph("simplified map")
    graph.node(str(nodes[0]), label="start")
    graph.node(str(nodes[1]), label="end")
    for node in nodes[2:]:
        graph.node(str(node))
    for node, dists in nodes_dists.items():
        for node_2, dist in dists.items():
            graph.edge(
                str(node),
                str(node_2),
                dir="forward",
                weight=str(len(dist)),
                label=str(len(dist)),
            )

    graph.render("lvl23.graf")


def find_longest_path(path, path_length, end_pos, graph):
    if path[-1] == end_pos:
        # print(f"found path ({path_length}) : {path}")
        return path, path_length

    longest_path = []
    longest_path_length = 0
    for node, dist in graph[path[-1]].items():
        if node not in path:
            new_path, new_path_length = find_longest_path(
                path + [node], path_length + len(dist) - 1, end_pos, graph
            )
            if new_path_length > longest_path_length:
                longest_path = new_path
                longest_path_length = new_path_length

    return longest_path, longest_path_length


def gogo(lines, no_slopes):
    start_pos = (0, lines[0].find("."))
    end_pos = (len(lines) - 1, lines[-1].find("."))

    # It is a graph problem. With each nodes being [start_pos, end_pos, intersections]
    nodes = [start_pos, end_pos]
    for r in range(1, len(lines) - 1):
        for c in range(len(lines[0])):
            if lines[r][c] != "#" and len(get_neighbors((r, c), lines, True)) > 2:
                nodes.append((r, c))

    nodes_dists = {}
    for node in nodes:
        nodes_dists[node] = {}
        paths = [[node, neighbor] for neighbor in get_neighbors(node, lines, no_slopes)]
        for path in paths:
            while True:
                if path[-1] in nodes:
                    nodes_dists[node][path[-1]] = path
                    break

                is_dead_end = True
                for neighbor in get_neighbors(path[-1], lines, no_slopes):
                    if neighbor not in path:
                        path.append(neighbor)
                        is_dead_end = False
                if is_dead_end:
                    break

    visualize(nodes, nodes_dists)

    path, length = find_longest_path([start_pos], 0, end_pos, nodes_dists)
    print(path)
    return path, length


@main.pretty_level
def part_1(lines):
    _, length = gogo(lines, False)
    return length


@main.pretty_level
def part_2(lines):
    _, length = gogo(lines, True)
    return length
