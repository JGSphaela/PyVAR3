from PyQt6.QtWidgets import QMainWindow, QPushButton, QMessageBox
from src.gpib.gpib_communication import GPIBCommunication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyVAR3: A Minimal GPIB Measurement Tool")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()
        self.gpib_comm = GPIBCommunication()
        self.check_gpib_init()

    def initUI(self):
        self.test_button = QPushButton("Test PyVISA", self)
        self.test_button.clicked.connect(self.test_pyvisa)
        self.test_button.setGeometry(100, 100, 200, 40)

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
            QMessageBox.information(self, "Success", response)
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
