# src/gpib/gpib_communication.py

import pyvisa


class GPIBCommunication:
    def __init__(self):
        """
        GPIB communication class to communicate with GPIB device.

        """
        self.device = None
        try:
            self.rm = pyvisa.ResourceManager()
            print("ResourceManager initialized successfully")
        except ValueError as e:
            self.rm = None
            self.error_message = f"Failed to initialize ResourceManager: {e}"
            print(self.error_message)

    def connect_device(self, address: str) -> None:
        """
        Try to connect to a GPIB device using the given address.

        :param address: GPIB address to connect to.
        :return:
        """
        if not self.rm:
            print("ResourceManager not initialized.")
            return

        try:
            self.device = self.rm.open_resource(address)
            print(f"Connected to {address}")
        except pyvisa.VisaIOError as e:
            self.device = None
            self.error_message = f"Failed to connect to {address}: {e}"
            print(self.error_message)

    def send_command(self, command: str) -> None:
        """
        Send a command to the GPIB device.

        :param command: The command to send.
        """
        if self.device:
            try:
                self.device.write(command)
                print(f"Command sent: {command}")
            except pyvisa.VisaIOError as e:
                self.error_message = f"Failed to send command: {e}"
                print(self.error_message)
        else:
            print("No device connected.")

    def read_response(self) -> str:
        """
        Read response from the GPIB device.

        :return:
        """
        if self.device:
            try:
                response = self.device.read()
                print(f"Response: {response}")
                return response
            except pyvisa.VisaIOError as e:
                self.error_message = f"Failed to read response: {e}"
                print(self.error_message)
        else:
            print("No device connected.")

    def read_ascii(self) -> str:
        """
        Read ASCII response from the GPIB device.

        :return:
        """
        if self.device:
            try:
                response = self.device.read_ascii_values()
                print(f"Response: {response}")
                return response
            except pyvisa.VisaIOError as e:
                self.error_message = f"Failed to read response: {e}"
                print(self.error_message)
        else:
            print("No device connected.")
