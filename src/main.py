import sys
from PySide6.QtWidgets import QApplication
from gui.main_window_pyside import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.show()

    app.exec()
