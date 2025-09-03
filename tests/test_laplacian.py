"""Pytest for laplacian-related calculations."""

import numpy as np
import pytest

from graph_time_series import Graph, utilities
from graph_time_series.observables import laplacian

# ---------------- Fixtures ----------------


@pytest.fixture(scope="module")
def graph() -> Graph:
    ad_mat = utilities.random_adj_matrix_er(n=10, seed=42)
    return Graph(ad_mat)


# ---------------- Tests ----------------


def test_laplacian(graph: Graph) -> None:
    l_matrix = laplacian(graph)
    assert np.isclose(l_matrix[0][0], 4.0)

    evals, _ = utilities.eigenpairs(l_matrix)
    assert np.isclose(evals[0], 0.0)
