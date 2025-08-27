"""Class for graph time-series."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from graph_time_series import observables

if TYPE_CHECKING:
    from numpy.typing import NDArray

import numpy as np

from .graph import Graph


class GraphTimeSeries:
    """A time-series of graphs.

    Attributes:
    -----------
    matrices :
        A list of adjacency matrices (one per timestep).
    directed :
        Whether graphs are directed.
    """

    def __init__(
        self,
        matrices: list[NDArray[np.float64]],
        directed: bool = False,
    ) -> None:
        """Initialize the time-series from a list of adjacency matrices."""
        self.directed = directed
        self.graphs: list[Graph] = [
            Graph(m, directed=directed) for m in matrices
        ]

    def __getitem__(self, idx: int) -> Graph:
        """Return the Graph at index `idx`."""
        return self.graphs[idx]

    def __len__(self) -> int:
        """Return the number of timesteps in the series."""
        return len(self.graphs)

    # --- Observables over time ---
    def local_observable_over_time(
        self, fn: Callable[[Graph], Any]
    ) -> NDArray[np.float64]:
        """Apply a local observable function to each graph in the series.

        Parameters
        ----------
        fn :
            A function that takes a Graph and returns an observable.

        Returns:
        -------
        list
            list of average values, one per timestep.
        """
        list_of_dicts = [fn(g) for g in self.graphs]
        tmp_list = [
            np.mean([float(v) for v in d.values()]) for d in list_of_dicts
        ]
        return np.array(tmp_list)

    def global_observable_over_time(
        self, fn: Callable[[Graph], Any]
    ) -> NDArray[np.float64]:
        """Apply a global observable function to each graph in the series.

        Parameters
        ----------
        fn :
            A function that takes a Graph and returns an observable.

        Returns:
        -------
        list
            list of values, one per timestep.
        """
        return np.array([fn(g) for g in self.graphs])

    def clustering_over_time(self) -> NDArray[np.float64]:
        """Return clustering coefficients for each graph in the series."""
        return self.local_observable_over_time(observables.clustering)

    def degree_over_time(self) -> NDArray[np.float64]:
        """Return node degrees for each graph in the series."""
        return self.local_observable_over_time(observables.degree)

    def n_nodes_over_time(self) -> NDArray[np.float64]:
        """Return the number of nodes for each graph in the series."""
        return self.local_observable_over_time(observables.n_nodes)

    def diameter_over_time(self) -> NDArray[np.float64]:
        """Return graph diameters for each graph in the series."""
        return self.global_observable_over_time(observables.diameter)

    def aver_shortest_dist_over_time(self) -> NDArray[np.float64]:
        """Return average shortest distance for each graph in the series."""
        return self.global_observable_over_time(observables.average_distance)
