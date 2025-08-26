"""Pytest for GraphTimeSeries class."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from graph_time_series import GraphTimeSeries, utilities

# ---------------- Fixtures ----------------


@pytest.fixture(scope="module")
def here() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="module")
def gts() -> GraphTimeSeries:
    n_frames = 100
    rs = np.arange(1, n_frames + 1)
    ad_mat_list = [
        utilities.random_adj_matrix_er(n=10, p=0.5, seed=int(rs[i]))
        for i in range(n_frames)
    ]
    return GraphTimeSeries(ad_mat_list)


# ---------------- Tests ----------------


def test_graph(gts: GraphTimeSeries) -> None:
    """Test initialization and methods for GraphTimeSeries class."""
    _ = gts.degree_over_time()
    _ = gts.clustering_over_time()
    _ = gts.diameter_over_time()
