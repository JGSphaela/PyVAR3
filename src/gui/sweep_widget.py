"""PySide6 widget for configuring a single sweep channel.

Provides input fields for channel number, mode, voltage range, start/stop voltages,
step count, current compliance, and power compliance.
"""

from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout


def _read_int(line_edit: QLineEdit, default=None):
    """Read an integer from a QLineEdit, returning default if empty."""
    text = line_edit.text().strip()
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        return default


def _read_float(line_edit: QLineEdit, default=None):
    """Read a float from a QLineEdit, returning default if empty."""
    text = line_edit.text().strip()
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


class SweepWidget(QWidget):
    """Widget for configuring a single sweep channel.

    Contains input fields for channel, mode, range, start/stop voltages,
    step count, current compliance, and power compliance.
    """

    def __init__(self, sweep_index):
        super().__init__()
        self.sweep_index = sweep_index

        sweep_label = QLabel(f"Sweep {sweep_index}: ")
        channel_label = QLabel("Channel: ")
        self.channel = QLineEdit()
        self.channel.setMaxLength(2)
        self.channel.setMaximumWidth(30)
        self.channel.setValidator(QIntValidator(1, 99))
        self.channel.setPlaceholderText("1")
        mode_label = QLabel("Mode: ")
        self.mode = QLineEdit()
        self.mode.setMaxLength(1)
        self.mode.setMaximumWidth(20)
        self.mode.setValidator(QIntValidator())
        self.mode.setPlaceholderText("1")
        range_label = QLabel("Range: ")
        self.range = QLineEdit()
        self.range.setMaxLength(1)
        self.range.setMaximumWidth(20)
        self.range.setValidator(QIntValidator())
        self.range.setPlaceholderText("0")
        start_label = QLabel("Start (V): ")
        self.start = QLineEdit()
        self.start.setMinimumWidth(50)
        self.start.setValidator(QDoubleValidator())
        self.start.setPlaceholderText("0.0")
        stop_label = QLabel("Stop (V): ")
        self.stop = QLineEdit()
        self.stop.setMinimumWidth(50)
        self.stop.setValidator(QDoubleValidator())
        self.stop.setPlaceholderText("0.0")
        step_label = QLabel("Step: ")
        self.step = QLineEdit()
        self.step.setMinimumWidth(40)
        self.step.setValidator(QIntValidator(1, 99999))
        self.step.setPlaceholderText("101")
        current_comp_label = QLabel("I Comp (A): ")
        self.current_comp = QLineEdit()
        self.current_comp.setMinimumWidth(50)
        self.current_comp.setValidator(QDoubleValidator())
        self.current_comp.setPlaceholderText("0.1")
        power_comp_label = QLabel("P Comp (W): ")
        self.power_comp = QLineEdit()
        self.power_comp.setMinimumWidth(50)
        self.power_comp.setValidator(QDoubleValidator())

        layout = QHBoxLayout()
        layout.addWidget(sweep_label)
        layout.addWidget(channel_label)
        layout.addWidget(self.channel)
        layout.addWidget(mode_label)
        layout.addWidget(self.mode)
        layout.addWidget(range_label)
        layout.addWidget(self.range)
        layout.addWidget(start_label)
        layout.addWidget(self.start)
        layout.addWidget(stop_label)
        layout.addWidget(self.stop)
        layout.addWidget(step_label)
        layout.addWidget(self.step)
        layout.addWidget(current_comp_label)
        layout.addWidget(self.current_comp)
        layout.addWidget(power_comp_label)
        layout.addWidget(self.power_comp)

        self.setLayout(layout)

    def get_values(self) -> dict:
        """Read all field values and return as a dict.

        Keys match SweepChannelConfig field names. Values are parsed to
        their proper types (int/float) or None if empty.
        """
        return {
            'channel': _read_int(self.channel, default=1),
            'mode': _read_int(self.mode, default=1),
            'range': _read_int(self.range, default=0),
            'start': _read_float(self.start, default=0.0),
            'stop': _read_float(self.stop, default=0.0),
            'step': _read_int(self.step, default=0),
            'current_compliance': _read_float(self.current_comp),
            'power_compliance': _read_float(self.power_comp),
            'comp_polarity': 0,
            'current_range': None,
        }

    def set_values(self, values: dict) -> None:
        """Populate fields from a dict (e.g. loaded from a profile).

        :param values: Dict with keys matching SweepChannelConfig field names.
        """
        def _set(line_edit: QLineEdit, key: str):
            val = values.get(key)
            line_edit.setText(str(val) if val is not None else "")

        _set(self.channel, 'channel')
        _set(self.mode, 'mode')
        _set(self.range, 'range')
        _set(self.start, 'start')
        _set(self.stop, 'stop')
        _set(self.step, 'step')
        _set(self.current_comp, 'current_compliance')
        _set(self.power_comp, 'power_compliance')


class SweepWidgetGroup(QWidget):
    """Container for multiple SweepWidget instances."""

    def __init__(self, sweep_count):
        super().__init__()

        self.widgets = []
        layout = QVBoxLayout()

        for i in range(1, sweep_count + 1):
            sweep_widget = SweepWidget(sweep_index=i)
            self.widgets.append(sweep_widget)
            layout.addWidget(sweep_widget)

        self.setLayout(layout)

