from graph.hamiltonian import build_point_cloud_graph
from graph.hamiltonian import find_longest_simple_path


def is_valid_simple_path(graph, path):
    if path is None:
        return False

    if len(set(path)) != len(path):
        return False

    for current, next_node in zip(path, path[1:]):
        if next_node not in graph[current]:
            return False

    return True


def test_empty_point_cloud():
    graph = build_point_cloud_graph([])

    assert graph == {}
    assert find_longest_simple_path(graph) == []


def test_single_point():
    points = [(0, 0)]

    graph = build_point_cloud_graph(points)

    assert graph == {(0, 0): set()}
    assert find_longest_simple_path(graph) == [(0, 0)]


def test_cardinal_and_diagonal_neighbors():
    points = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    ]

    graph = build_point_cloud_graph(points)

    assert graph[(0, 0)] == {
        (0, 1),
        (1, 0),
        (1, 1),
    }


def test_points_with_gap_are_not_neighbors():
    points = [
        (0, 0),
        (0, 2),
        (2, 0),
        (2, 2),
    ]

    graph = build_point_cloud_graph(points)

    for point in points:
        assert graph[point] == set()


def test_diagonal_neighbors_are_allowed():
    points = [
        (0, 0),
        (1, 1),
    ]

    graph = build_point_cloud_graph(points)

    assert graph[(0, 0)] == {(1, 1)}
    assert graph[(1, 1)] == {(0, 0)}


def test_non_neighboring_points_are_not_connected():
    points = [
        (0, 0),
        (1, 2),
    ]

    graph = build_point_cloud_graph(points)

    assert graph[(0, 0)] == set()
    assert graph[(1, 2)] == set()


def test_missing_points_break_the_connection():
    points = [
        (0, 0),
        (0, 2),
    ]

    graph = build_point_cloud_graph(points)

    assert graph[(0, 0)] == set()
    assert graph[(0, 2)] == set()


def test_finds_longest_path_in_connected_point_cloud():
    points = [
        (0, 0),
        (0, 1),
        (1, 1),
        (2, 1),
    ]

    graph = build_point_cloud_graph(points)

    path = find_longest_simple_path(graph)

    assert is_valid_simple_path(graph, path)
    assert len(path) == 4


def test_finds_path_using_diagonal_edges():
    points = [
        (0, 0),
        (1, 1),
        (2, 2),
    ]

    graph = build_point_cloud_graph(points)

    path = find_longest_simple_path(graph)

    assert is_valid_simple_path(graph, path)
    assert len(path) == 3


def test_disconnected_point_cloud():
    points = [
        (0, 0),
        (0, 1),
        (5, 5),
    ]

    graph = build_point_cloud_graph(points)

    path = find_longest_simple_path(graph)

    assert is_valid_simple_path(graph, path)
    assert len(path) == 2


def test_longest_path_does_not_need_to_use_all_vertices():
    graph = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B"},
        "D": set(),
    }

    path = find_longest_simple_path(graph)

    assert is_valid_simple_path(graph, path)
    assert len(path) == 3
    assert set(path) == {"A", "B", "C"}


def test_longest_path_in_star_graph():
    graph = {
        "A": {"B", "C", "D"},
        "B": {"A"},
        "C": {"A"},
        "D": {"A"},
    }

    path = find_longest_simple_path(graph)

    assert is_valid_simple_path(graph, path)
    assert len(path) == 3
    assert "A" in path


def test_hamiltonian_path_is_found_when_all_vertices_are_connected():
    graph = {
        "A": {"B"},
        "B": {"A", "C"},
        "C": {"B", "D"},
        "D": {"C"},
    }

    path = find_longest_simple_path(graph)

    assert is_valid_simple_path(graph, path)
    assert len(path) == 4
    assert set(path) == {"A", "B", "C", "D"}