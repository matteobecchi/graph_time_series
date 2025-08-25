"""Compute observables on the graphs."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph


import networkx as nx


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

    Parameters
    ----------
    graph: graph_time_series.Graph
        The graph we want to compute the nodes' degrees.
    """
    return dict(nx.clustering(graph.nx_graph.to_undirected(), weight="weight"))


def diameter(graph: Graph) -> int:
    """Return the diameter of the graph.

    Parameters
    ----------
    graph: graph_time_series.Graph
        The graph we want to compute the nodes' degrees.
    """
    if nx.is_connected(graph.nx_graph.to_undirected()):
        return nx.diameter(graph.nx_graph.to_undirected())
    msg = "Graph is not connected."
    raise RuntimeError(msg)
