"""The single graph class."""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from numpy.typing import NDArray


class Graph:
    """Wrapper around a nx graph representing exchanges at one timestep."""

    def __init__(
        self,
        adjacency_matrix: NDArray[np.float64],
        directed: bool = False,
    ) -> None:
        """Initialize a graph from an adjacency matrix.

        Parameters
        ----------
        adjacency_matrix :
            The adjacency matrix representing exchanges between nodes.
        directed :
            Whether the graph is directed.
        """
        self.directed = directed
        self.nx_graph = nx.DiGraph() if directed else nx.Graph()
        self._build_graph(adjacency_matrix)

    def _build_graph(self, adjacency_matrix: NDArray[np.float64]) -> None:
        """Builds the networkx graph from the adjacency matrix."""
        for (i, j), weight in np.ndenumerate(adjacency_matrix):
            if weight != 0:
                self.nx_graph.add_edge(i, j, weight=weight)

    # --- Graph observables ---
    def degree(self) -> dict:
        """Return a dict of node degrees (weighted if graph is weighted)."""
        return dict(self.nx_graph.degree(weight="weight"))

    def clustering(self) -> dict:
        """Return clustering coefficients per node."""
        if self.directed:
            return nx.clustering(
                self.nx_graph.to_undirected(), weight="weight"
            )
        return nx.clustering(self.nx_graph, weight="weight")

    def diameter(self) -> float:
        """Return the diameter of the graph."""
        if nx.is_connected(self.nx_graph.to_undirected()):
            return nx.diameter(self.nx_graph.to_undirected())
        return float("inf")  # or raise an exception

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
