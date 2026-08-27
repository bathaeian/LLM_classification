from graph.hamiltonian import build_grid_graph
from graph.hamiltonian import longest_hamiltonian_path


def test_single_cell():
    graph = build_grid_graph(1, 1)

    assert graph == {
        (0, 0): set(),
    }


def test_two_by_two_has_diagonal_edges():
    graph = build_grid_graph(2, 2)

    assert graph[(0, 0)] == {
        (0, 1),
        (1, 0),
        (1, 1),
    }

    assert graph[(1, 1)] == {
        (0, 0),
        (0, 1),
        (1, 0),
    }


def test_all_eight_directions():
    graph = build_grid_graph(3, 3)

    center = (1, 1)

    expected_neighbors = {
        (0, 0), (0, 1), (0, 2),
        (1, 0),         (1, 2),
        (2, 0), (2, 1), (2, 2),
    }

    assert graph[center] == expected_neighbors


def test_corner_has_three_neighbors():
    graph = build_grid_graph(3, 3)

    assert len(graph[(0, 0)]) == 3
    assert len(graph[(0, 2)]) == 3
    assert len(graph[(2, 0)]) == 3
    assert len(graph[(2, 2)]) == 3


def test_center_has_eight_neighbors():
    graph = build_grid_graph(3, 3)

    assert len(graph[(1, 1)]) == 8


def test_invalid_dimensions():
    try:
        build_grid_graph(0, 3)
        assert False
    except ValueError:
        pass

    try:
        build_grid_graph(3, 0)
        assert False
    except ValueError:
        pass

def is_valid_path(graph, path):
    if path is None:
        return False

    if len(path) != len(graph):
        return False

    if len(set(path)) != len(path):
        return False

    for current, next_node in zip(path, path[1:]):
        if next_node not in graph[current]:
            return False

    return True


def test_finds_hamiltonian_path_in_3x3_grid():
    graph = build_grid_graph(3, 3)

    path = longest_hamiltonian_path(graph)

    assert is_valid_path(graph, path)


def test_finds_hamiltonian_path_in_2x3_grid():
    graph = build_grid_graph(2, 3)

    path = longest_hamiltonian_path(graph)

    assert is_valid_path(graph, path)


def test_diagonal_edges_are_allowed_in_hamiltonian_path():
    graph = build_grid_graph(2, 2)

    path = longest_hamiltonian_path(graph)

    assert is_valid_path(graph, path)

    diagonal_edges = {
        ((0, 0), (1, 1)),
        ((1, 1), (0, 0)),
        ((0, 1), (1, 0)),
        ((1, 0), (0, 1)),
    }

    assert any(
        (current, next_node) in diagonal_edges
        for current, next_node in zip(path, path[1:])
    )
    
def test_empty_graph():
    graph = {}

    path = longest_hamiltonian_path(graph)

    assert path == []


def test_single_vertex_graph():
    graph = {
        "A": set()
    }

    path = longest_hamiltonian_path(graph)

    assert path == ["A"]


def test_graph_without_hamiltonian_path():
    graph = {
        "A": {"B"},
        "B": {"A"},
        "C": set(),
    }

    path = longest_hamiltonian_path(graph)

    assert path is None


def test_hamiltonian_path_uses_every_vertex_exactly_once():
    graph = {
        "A": {"B", "C"},
        "B": {"A", "C", "D"},
        "C": {"A", "B", "D"},
        "D": {"B", "C"},
    }

    path = longest_hamiltonian_path(graph)

    assert is_valid_path(graph, path)
    assert len(path) == len(graph)
    assert len(set(path)) == len(graph)
    
def test_grid_graph_contains_all_eight_directions():
    graph = build_grid_graph(3, 3)

    center = (1, 1)

    expected_neighbors = {
        (0, 0),  # upper-left
        (0, 1),  # up
        (0, 2),  # upper-right
        (1, 0),  # left
        (1, 2),  # right
        (2, 0),  # lower-left
        (2, 1),  # down
        (2, 2),  # lower-right
    }

    assert graph[center] == expected_neighbors