"""Pytest for centrality measures."""

import numpy as np
import pytest

from graph_time_series import Graph
from graph_time_series.observables import (
    betweenness_centrality,
    closeness_centrality,
    degree_centrality,
    h_index_centrality,
)
from graph_time_series.utilities import random_adj_matrix_er

# ---------------- Fixtures ----------------


@pytest.fixture
def star_graph() -> Graph:
    """Star graph with 5 nodes: node 0 is center."""
    ad_mat = np.zeros((5, 5))
    for i in range(1, 5):
        ad_mat[0, i] = 1
        ad_mat[i, 0] = 1
    return Graph(ad_mat)


@pytest.fixture
def path_graph() -> Graph:
    """Path graph with 4 nodes: 0-1-2-3."""
    ad_mat = np.zeros((4, 4))
    ad_mat[0, 1] = ad_mat[1, 0] = 1
    ad_mat[1, 2] = ad_mat[2, 1] = 1
    ad_mat[2, 3] = ad_mat[3, 2] = 1
    return Graph(ad_mat)


# ---------------- Tests ----------------


def test_degree_centrality_star(star_graph: Graph) -> None:
    dc = degree_centrality(star_graph)
    # Center node 0 should have degree 1.0 (normalized)
    assert np.isclose(dc[0], 1.0)
    for i in range(1, 5):
        assert np.isclose(dc[i], 0.25)


def test_closeness_centrality_star(star_graph: Graph) -> None:
    cc = closeness_centrality(star_graph)
    # Center node highest closeness
    assert cc[0] > max(cc[i] for i in range(1, 5))
    # Leaves all equal
    leaves = [cc[i] for i in range(1, 5)]
    assert np.allclose(leaves, leaves[0])


def test_betweenness_centrality_star(star_graph: Graph) -> None:
    bc = betweenness_centrality(star_graph)
    # Center node highest
    assert bc[0] > max(bc[i] for i in range(1, 5))
    # Leaves all equal (and 0)
    leaves = [bc[i] for i in range(1, 5)]
    assert np.allclose(leaves, 0.0)


def test_h_index_centrality_star(star_graph: Graph) -> None:
    hc = h_index_centrality(star_graph)
    assert hc[0] == 1.0  # center has 4 neighbors with degree>=1
    for i in range(1, 5):
        assert hc[i] == 1.0  # leaves have 1 neighbor (the center)


def test_degree_path_graph(path_graph: Graph) -> None:
    dc = degree_centrality(path_graph)
    # endpoints degree 1/(n-1) = 1/3 ≈ 0.3333
    assert np.isclose(dc[0], 1 / 3)
    assert np.isclose(dc[3], 1 / 3)
    # middle nodes degree 2/3 ≈ 0.6666
    assert np.isclose(dc[1], 2 / 3)
    assert np.isclose(dc[2], 2 / 3)


def test_closeness_path_graph(path_graph: Graph) -> None:
    cc = closeness_centrality(path_graph)
    # Node 1 and 2 should be highest
    assert cc[1] == max(cc.values())
    assert cc[2] == max(cc.values())


def test_random_graph_h_index() -> None:
    ad_mat = random_adj_matrix_er(n=5, p=0.5, seed=42)
    g = Graph(ad_mat)
    hc = h_index_centrality(g)
    # H-index should be non-negative and int
    for v in hc.values():
        assert v >= 0
        assert isinstance(v, int)
