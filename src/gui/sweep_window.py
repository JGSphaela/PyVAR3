from PySide6.QtGui import QFont, Qt

from src.gui.sweep_widget import SweepWidgetGroup
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar


class SweepWindow(QWidget):
    def __init__(self):
        super().__init__()

        sweep_widget = SweepWidgetGroup(4)

        running_status = QLabel("Ready")
        running_status.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        running_status.setStyleSheet("color: green")

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(True)

        start_stop_button = QPushButton("Start")

        h_layout = QHBoxLayout()
        h_layout.addWidget(running_status)
        h_layout.addWidget(progress_bar)
        # h_layout.addStretch()
        h_layout.addWidget(start_stop_button)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(sweep_widget)

        h_layout.setContentsMargins(20, 0, 20, 0)

        self.setLayout(v_layout)