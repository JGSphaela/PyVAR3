import sys

from PySide6.QtWidgets import QApplication

from src.gui.sweep_window import SweepWindow

app = QApplication(sys.argv)

windows = SweepWindow()
windows.show()

app.exec()