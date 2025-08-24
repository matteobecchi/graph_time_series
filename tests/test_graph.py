"""Pytest for Graph class."""

from __future__ import annotations

from pathlib import Path

import pytest

from graph_time_series import Graph, utilities

# ---------------- Fixtures ----------------


@pytest.fixture(scope="module")
def here() -> Path:
    return Path(__file__).parent


# ---------------- Tests ----------------


def test_graph() -> None:
    """Test initialization and methods for Graph class."""
    ad_mat = utilities.random_adj_matrix_er(n=10, seed=42)
    graph = Graph(ad_mat)

    degree_of_node_0 = 4
    assert graph.degree()[0] == degree_of_node_0

    graph.clustering()

    graph_dimaeter = 3
    assert graph.diameter() == graph_dimaeter
