"""Compute Laplacian and related quantities on the graphs."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray

    from .graph import Graph

import networkx as nx


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
