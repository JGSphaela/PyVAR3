"""Interactive Plotly 3D plotting helpers for PyVAR3 measurement CSV files.

This module is import-safe: it does not load example data or open a plot window
until ``plot_interactive_currents`` or ``main`` is called.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_interactive_currents(
    csv_path: str | Path,
    *,
    x_column: str = "Gate_V",
    y_column: str = "Sub_V",
    line_column: str = "Drain_V",
    current_columns: tuple[str, ...] = ("Drain_I", "Gate_I", "Source_I", "Sub_I"),
) -> go.Figure:
    """Create an interactive 3D Plotly figure with current-column dropdowns.

    Args:
        csv_path: Measurement CSV to read. Metadata comment lines are ignored.
        x_column: Column to use as the x axis.
        y_column: Column to use as the y axis.
        line_column: Column used to draw multiple traces per y-axis slice.
        current_columns: Current columns exposed in the dropdown.

    Returns:
        A Plotly ``Figure``.
    """
    data = pd.read_csv(csv_path, comment="#")
    available_currents = tuple(column for column in current_columns if column in data.columns)
    missing = {x_column, y_column, line_column} - set(data.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")
    if not available_currents:
        raise ValueError("CSV does not contain any requested current columns")

    y_values = data[y_column].unique()
    line_values = data[line_column].unique()
    colors = plt.cm.viridis(np.linspace(0, 1, max(len(y_values), 1)))

    fig = go.Figure()
    for current_column in available_currents:
        for y_idx, y_value in enumerate(y_values):
            y_data = data[data[y_column] == y_value]
            for line_value in line_values:
                line_data = y_data[y_data[line_column] == line_value]
                rgba = colors[y_idx]
                fig.add_trace(go.Scatter3d(
                    x=line_data[x_column],
                    y=[y_value] * len(line_data),
                    z=line_data[current_column],
                    mode="lines",
                    name=f"{current_column} ({line_column}={line_value})",
                    line=dict(color=f"rgba({rgba[0] * 255},{rgba[1] * 255},{rgba[2] * 255},1)"),
                    visible=(current_column == available_currents[0]),
                    hovertemplate=(
                        f"{x_column}: %{{x}}<br>{y_column}: %{{y}}<br>"
                        f"{current_column}: %{{z}}<br>{line_column}: {line_value}<extra></extra>"
                    ),
                ))

    buttons = []
    for current_column in available_currents:
        visible = [trace.name.split(" ")[0] == current_column for trace in fig.data]
        buttons.append(dict(
            label=current_column,
            method="update",
            args=[
                {"visible": visible},
                {
                    "title": f"3D plot of {current_column} vs {x_column} and {y_column}",
                    "scene": {
                        "xaxis": {"title": x_column},
                        "yaxis": {"title": y_column},
                        "zaxis": {"title": current_column},
                    },
                },
            ],
        ))

    fig.update_layout(
        updatemenus=[
            dict(buttons=buttons, direction="down", showactive=True, xanchor="left", yanchor="top"),
            dict(
                buttons=[
                    dict(label="Linear Z", method="relayout", args=[{"scene.zaxis.type": "linear"}]),
                    dict(label="Log Z", method="relayout", args=[{"scene.zaxis.type": "log"}]),
                ],
                direction="down",
                showactive=True,
                xanchor="right",
                yanchor="top",
            ),
        ],
        scene=dict(
            xaxis=dict(title=x_column),
            yaxis=dict(title=y_column),
            zaxis=dict(title=available_currents[0]),
        ),
        title=f"3D plot of {available_currents[0]} vs {x_column} and {y_column}",
    )
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot interactive PyVAR3 current traces with Plotly.")
    parser.add_argument("csv_path", help="Measurement CSV to plot")
    args = parser.parse_args()

    plot_interactive_currents(args.csv_path).show()


if __name__ == "__main__":
    main()
