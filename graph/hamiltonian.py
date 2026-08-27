from typing import Hashable


Node = Hashable
Graph = dict[Node, set[Node]]


DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def build_grid_graph(rows: int, cols: int) -> Graph:
    """
    Build an 8-neighbor grid graph.

    Each cell is connected to all valid neighboring cells in the
    four cardinal and four diagonal directions.

    Args:
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.

    Returns:
        An adjacency-list representation of the grid graph.

    Raises:
        ValueError: If rows or cols is not positive.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive")

    graph: Graph = {}

    for row in range(rows):
        for col in range(cols):
            node = (row, col)
            graph[node] = set()

            for row_offset, col_offset in DIRECTIONS:
                neighbor_row = row + row_offset
                neighbor_col = col + col_offset

                if (
                    0 <= neighbor_row < rows
                    and 0 <= neighbor_col < cols
                ):
                    graph[node].add((neighbor_row, neighbor_col))

    return graph


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
    if not graph:
        return []

    nodes = list(graph)
    total_nodes = len(nodes)

    def dfs(node: Node, path: list[Node], visited: set[Node]) -> list[Node] | None:
        if len(path) == total_nodes:
            return path.copy()

        for neighbor in graph[node]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            path.append(neighbor)

            result = dfs(neighbor, path, visited)
            if result is not None:
                return result

            path.pop()
            visited.remove(neighbor)

        return None

    for start in nodes:
        visited = {start}
        path = [start]

        result = dfs(start, path, visited)
        if result is not None:
            return result

    return None