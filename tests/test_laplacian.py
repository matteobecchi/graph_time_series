"""Pytest for laplacian-related calculations."""

import numpy as np
import pytest
from numpy.typing import NDArray

from graph_time_series import Graph, utilities
from graph_time_series.observables import laplacian, spectral_dimension


def lattice_1d_adjacency(n: int) -> NDArray[np.float64]:
    """1D lattice (path) with n nodes, edges between neighbors."""
    ad_mat = np.zeros((n, n))
    for i in range(n - 1):
        ad_mat[i, i + 1] = 1
        ad_mat[i + 1, i] = 1
    return ad_mat


def lattice_2d_adjacency(rows: int, cols: int) -> NDArray[np.float64]:
    """2D square lattice with rows x cols nodes, 4-neighbor connectivity."""
    n = rows * cols
    ad_mat = np.zeros((n, n))

    def node_index(r: int, c: int) -> int:
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            idx = node_index(r, c)
            # right neighbor
            if c + 1 < cols:
                j = node_index(r, c + 1)
                ad_mat[idx, j] = 1
                ad_mat[j, idx] = 1
            # down neighbor
            if r + 1 < rows:
                j = node_index(r + 1, c)
                ad_mat[idx, j] = 1
                ad_mat[j, idx] = 1
    return ad_mat


# ---------------- Fixtures ----------------


@pytest.fixture(scope="module")
def graph() -> Graph:
    ad_mat = utilities.random_adj_matrix_er(n=10, seed=42)
    return Graph(ad_mat)


@pytest.fixture
def lattice_1d() -> Graph:
    """Return a 1D lattice Graph with 10 nodes."""
    return Graph(lattice_1d_adjacency(1000))


@pytest.fixture
def lattice_2d() -> Graph:
    """Return a 2D lattice Graph 3x3 (9 nodes)."""
    return Graph(lattice_2d_adjacency(30, 30))


# ---------------- Tests ----------------


def test_laplacian(graph: Graph) -> None:
    l_matrix = laplacian(graph)
    assert np.isclose(l_matrix[0][0], 4.0)

    evals, _ = utilities.eigenpairs(l_matrix)
    assert np.isclose(evals[0], 0.0)


def test_spectral_dim(
    lattice_1d: Graph,
    lattice_2d: Graph,
) -> None:
    d_s = spectral_dimension(lattice_1d)
    assert np.isclose(d_s, 1.0981732774604245)
    d_s = spectral_dimension(lattice_2d)
    assert np.isclose(d_s, 2.1170282420739355)
