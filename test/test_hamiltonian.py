from graph.hamiltonian import build_grid_graph


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