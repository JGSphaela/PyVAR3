import logging
import sys

from PySide6.QtWidgets import QApplication

try:
    from src.gui.main_window_pyside import MainWindow
except ModuleNotFoundError:
    # Allow direct execution: python src/main.py
    from gui.main_window_pyside import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)


def main():
    """Entry point for PyVAR3 application."""
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
