# src/gpib/gpib_communication.py

import logging

import pyvisa

from src.gpib.exceptions import DeviceNotConnectedError, GPIBError

logger = logging.getLogger(__name__)


class GPIBCommunication:
    def __init__(self):
        """
        GPIB communication class to communicate with GPIB device.
        """
        self.device = None
        try:
            self.rm = pyvisa.ResourceManager()
            logger.info("ResourceManager initialized successfully")
        except ValueError as e:
            self.rm = None
            self.error_message = f"Failed to initialize ResourceManager: {e}"
            logger.error(self.error_message)

    def connect_device(self, address: str) -> None:
        """
        Try to connect to a GPIB device using the given address.

        :param address: GPIB address to connect to.
        :raises DeviceNotConnectedError: If the ResourceManager is not initialized.
        :raises GPIBError: If connection to the device fails.
        """
        if not self.rm:
            raise DeviceNotConnectedError("ResourceManager not initialized.")

        try:
            self.device = self.rm.open_resource(address)
            self.device.timeout = None
            logger.info(f"Connected to {address}")
        except pyvisa.VisaIOError as e:
            self.device = None
            raise GPIBError(f"Failed to connect to {address}: {e}") from e

    def send_command(self, command: str) -> None:
        """
        Send a command to the GPIB device.

        :param command: The command to send.
        :raises DeviceNotConnectedError: If no device is connected.
        :raises GPIBError: If the command fails to send.
        """
        if not self.device:
            raise DeviceNotConnectedError("No device connected.")
        try:
            self.device.write(command)
            logger.debug(f"Command sent: {command}")
        except pyvisa.VisaIOError as e:
            raise GPIBError(f"Failed to send command: {e}") from e

    def read_response(self) -> str:
        """
        Read response from the GPIB device.

        :return: The response string from the device.
        :raises DeviceNotConnectedError: If no device is connected.
        :raises GPIBError: If reading the response fails.
        """
        if not self.device:
            raise DeviceNotConnectedError("No device connected.")
        try:
            response = self.device.read()
            logger.debug(f"Response: {response}")
            return response
        except pyvisa.VisaIOError as e:
            raise GPIBError(f"Failed to read response: {e}") from e

    def read_ascii(self) -> str:
        """
        Read ASCII response from the GPIB device.

        :return: The ASCII response from the device.
        :raises DeviceNotConnectedError: If no device is connected.
        :raises GPIBError: If reading the response fails.
        """
        if not self.device:
            raise DeviceNotConnectedError("No device connected.")
        try:
            response = self.device.read_ascii_values()
            logger.debug(f"Response: {response}")
            return response
        except pyvisa.VisaIOError as e:
            raise GPIBError(f"Failed to read response: {e}") from e

    def query_response(self, command: str) -> str:
        """
        Query response from the GPIB device.

        :param command: The command to query.
        :return: The response string from the device.
        :raises DeviceNotConnectedError: If no device is connected.
        :raises GPIBError: If the query fails.
        """
        if not self.device:
            raise DeviceNotConnectedError("No device connected.")
        try:
            response = self.device.query(command)
            logger.debug(f"Query: {command} -> {response}")
            return response
        except pyvisa.VisaIOError as e:
            raise GPIBError(f"Failed to query response: {e}") from e
