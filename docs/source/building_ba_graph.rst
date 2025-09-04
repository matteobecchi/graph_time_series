Iterative construction of Barabàsi-Albert graph
===============================================

In this recipe, we build a scale-free Barabàsi-Albert (BA) graph with an
iterative process, which is stored in a :class:`.GraphTimeSeries` so that
all the observables can me easily measured during the construction.

We start creating the seed, a small connected graph:

.. testcode:: recipe2-test

    import numpy as np
    from graph_time_series.utilities import random_adj_matrix_er
    from graph_time_series import Graph

    adj_0 = random_adj_matrix_er(n=10, p=0.8, seed=42)
    graph_0 = Graph(adj_0)

To Be Continued

.. testcode:: recipe2-test
    :hide:

    assert len(adj_0) == 10
