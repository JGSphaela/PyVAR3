from PySide6.QtWidgets import QMainWindow, QStatusBar, QMessageBox

from src.gui import sweep_window
from src.gui.sweep_window import SweepWindow

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.setWindowTitle("PyVAR3 GUI")
        self.menuBar().setNativeMenuBar(False)  # only needed on Mac
        # self.setGeometry(100, 100, 800, 600)  # Set the window size to 800x600

        # Menubar
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.app.quit)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")
        about_menu = help_menu.addAction("About")
        about_menu.triggered.connect(self.about_app)

        # Status Bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Waiting for Measurement")

        self.sweep_window = SweepWindow()
        self.setCentralWidget(self.sweep_window)

    def quit_app(self):
        self.app.quit()

    def about_app(self):
        ret = QMessageBox.about(self, "About", "PyVAR3 GUI")