"""Compute centrality measures on the graphs."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph

import networkx as nx


def degree_centrality(graph: Graph) -> dict[int, float]:
    """Return the degree centrality of each node.

    For an undirected graph with n nodes, degree centrality of node i
    is defined as deg(i) / (n - 1). It is thus normalized between 0 and 1.

    Example:

        .. testcode:: centr-deg-test

            from graph_time_series import Graph
            from graph_time_series.observables import degree_centrality
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the number of nodes
            dict_centrality = degree_centrality(graph)

        .. testcode:: centr-deg-test
            :hide:

            import numpy as np
            assert np.isclose(dict_centrality[0], 0.4444444444444444)
    """
    return dict(nx.degree_centrality(graph.nx_graph))


def h_index_centrality(graph: Graph) -> dict[int, int]:
    """Return the H-index centrality of each node.

    The H-index centrality of node i is the largest integer h such that
    node i has at least h neighbors with degree >= h.

    Example:

        .. testcode:: centr-hindex-test

            from graph_time_series import Graph
            from graph_time_series.observables import h_index_centrality
            from graph_time_series.utilities import random_adj_matrix_er

            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            dict_centrality = h_index_centrality(graph)

        .. testcode:: centr-hindex-test
            :hide:

            import numpy as np
            assert dict_centrality[0] == 3
    """
    # Precompute all degrees
    deg = graph.get_degree()
    centrality: dict[int, int] = {}

    for node in graph.nx_graph.nodes():
        # degrees of neighbors
        neigh_degs = sorted(
            (deg[nbr] for nbr in graph.nx_graph.neighbors(node)), reverse=True
        )
        h = 0
        for i, d in enumerate(neigh_degs, start=1):
            if d >= i:
                h = i
            else:
                break
        centrality[node] = h

    return centrality


def closeness_centrality(graph: Graph) -> dict[int, float]:
    """Return the closeness centrality of each node.

    Closeness centrality of node i is defined as the reciprocal of the average
    shortest path distance from i to all other reachable nodes.

    Example:

        .. testcode:: centr-close-test

            from graph_time_series import Graph
            from graph_time_series.observables import closeness_centrality
            from graph_time_series.utilities import random_adj_matrix_er

            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            dict_centrality = closeness_centrality(graph)

        .. testcode:: centr-close-test
            :hide:

            import numpy as np
            assert np.isclose(dict_centrality[0], 0.6428571428571429)
    """
    return dict(nx.closeness_centrality(graph.nx_graph))


def betweenness_centrality(graph: Graph) -> dict[int, float]:
    """Return the betweenness centrality of each node.

    Betweenness centrality of a node is defined as the fraction of all
    shortest paths between pairs of nodes that pass through this node.

    Normalization ensures values lie in [0, 1].

    Example:

        .. testcode:: centr-betw-test

            from graph_time_series import Graph
            from graph_time_series.observables import betweenness_centrality
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            dict_centrality = betweenness_centrality(graph)

        .. testcode:: centr-betw-test
            :hide:

            import numpy as np
            assert np.isclose(dict_centrality[0], 0.2731481481481481)
    """
    return dict(nx.betweenness_centrality(graph.nx_graph, normalized=True))
