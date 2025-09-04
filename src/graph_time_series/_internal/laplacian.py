"""Compute Laplacian and related quantities on the graphs."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from .graph import Graph

import networkx as nx
import numpy as np
from scipy.stats import linregress


def laplacian(graph: Graph) -> NDArray[np.float64]:
    """Return the Laplacian of the graph.

    For a graph with n nodes, the Laplacian matrix is defined as
    L = D - A, where D is the (diagonal) degree matrix, and A the adjacency
    matrix.

    Example:

        .. testcode:: laplacian-test

            from graph_time_series import Graph
            from graph_time_series.observables import laplacian
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the Laplacian
            l_matrix = laplacian(graph)

        .. testcode:: laplacian-test
            :hide:

            import numpy as np
            assert np.isclose(l_matrix[0][0], 4.0)
    """
    laplacian = nx.laplacian_matrix(graph.nx_graph, weight="weight")
    return laplacian.toarray()


def walk_length_distribution(graph: Graph, max_length: int) -> dict[int, int]:
    """Return distribution of closed walk counts up to given length.

    For each l in (1, max_length), compute:

        W_l = sum(λ_i^l)

    where λ_i are the Laplacian eigenvalues.

    Parameters:
        graph: input Graph.
        max_length: maximum walk length to compute.

    Returns:
        A dict mapping walk length l -> spectral walk count W_l.


    Example:

        .. testcode:: walks-test

            from graph_time_series import Graph
            from graph_time_series.observables import walk_length_distribution
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the Laplacian
            walk_dist = walk_length_distribution(graph, 5)

        .. testcode:: walks-test
            :hide:

            assert walk_dist[1] == 34
    """
    l_matrix = laplacian(graph)
    eigvals = np.linalg.eigvalsh(l_matrix)

    dist: dict[int, int] = {}
    for ell in range(1, max_length + 1):
        dist[ell] = round(np.sum(eigvals**ell))
    return dist


def spectral_dimension(
    graph: Graph,
    bins: int = 50,
    fit_range: tuple[int, int] = (1, 10),
    eigen_threshold: float = 1e-10,
) -> float:
    r"""Compute the spectral dimension of a graph.

    For a very large graph, the spectral dimension d_s is defined from the
    long-time behavior of the return probability of a random walk:

    .. math::
        P(t)\sim t^{-d_s / 2}, t\rightarrow \infty

    where P(t) is the probability that a random walker starting at some node
    is back at the same node after t steps. Equivalently, d_s can be extracted
    from the density of states (DOS) of the Laplacian eigenvalues near zero:

    .. math::
        \rho(\lambda) \sim \lambda^{d_s/2 - 1}, \lambda\rightarrow 0

    Parameters:
        graph: the graph to compute the spectral dimension.
        bins: the number of bins for the eigenvalues DOS.
        fit_range: the indices of the DOS to include in the fitting.
        eigen_threshold: eigenvalues smaller than this threshold are ignored.

    Example:

        .. testcode:: spectral-test

            from graph_time_series import Graph
            from graph_time_series.observables import spectral_dimension
            from graph_time_series.utilities import random_adj_matrix_ws

            # Create a random graph
            ad_mat = random_adj_matrix_ws(n=100, seed=42)
            graph = Graph(ad_mat)

            # Compute the spectral dimension
            d_s = spectral_dimension(graph)

        .. testcode:: spectral-test
            :hide:

            import numpy as np
            assert np.isclose(d_s, 1.3164869124177108)
    """
    l_sparse = laplacian(graph).astype(float)  # keep as sparse
    # Convert to dense for eigvalsh
    l_matrix = l_sparse.todense() if hasattr(l_sparse, "todense") else l_sparse

    # Eigenvalues
    eigvals = np.linalg.eigvalsh(l_matrix)
    eigvals = eigvals[eigvals > eigen_threshold]

    # Histogram DOS
    hist, edges = np.histogram(eigvals, bins=bins, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])

    # Select fitting range (small lambda)
    x = np.log(centers[fit_range[0] : fit_range[1]])
    y = np.log(hist[fit_range[0] : fit_range[1]])

    slope, intercept, _, _, _ = linregress(x, y)

    return 2 * (slope + 1)
