from PySide6.QtWidgets import QMainWindow, QStatusBar


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

        # Status Bar
        self.setStatusBar(QStatusBar(self))

    def quit_app(self):
        self.app.quit()