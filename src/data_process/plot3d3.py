"""Interactive Plotly 3D plotting helpers for PyVAR3 measurement CSV files.

This module is import-safe: it does not load example data or open a plot window
until ``plot_interactive_currents`` or ``main`` is called.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go

LEGACY_X_COLUMN = "Gate_V"
LEGACY_Y_COLUMN = "Sub_V"
LEGACY_LINE_COLUMN = "Drain_V"
LEGACY_CURRENT_COLUMNS = ("Drain_I", "Gate_I", "Source_I", "Sub_I")


def _infer_plot_columns(columns: Sequence[str]) -> tuple[str, str, str, tuple[str, ...]]:
    """Infer plotting columns from either legacy or raw B1500 column names.

    Older ad-hoc CSVs used semantic names such as ``Gate_V``/``Drain_I``.
    GUI/exported CSVs keep the raw B1500 channel names such as
    ``A_I``, ``A_V``, ``B_V``, and ``C_V``. This helper supports both.
    """
    column_set = set(columns)
    legacy_voltage_columns = {LEGACY_X_COLUMN, LEGACY_Y_COLUMN, LEGACY_LINE_COLUMN}
    legacy_current_columns = tuple(column for column in LEGACY_CURRENT_COLUMNS if column in column_set)
    if legacy_voltage_columns <= column_set and legacy_current_columns:
        return LEGACY_X_COLUMN, LEGACY_Y_COLUMN, LEGACY_LINE_COLUMN, legacy_current_columns

    voltage_columns = tuple(column for column in columns if column.endswith("_V"))
    current_columns = tuple(column for column in columns if column.endswith("_I"))
    if len(voltage_columns) < 2:
        raise ValueError(
            "CSV needs at least two voltage columns for interactive plotting. "
            f"Found voltage columns: {list(voltage_columns)}"
        )
    if not current_columns:
        raise ValueError("CSV does not contain any current columns ending in '_I'")

    x_column = voltage_columns[0]
    y_column = voltage_columns[1]
    line_column = voltage_columns[2] if len(voltage_columns) >= 3 else y_column
    return x_column, y_column, line_column, current_columns


def plot_interactive_currents(
    csv_path: str | Path,
    *,
    x_column: str | None = None,
    y_column: str | None = None,
    line_column: str | None = None,
    current_columns: tuple[str, ...] | None = None,
) -> go.Figure:
    """Create an interactive 3D Plotly figure with current-column dropdowns.

    Args:
        csv_path: Measurement CSV to read. Metadata comment lines are ignored.
        x_column: Column to use as the x axis. Inferred when omitted.
        y_column: Column to use as the y axis. Inferred when omitted.
        line_column: Column used to draw multiple traces per y-axis slice. Inferred when omitted.
        current_columns: Current columns exposed in the dropdown. Inferred when omitted.

    Returns:
        A Plotly ``Figure``.
    """
    data = pd.read_csv(csv_path, comment="#")
    inferred_x, inferred_y, inferred_line, inferred_currents = _infer_plot_columns(tuple(data.columns))
    x_column = x_column or inferred_x
    y_column = y_column or inferred_y
    line_column = line_column or inferred_line
    current_columns = current_columns or inferred_currents

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
