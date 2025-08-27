Computing observables on a graph time-series
============================================

This recipe explains how to compute observables from a
:class:`.GraphTimeSeries` object.

We can create a graph time-series by starting from a random graph created
with the function :class:`.utilities.random_adj_matrix_ba()`, and defining
some update function.

.. testcode:: recipe1-test

    from graph_time_series.utilities import random_adj_matrix_ba
    import numpy as np

    n_nodes = 10
    mat_0 = random_adj_matrix_ba(
        n=n_nodes,  # Number of nodes
        m=2,        # Barabasi-Albert graph parameter
        seed=42,
    )

    def update_ad_matrix(
        mat_0: np.ndarray,
        rng: np.random.Generator,
    ) -> np.ndarray:
        """Updates the matrix by randomly swapping one edge."""
        mat_1 = np.copy(mat_0)
        i, j = rng.integers(0, n_nodes, size=2)
        if mat_1[i][j] == 0:
            mat_1[i][j] = 1
        else:
            mat_1[i][j] = 0
        return mat_1

    list_of_ad_matrices = [mat_0]
    n_frames = 100
    rng = np.random.default_rng(seed=42)
    for _ in range(n_frames - 1):
        list_of_ad_matrices.append(
            update_ad_matrix(list_of_ad_matrices[-1], rng)
        )

Now we can initialize the :class:`.GraphTimeSeries` object:

.. testcode:: recipe1-test

    from graph_time_series import GraphTimeSeries

    gts = GraphTimeSeries(list_of_ad_matrices)

and we can use the methods of the :class:`.GraphTimeSeries` class to compute
observables along the time-series, and then plot them as a function of time.

.. testcode:: recipe1-test

    average_node_degree = gts.degree_over_time()
    average_node_cl_coeff = gts.clustering_over_time()
    graph_diameter = gts.diameter_over_time()

These quantities can be easily plotted using the `plotting` module:

.. testcode:: recipe1-test

    from pathlib import Path
    from graph_time_series.plotting import plot_global_obs

    output_path = Path("source/_static")
    plot_global_obs(
        fig_path=Path(output_path / "Fig1_1.png"),
        time_series=average_node_degree,
        y_label="Average degree",
    )
    plot_global_obs(
        fig_path=Path(output_path / "Fig1_2.png"),
        time_series=average_node_cl_coeff,
        y_label="Average clustering coeff.",
    )
    plot_global_obs(
        fig_path=Path(output_path / "Fig1_3.png"),
        time_series=graph_diameter,
        y_label="Graph's diameter",
    )

.. testcode:: recipe1-test
    :hide:

    assert len(list_of_ad_matrices) == 100
