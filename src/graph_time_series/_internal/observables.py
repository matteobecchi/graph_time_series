"""Compute observables on the graphs."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph


import networkx as nx


def n_nodes(graph: Graph) -> int:
    """Return the number of nodes.

    Parameters:

        graph: graph_time_series.Graph
            The graph we want to compute the number of nodes.

    Example:

        .. testcode:: nnodes-test

            from graph_time_series import Graph
            from graph_time_series.observables import n_nodes
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the number of nodes
            number_of_nodes = n_nodes(graph)

        .. testcode:: nnodes-test
            :hide:

            assert number_of_nodes == 10
    """
    return len(graph.nx_graph.nodes)


def degree(graph: Graph) -> dict[int, float]:
    """Return a dict of node degrees (weighted if graph is weighted).

    Parameters:

        graph: graph_time_series.Graph
            The graph we want to compute the nodes' degrees.

    Example:

        .. testcode:: degree-test

            from graph_time_series import Graph
            from graph_time_series.observables import degree
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the degree of the nodes
            degrees_dict = degree(graph)

        .. testcode:: degree-test
            :hide:

            assert degrees_dict[0] == 4
    """
    return dict(graph.nx_graph.degree(weight="weight"))


def clustering(graph: Graph) -> dict[int, float]:
    """Return clustering coefficients per node.

    Parameters:

        graph: graph_time_series.Graph
            The graph we want to compute the nodes' clustering coefficient.

    Example:

        .. testcode:: clust-test

            from graph_time_series import Graph
            from graph_time_series.observables import clustering
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the clustering coefficient of the nodes
            clust_dict = clustering(graph)

        .. testcode:: clust-test
            :hide:

            import numpy as np
            assert np.isclose(clust_dict[2], 1/3)
    """
    return dict(nx.clustering(graph.nx_graph.to_undirected(), weight="weight"))


def diameter(graph: Graph) -> int:
    """Return the diameter of the graph.

    Parameters
    ----------
    graph: graph_time_series.Graph
        The graph we want to compute the diameter.

    Example:

        .. testcode:: diameter-test

            from graph_time_series import Graph
            from graph_time_series.observables import diameter
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the diameter of the graph
            diameter = diameter(graph)

        .. testcode:: diameter-test
            :hide:

            assert diameter == 3
    """
    if nx.is_connected(graph.nx_graph.to_undirected()):
        return nx.diameter(graph.nx_graph.to_undirected())
    msg = "Graph is not connected."
    raise RuntimeError(msg)


def average_distance(graph: Graph) -> float:
    """Return the average shortest distance between nodes.

    Parameters
    ----------
    graph: graph_time_series.Graph
        The graph we want to compute the diameter.

    Example:

        .. testcode:: distance-test

            from graph_time_series import Graph
            from graph_time_series.observables import average_distance
            from graph_time_series.utilities import random_adj_matrix_er

            # Create a random graph
            ad_mat = random_adj_matrix_er(n=10, seed=42)
            graph = Graph(ad_mat)

            # Compute the average shortest distance between nodes
            shortest_dist = average_distance(graph)

        .. testcode:: distance-test
            :hide:

            import numpy as np
            assert np.isclose(shortest_dist, 1.7777777777777777)
    """
    if nx.is_connected(graph.nx_graph.to_undirected()):
        return nx.average_shortest_path_length(graph.nx_graph.to_undirected())
    msg = "Graph is not connected."
    raise RuntimeError(msg)
