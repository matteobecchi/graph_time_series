"""Utilities functions for the package."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy.typing import NDArray

import networkx as nx
import numpy as np


def random_adj_matrix_er(
    n: int,
    p: float = 0.3,
    directed: bool = False,
    seed: int | None = None,
) -> NDArray[np.float64]:
    """Generate adjacency matrix from Erdős-Rényi random graph."""
    g = nx.gnp_random_graph(n, p, directed=directed, seed=seed)
    return nx.to_numpy_array(g)


def random_adj_matrix_ba(n: int, m: int = 2) -> NDArray[np.float64]:
    """Generate adjacency matrix from Barabási-Albert scale-free graph."""
    g = nx.barabasi_albert_graph(n, m)
    return nx.to_numpy_array(g)


def random_adj_matrix_ws(
    n: int, k: int = 2, p: float = 0.1
) -> NDArray[np.float64]:
    """Generate adjacency matrix from Watts-Strogatz small-world graph."""
    g = nx.watts_strogatz_graph(n, k, p)
    return nx.to_numpy_array(g)


def random_weighted_adj_matrix(
    n: int, p: float = 0.3, max_weight: float = 10.0
) -> NDArray[np.float64]:
    """Random weighted adjacency matrix."""
    rng = np.random.default_rng()
    mask = rng.random((n, n)) < p
    weights = rng.uniform(1, max_weight, size=(n, n))
    mat = mask * weights
    np.fill_diagonal(mat, 0)  # no self-loops
    return mat
