"""2D plotting helpers for PyVAR3 measurement CSV files.

This module is import-safe: it does not load example data or open a plot window
until ``plot_2d`` or ``main`` is called.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import ScalarFormatter


def plot_2d(
    csv_path: str | Path,
    *,
    drain_index: int = 30,
    x_column: str = "Gate_V",
    y_column: str = "Drain_I",
    drain_column: str = "Drain_V",
    group_column: str = "Sub_V",
):
    """Plot a 2D IV curve grouped by substrate voltage.

    Args:
        csv_path: Measurement CSV to read. Metadata comment lines are ignored.
        drain_index: Index into the unique drain-voltage list to plot.
        x_column: Column to use as the x axis.
        y_column: Column to use as the y axis.
        drain_column: Column used to select one drain-voltage slice.
        group_column: Column used to draw one line per group.

    Returns:
        The Matplotlib ``(fig, ax)`` pair.
    """
    data = pd.read_csv(csv_path, comment="#")
    missing = {x_column, y_column, drain_column, group_column} - set(data.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

    drain_values = data[drain_column].unique()
    if len(drain_values) == 0:
        raise ValueError(f"CSV contains no values in {drain_column!r}")
    if drain_index < 0 or drain_index >= len(drain_values):
        raise IndexError(
            f"drain_index {drain_index} is outside available range 0..{len(drain_values) - 1}"
        )

    selected_drain = drain_values[drain_index]
    drain_slice = data[data[drain_column] == selected_drain]
    group_values = drain_slice[group_column].unique()

    colors = plt.cm.viridis(np.linspace(0, 1, len(group_values)))
    fig, ax = plt.subplots()

    for idx, group_value in enumerate(group_values):
        group_data = drain_slice[drain_slice[group_column] == group_value]
        ax.plot(
            group_data[x_column],
            group_data[y_column],
            color=colors[idx],
            label=f"{group_column}={group_value}",
        )

    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.yaxis.get_major_formatter().set_powerlimits((0, 0))
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(f"{y_column} vs {x_column} when {drain_column} = {selected_drain}")
    ax.legend(loc="best")
    return fig, ax


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot a 2D PyVAR3 measurement CSV.")
    parser.add_argument("csv_path", help="Measurement CSV to plot")
    parser.add_argument("--drain-index", type=int, default=30)
    args = parser.parse_args()

    plot_2d(args.csv_path, drain_index=args.drain_index)
    plt.show()


if __name__ == "__main__":
    main()
