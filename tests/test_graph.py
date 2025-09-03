"""Pytest for Graph class."""

from __future__ import annotations

from pathlib import Path

import pytest

from graph_time_series import Graph, utilities

# ---------------- Fixtures ----------------


@pytest.fixture(scope="module")
def here() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="module")
def graph() -> Graph:
    ad_mat = utilities.random_adj_matrix_er(n=10, seed=42)
    return Graph(ad_mat)


# ---------------- Tests ----------------


def test_graph(graph: Graph) -> None:
    """Test initialization and methods for Graph class."""
    graph.get_n_nodes()
    graph.get_degree()
    graph.get_clustering()
    graph.get_diameter()
    graph.get_average_distance()
