from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout


class SweepWidget(QWidget):
    def __init__(self, sweep_index):
        super().__init__()

        sweep_label = QLabel(f"Sweep {sweep_index}: ")
        channel_label = QLabel("Channel: ")
        self.channel = QLineEdit()
        self.channel.setMaxLength(1)
        self.channel.setMaximumWidth(20)
        self.channel.setValidator(QIntValidator())
        mode_label = QLabel("Mode: ")
        self.mode = QLineEdit()
        self.mode.setMaxLength(1)
        self.mode.setMaximumWidth(20)
        self.mode.setValidator(QIntValidator())
        range_label = QLabel("Range: ")
        self.range = QLineEdit()
        self.range.setMaxLength(1)
        self.range.setMaximumWidth(20)
        self.range.setValidator(QIntValidator())
        start_label = QLabel("Start: ")
        self.start = QLineEdit()
        self.start.setMinimumWidth(30)
        self.start.setValidator(QDoubleValidator())
        stop_label = QLabel("Stop: ")
        self.stop = QLineEdit()
        self.stop.setMinimumWidth(30)
        self.stop.setValidator(QDoubleValidator())
        step_label = QLabel("Step: ")
        self.step = QLineEdit()
        self.step.setMinimumWidth(30)
        self.step.setValidator(QIntValidator())
        current_comp_label = QLabel("Current Compliance: ")
        self.current_comp = QLineEdit()
        self.current_comp.setValidator(QDoubleValidator())
        power_comp_label = QLabel("Power Compliance: ")
        self.power_comp = QLineEdit()
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


class SweepWidgetGroup(QWidget):
    def __init__(self, sweep_count):
        super().__init__()

        layout = QVBoxLayout()

        for i in range(1, sweep_count + 1):
            sweep_widget = SweepWidget(sweep_index=i)
            layout.addWidget(sweep_widget)

        self.setLayout(layout)

