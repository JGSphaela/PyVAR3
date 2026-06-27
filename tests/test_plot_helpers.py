"""Regression tests for import-safe plotting helpers."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")


def test_plot_modules_import_without_example_data():
    """Plot modules should not read hard-coded CSV files at import time."""
    import src.data_process.plot2d  # noqa: F401
    import src.data_process.plot3d  # noqa: F401
    import src.data_process.plot3d2  # noqa: F401
    import src.data_process.plot3d3  # noqa: F401


def test_plot_helpers_accept_explicit_csv_path(tmp_path):
    csv_path = tmp_path / "measurement.csv"
    csv_path.write_text(
        "Gate_V,Sub_V,Drain_V,Drain_I,Gate_I,Source_I,Sub_I\n"
        "0.0,0.0,0.0,1e-9,2e-12,0,0\n"
        "0.1,0.0,0.0,2e-9,3e-12,0,0\n"
        "0.0,0.1,0.0,1.5e-9,2.5e-12,0,0\n"
        "0.1,0.1,0.0,2.5e-9,3.5e-12,0,0\n"
    )

    from src.data_process.plot2d import plot_2d
    from src.data_process.plot3d import plot_3d
    from src.data_process.plot3d2 import plot_3d_plotly
    from src.data_process.plot3d3 import plot_interactive_currents

    fig_2d, ax_2d = plot_2d(csv_path, drain_index=0)
    fig_3d, ax_3d = plot_3d(csv_path)
    plotly_fig = plot_3d_plotly(csv_path)
    interactive_fig = plot_interactive_currents(csv_path)

    assert fig_2d is not None
    assert ax_2d is not None
    assert fig_3d is not None
    assert ax_3d is not None
    assert len(plotly_fig.data) > 0
    assert len(interactive_fig.data) > 0
