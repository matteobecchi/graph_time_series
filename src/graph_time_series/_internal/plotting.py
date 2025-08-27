"""Plotting functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy.typing import NDArray

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_global_obs(
    fig_path: Path | str,
    time_series: NDArray[np.float64],
    time: NDArray[np.float64] | None = None,
    y_label: str | None = None,
) -> None:
    """Plot a global quantity over time.

    Parameters:
        fig_path: location where to save the output Figure.

        time_series: the observable's values along time. Must be 1-dim.

        time: optional, the time frame list. Must have the same length as
            `time_series`.

        y_label: optional, the name of the observable to use as y-axis label.
    """
    if time_series.ndim != 1:
        msg = "Input array has wrong dimension."
        raise ValueError(msg)
    if fig_path is str:
        fig_path = Path(fig_path)

    time_array = (
        np.linspace(0, len(time_series), len(time_series))
        if time is None
        else time
    )

    fig, ax = plt.subplots()
    ax.plot(time_array, time_series, marker="o")
    ax.set_xlabel("Frame")
    if y_label is not None:
        ax.set_ylabel(y_label)
    fig.savefig(fig_path, dpi=600)
    plt.close()
