from PySide6.QtGui import QFont, Qt

from src.gui.sweep_widget import SweepWidgetGroup
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar


class SweepWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.sweep_count = 1
        self.sweep_widget = SweepWidgetGroup(sweep_count=self.sweep_count)

        running_status = QLabel("Ready")
        running_status.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        running_status.setStyleSheet("color: green")

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(50)
        progress_bar.setTextVisible(True)

        start_stop_button = QPushButton("Start")
        start_stop_button.setCheckable(True)

        self.add_sweep_button = QPushButton("Add Sweep Channel")
        self.add_sweep_button.clicked.connect(self.add_sweep_channel)

        h_layout = QHBoxLayout()
        h_layout.addWidget(running_status)
        h_layout.addWidget(progress_bar)
        # h_layout.addStretch()
        h_layout.addWidget(start_stop_button)

        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(h_layout)
        self.v_layout.addWidget(self.sweep_widget)
        self.v_layout.addWidget(self.add_sweep_button)

        h_layout.setContentsMargins(20, 0, 20, 0)

        self.setLayout(self.v_layout)

    def add_sweep_channel(self):
        self.sweep_count += 1

        # Remove the existing SweepWidgetGroup and add a new one with the updated sweep_count
        self.v_layout.removeWidget(self.sweep_widget)
        self.sweep_widget.deleteLater()  # Remove the old widget from the layout
        self.sweep_widget = SweepWidgetGroup(sweep_count=self.sweep_count)
        self.v_layout.insertWidget(1, self.sweep_widget)  # Insert the new widget back in the layout

        if self.sweep_count == 4:
            self.v_layout.removeWidget(self.add_sweep_button)
            self.add_sweep_button.deleteLater()
