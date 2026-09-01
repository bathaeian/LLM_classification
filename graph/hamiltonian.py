from typing import Hashable

Node = Hashable
Graph = dict[Node, set[Node]]

def build_point_cloud_graph(points: list[Node]) -> Graph:
    """
    Build a graph from a point cloud.

    Two points are connected if they are at most one grid step
    apart in both coordinates, excluding the point itself.

    This includes the four cardinal and four diagonal directions.
    """
    graph: Graph = {point: set() for point in points}

    for point in points:
        x, y = point

        for other in points:
            if point == other:
                continue

            other_x, other_y = other

            if (
                abs(x - other_x) <= 1
                and abs(y - other_y) <= 1
            ):
                graph[point].add(other)

    return graph


def find_longest_simple_path(graph: Graph) -> list[Node]:
    """
    Find the longest simple path in the graph.

    A simple path visits each vertex at most once.
    Unlike a Hamiltonian path, it does not have to visit
    every vertex in the graph.

    Args:
        graph: An adjacency-list representation of the graph.

    Returns:
        A longest simple path. If the graph is empty, returns [].
    """
    if not graph:
        return []

    nodes = list(graph)
    longest_path: list[Node] = []

    def dfs(
        node: Node,
        path: list[Node],
        visited: set[Node],
    ) -> None:
        nonlocal longest_path

        if len(path) > len(longest_path):
            longest_path = path.copy()

        for neighbor in graph[node]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            path.append(neighbor)

            dfs(neighbor, path, visited)

            path.pop()
            visited.remove(neighbor)

    for start in nodes:
        dfs(start, [start], {start})

    return longest_path