"""The single graph class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from numpy.typing import NDArray

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from . import observables


class Graph:
    """Wrapper around a nx graph representing exchanges at one timestep.

    Attributes:
    -----------
    adjacency_matrix :
        The adjacency matrix representing exchanges between nodes.
    directed :
        Whether the graph is directed.
    """

    def __init__(
        self,
        adjacency_matrix: NDArray[np.float64],
        directed: bool = False,
    ) -> None:
        """Initialize a graph from an adjacency matrix."""
        self.directed = directed
        self.nx_graph = nx.DiGraph() if directed else nx.Graph()
        self._build_graph(adjacency_matrix)

    def _build_graph(self, adjacency_matrix: NDArray[np.float64]) -> None:
        """Builds the networkx graph from the adjacency matrix."""
        for (i, j), weight in np.ndenumerate(adjacency_matrix):
            if weight != 0:
                self.nx_graph.add_edge(i, j, weight=weight)

    # --- Graph observables ---
    def n_nodes(self) -> int:
        """Return the number of nodes."""
        return observables.n_nodes(self)

    def degree(self) -> dict[Any, float]:
        """Return a dict of node degrees (weighted if graph is weighted)."""
        return observables.degree(self)

    def clustering(self) -> dict[Any, float]:
        """Return clustering coefficients per node."""
        return observables.clustering(self)

    def diameter(self) -> int:
        """Return the diameter of the graph."""
        return observables.diameter(self)

    def average_distance(self) -> float:
        """Return the average shortest distance between nodes."""
        return observables.average_distance(self)

    # --- Plotting ---
    def plot(self, **kwargs: object) -> None:
        """Simple matplotlib plot of the graph."""
        pos = nx.spring_layout(self.nx_graph)
        nx.draw(self.nx_graph, pos, with_labels=True, **kwargs)
        edge_labels = nx.get_edge_attributes(self.nx_graph, "weight")
        nx.draw_networkx_edge_labels(
            self.nx_graph, pos, edge_labels=edge_labels
        )
        plt.show()
