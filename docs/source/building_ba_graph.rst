Iterative construction of Barabàsi-Albert graph
===============================================

In this recipe, we build a scale-free Barabàsi-Albert (BA) graph with an
iterative process, which is stored in a :class:`.GraphTimeSeries` so that
all the observables can me easily measured during the construction.

We start creating the seed, a small connected graph, of size m0:

.. testcode:: recipe2-test

    import numpy as np
    from graph_time_series.utilities import random_adj_matrix_er

    m_0 = 10
    adj_0 = random_adj_matrix_er(n=m_0, p=0.8, seed=42)

Then, we start an iterative process. At each step, a node is added to the
existing graph. A number m of pre-esisting nodes is randomly drawn and
ad edge between the new node and the selected ones is added with a probability
proportional to the number of edges the node alredy has:

.. testcode:: recipe2-test

    m = 5  # The BA parameter, m <= m_0
    n_steps = 200
    list_of_adj = [adj_0]
    for _ in range(n_steps):
        sum_k = np.sum(list_of_adj[-1]) / 2
        n_nodes = len(list_of_adj[-1]) + 1
        new_adj = np.zeros((n_nodes, n_nodes))
        new_adj[:-1, :-1] = list_of_adj[-1]
        rndint = np.random.randint(low=0, high=n_nodes - 1, size=m)
        for i in rndint:
            p = np.sum(list_of_adj[-1][i]) / sum_k
            if np.random.uniform() < p:
                new_adj[i, n_nodes - 1] = 1
                new_adj[n_nodes - 1, i] = 1
        list_of_adj.append(new_adj)

Now, with this list of adjacency matrices we can build a
:class:`.GraphTimeSeries` and use its methods to compute and plot useful
observables:

.. testcode:: recipe2-test
    :hide:

    from  graph_time_series import GraphTimeSeries, plotting

    gts = GraphTimeSeries(list_of_adj)

    number_of_nodes = gts.n_nodes_over_time()
    plotting.plot_global_obs(
        fig_path="source/_static/Fig2_1.png",
        time_series=number_of_nodes,
        y_label="Number of nodes",
    )

    average_degree = gts.degree_over_time()
    plotting.plot_global_obs(
        fig_path="source/_static/Fig2_2.png",
        time_series=average_degree,
        y_label="Average degree",
    )

    clustering_coeff = gts.clustering_over_time()
    plotting.plot_global_obs(
        fig_path="source/_static/Fig2_3.png",
        time_series=clustering_coeff,
        y_label="Clustering coefficient",
    )

    diameter = gts.diameter_over_time()
    plotting.plot_global_obs(
        fig_path="source/_static/Fig2_4.png",
        time_series=diameter,
        y_label="Diameter",
    )


.. testcode:: recipe2-test
    :hide:

    assert len(list_of_adj) == 201
    assert len(list_of_adj[-1]) == 210
