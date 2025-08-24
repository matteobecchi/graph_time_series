"""Class for graph time-series."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from graph_time_series import observables

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray

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
    def observable_over_time(self, fn: Callable[[Graph], Any]) -> list[Any]:
        """Apply an observable function to each graph in the series.

        Parameters
        ----------
        fn :
            A function that takes a Graph and returns an observable.

        Returns:
        -------
        list
            list of observable values, one per timestep.
        """
        return [fn(g) for g in self.graphs]

    def clustering_over_time(self) -> list[dict[int, float]]:
        """Return clustering coefficients for each graph in the series."""
        return self.observable_over_time(observables.clustering)

    def degree_over_time(self) -> list[dict[int, float]]:
        """Return node degrees for each graph in the series."""
        return self.observable_over_time(observables.degree)

    def diameter_over_time(self) -> list[float]:
        """Return graph diameters for each graph in the series."""
        return self.observable_over_time(observables.diameter)
