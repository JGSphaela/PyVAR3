import logging
import os
import sys

from PySide6.QtWidgets import QApplication

try:
    from src.gui.main_window_pyside import MainWindow
except ModuleNotFoundError:
    # Allow direct execution: python src/main.py from repo root.
    # Add repo root to sys.path so 'src.*' imports resolve inside the GUI modules.
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from src.gui.main_window_pyside import MainWindow

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
