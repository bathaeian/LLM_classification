from typing import Hashable


Node = Hashable
Graph = dict[Node, set[Node]]


def longest_hamiltonian_path(graph: Graph) -> list[Node] | None:
    """
    Find a Hamiltonian path in the given graph.

    A Hamiltonian path visits every vertex exactly once.

    Args:
        graph: An adjacency-list representation of the graph.
               Each key is a vertex and its value is the set of
               adjacent vertices.

    Returns:
        A Hamiltonian path containing every vertex exactly once,
        or None if no Hamiltonian path exists.
    """
    raise NotImplementedError