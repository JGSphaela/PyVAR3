"""Matplotlib 3D plotting helpers for PyVAR3 measurement CSV files.

This module is import-safe: it does not load example data or open a plot window
until ``plot_3d`` or ``main`` is called.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import ScalarFormatter


def plot_3d(
    csv_path: str | Path,
    *,
    x_column: str = "Gate_V",
    y_column: str = "Sub_V",
    z_column: str = "Drain_I",
    line_column: str = "Drain_V",
):
    """Plot a 3D measurement surface as grouped line traces.

    Args:
        csv_path: Measurement CSV to read. Metadata comment lines are ignored.
        x_column: Column to use as the x axis.
        y_column: Column to use as the y axis.
        z_column: Column to use as the z axis.
        line_column: Column used to draw multiple traces per y-axis slice.

    Returns:
        The Matplotlib ``(fig, ax)`` pair.
    """
    data = pd.read_csv(csv_path, comment="#")
    missing = {x_column, y_column, z_column, line_column} - set(data.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

    y_values = data[y_column].unique()
    line_values = data[line_column].unique()

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    colors = plt.cm.viridis(np.linspace(0, 1, max(len(y_values), 1)))

    for y_idx, y_value in enumerate(y_values):
        y_data = data[data[y_column] == y_value]
        for line_value in line_values:
            line_data = y_data[y_data[line_column] == line_value]
            ax.plot(
                line_data[x_column],
                [y_value] * len(line_data),
                line_data[z_column],
                color=colors[y_idx],
            )

    ax.view_init(elev=20, azim=135)
    ax.zaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.zaxis.get_major_formatter().set_powerlimits((0, 0))
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_zlabel(z_column)
    ax.set_title(f"3D plot of {z_column} vs {x_column} and {y_column}")
    return fig, ax


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot a 3D PyVAR3 measurement CSV with Matplotlib.")
    parser.add_argument("csv_path", help="Measurement CSV to plot")
    args = parser.parse_args()

    plot_3d(args.csv_path)
    plt.show()


if __name__ == "__main__":
    main()
