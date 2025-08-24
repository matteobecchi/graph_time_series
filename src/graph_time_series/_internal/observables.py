"""Compute observables on the graphs."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph


import networkx as nx


def degree(graph: Graph) -> dict[int, float]:
    """Return a dict of node degrees (weighted if graph is weighted).

    Parameters
    ----------
    graph: graph_time_series.Graph
        The graph we want to compute the nodes' degrees.
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
