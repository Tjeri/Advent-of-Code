import networkx as nx

from aoc.input import read_input


class BiDiGraph(nx.DiGraph):
    def add_edge(self, u_of_edge, v_of_edge, **attr):
        super().add_edge(u_of_edge, v_of_edge, **attr)
        super().add_edge(v_of_edge, u_of_edge, **attr)


def parse_graph(lines: list[str]) -> nx.Graph:
    graph = BiDiGraph()
    for line in lines:
        node, neighbors = line.split(': ')
        for neighbor in neighbors.split(' '):
            graph.add_edge(node, neighbor, capacity=1)
    return graph


def solve(graph: nx.Graph) -> int:
    for x in graph.nodes:
        for y in graph.nodes:
            if x == y:
                continue
            cut, (l, r) = nx.minimum_cut(graph, x, y)
            if cut == 3:
                return len(l) * len(r)
    raise ValueError


_lines = read_input(True)
_graph = parse_graph(_lines)
print(solve(_graph))
