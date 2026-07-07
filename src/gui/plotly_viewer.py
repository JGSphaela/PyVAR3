"""PyQt6 window for displaying interactive Plotly measurement figures."""

from __future__ import annotations

import plotly.io as pio
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from src.data_process.plot3d3 import plot_interactive_currents


def create_plot(csv_path: str) -> str:
    """Create the Plotly HTML for a measurement CSV file."""
    fig = plot_interactive_currents(csv_path)
    return pio.to_html(fig)


class PlotlyViewer(QMainWindow):
    def __init__(self, csv_path: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PyVAR3 3D Plot")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setHtml(create_plot(csv_path))
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
