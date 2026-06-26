"""Container widget for sweep configuration with add/remove sweep channels.

Shows a status bar (Ready/Running), progress bar, Start button, and allows
adding up to 4 sweep channels via SweepWidgetGroup.
"""

import logging

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                                 QPushButton, QProgressBar, QLineEdit, QGroupBox)

from src.gui.sweep_widget import SweepWidgetGroup
from src.measurement.config import MeasurementConfig, SweepChannelConfig

logger = logging.getLogger(__name__)

MAX_SWEEP_CHANNELS = 4


class SweepWindow(QWidget):
    """Main sweep configuration window.

    Provides sweep parameter inputs, GPIB device configuration,
    measurement start/stop controls, and progress display.
    """

    def __init__(self):
        super().__init__()

        self.sweep_count = 1

        # GPIB configuration
        gpib_group = QGroupBox("Instrument")
        gpib_layout = QHBoxLayout()
        gpib_layout.addWidget(QLabel("B1500 GPIB ID:"))
        self.gpib_id_input = QLineEdit("17")
        self.gpib_id_input.setMaximumWidth(40)
        gpib_layout.addWidget(self.gpib_id_input)
        gpib_layout.addStretch()
        gpib_group.setLayout(gpib_layout)

        # Sweep widgets
        self.sweep_widget = SweepWidgetGroup(sweep_count=self.sweep_count)

        # Status bar
        self.running_status = QLabel("Ready")
        self.running_status.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.running_status.setStyleSheet("color: green")

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v% (%p%)")

        # ETA label
        self.eta_label = QLabel("ETA: —")

        # Start/Stop button
        self.start_stop_button = QPushButton("Start Measurement")
        self.start_stop_button.setMinimumHeight(40)

        # Add sweep channel button
        self.add_sweep_button = QPushButton("+ Add Sweep Channel")
        self.add_sweep_button.clicked.connect(self.add_sweep_channel)

        # Layout
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.running_status)
        h_layout.addWidget(self.progress_bar)
        h_layout.addWidget(self.eta_label)
        h_layout.addWidget(self.start_stop_button)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(gpib_group)
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
        self.v_layout.insertWidget(2, self.sweep_widget)  # Insert after the h_layout

        if self.sweep_count >= MAX_SWEEP_CHANNELS:
            self.v_layout.removeWidget(self.add_sweep_button)
            self.add_sweep_button.deleteLater()

    def get_config(self) -> MeasurementConfig:
        """Build a MeasurementConfig from the current widget values.

        :return: MeasurementConfig populated with values from all sweep widgets.
        """
        try:
            gpib_id = int(self.gpib_id_input.text().strip())
        except (ValueError, AttributeError):
            gpib_id = 17

        channels = []
        for widget in self.sweep_widget.widgets:
            vals = widget.get_values()
            channels.append(SweepChannelConfig(**vals))

        return MeasurementConfig(
            gpib_device_id=gpib_id,
            sweep_channels=channels,
        )

    def set_config(self, config: MeasurementConfig) -> None:
        """Populate widgets from a MeasurementConfig.

        :param config: Configuration to load into the UI.
        """
        self.gpib_id_input.setText(str(config.gpib_device_id))

        # Rebuild sweep widgets to match config
        target_count = max(1, len(config.sweep_channels))
        while self.sweep_count < target_count:
            self.add_sweep_channel()

        for widget, ch_config in zip(self.sweep_widget.widgets, config.sweep_channels):
            widget.set_values({
                'channel': ch_config.channel,
                'mode': ch_config.mode,
                'range': ch_config.range,
                'start': ch_config.start,
                'stop': ch_config.stop,
                'step': ch_config.step,
                'current_compliance': ch_config.current_compliance,
                'power_compliance': ch_config.power_compliance,
            })

    def set_running(self, running: bool) -> None:
        """Update UI state for running/idle."""
        if running:
            self.running_status.setText("Running...")
            self.running_status.setStyleSheet("color: red")
            self.start_stop_button.setText("Abort")
            self.progress_bar.setValue(0)
        else:
            self.running_status.setText("Ready")
            self.running_status.setStyleSheet("color: green")
            self.start_stop_button.setText("Start Measurement")
            self.eta_label.setText("ETA: —")

    def update_progress(self, current: int, total: int, eta_str: str) -> None:
        """Update the progress bar and ETA label.

        :param current: Current step number.
        :param total: Total number of steps.
        :param eta_str: Formatted ETA string.
        """
        if total > 0:
            pct = int(current / total * 100)
            self.progress_bar.setValue(pct)
            self.progress_bar.setFormat(f"{current}/{total} ({pct}%)")
        self.eta_label.setText(f"ETA: {eta_str}")
