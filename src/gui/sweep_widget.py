from PySide6.QtWidgets import QWidget, QHBoxLayout


class SweepWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
