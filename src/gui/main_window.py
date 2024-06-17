from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox
from PyQt6.QtCore import Qt
from src.gpib.gpib_communication import GPIBCommunication
from src.utils.helper import load_translations
from src.gui.plotly_viewer import PlotlyViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language_code = "en"  # Default language
        self.translations = load_translations(self.language_code)
        self.initUI()
        self.gpib_comm = GPIBCommunication()
        self.check_gpib_init()

    def initUI(self):
        self.setWindowTitle("GPIB Communication Tool")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.setup_tab = QWidget()
        self.measurement_tab = QWidget()
        self.result_tab = QWidget()
        self.console_tab = QWidget()

        self.tabs.addTab(self.setup_tab, self.translations["setup_tab"])
        self.tabs.addTab(self.measurement_tab, self.translations["measurement_tab"])
        self.tabs.addTab(self.result_tab, self.translations["result_tab"])
        self.tabs.addTab(self.console_tab, self.translations["console_tab"])

        self.init_setup_tab()
        self.init_result_tab()
        self.init_language_selection()

    def init_setup_tab(self):
        layout = QVBoxLayout()

        self.test_button = QPushButton(self.translations["test_connection_button"])
        self.test_button.clicked.connect(self.test_pyvisa)
        layout.addWidget(self.test_button)

        self.setup_tab.setLayout(layout)

    def init_result_tab(self):
        layout = QVBoxLayout()

        self.plot_button = QPushButton("Show 3D Plot")
        self.plot_button.clicked.connect(self.show_plotly_viewer)
        layout.addWidget(self.plot_button)

        self.result_tab.setLayout(layout)

    def init_language_selection(self):
        language_label = QLabel(self.translations["language_label"])
        language_dropdown = QComboBox()
        language_dropdown.addItems(["English", "日本語"])
        language_dropdown.currentIndexChanged.connect(self.change_language)

        self.tabs.setCornerWidget(language_label, Qt.Corner.TopLeftCorner)
        self.tabs.setCornerWidget(language_dropdown, Qt.Corner.TopRightCorner)

    def change_language(self, index):
        if index == 0:
            self.language_code = "en"
        else:
            self.language_code = "ja"
        self.translations = load_translations(self.language_code)
        self.update_ui_texts()

    def update_ui_texts(self):
        self.tabs.setTabText(0, self.translations["setup_tab"])
        self.tabs.setTabText(1, self.translations["measurement_tab"])
        self.tabs.setTabText(2, self.translations["result_tab"])
        self.tabs.setTabText(3, self.translations["console_tab"])
        self.test_button.setText(self.translations["test_connection_button"])
        self.plot_button.setText("Show 3D Plot")

    def check_gpib_init(self):
        if not self.gpib_comm.rm:
            self.show_error(self.gpib_comm.error_message)

    def test_pyvisa(self):
        if not self.gpib_comm.rm:
            self.show_error(self.gpib_comm.error_message)
            return

        try:
            self.gpib_comm.connect_device("GPIB0::1::INSTR")  # Replace with your actual GPIB address
            self.gpib_comm.send_command("*IDN?")
            response = self.gpib_comm.read_response()
            QMessageBox.information(self, "Success", self.translations["success_message"])
        except Exception as e:
            self.show_error(str(e))

    def show_plotly_viewer(self):
        self.plotly_viewer = PlotlyViewer(self)
        self.plotly_viewer.show()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)