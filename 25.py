import main
import graphviz
import math
import networkx


def get_graph_from_input(lines):
    graph = networkx.Graph()
    for line in lines:
        left, rights = line.split(":")
        rights = [x for x in rights.split(" ") if x]
        for right in rights:
            graph.add_edge(left, right)
    return graph


def print_graph(graph):
    viz = graphviz.Graph("Level 20")
    for edge in graph.edges():
        viz.edge(edge[0], edge[1])
    viz.render("lvl25.graf")


@main.pretty_level
def part_1(lines):
    # Create the graph with networkx
    graph = get_graph_from_input(lines)

    # Get the minimum cut. It must be 3 (because of the initial statements)
    minimum_cut = networkx.minimum_edge_cut(graph)
    assert len(minimum_cut) == 3

    # Remove edges from the minimum cut to divide the graph into 2 subgraphs
    graph.remove_edges_from(minimum_cut)

    return math.prod([len(x) for x in networkx.connected_components(graph)])


@main.pretty_level
def part_2(lines):
    return 42
