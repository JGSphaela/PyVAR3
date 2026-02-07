# src/gpib/gpib_command_model335.py
# This file implemented Model335 GPIB commands.

from typing import List, Optional
from src.gpib.gpib_communication import GPIBCommunication

class Model335GPIBCommand:
    def __init__(self):
        self.communication = GPIBCommunication()

    def init_connection(self, gpib_id: int = 12):
        """
        Initializes connection to the GPIB device.

        :param gpib_id: gpib address of the GPIB device.
        """
        gpib_address = f"GPIB0::{gpib_id}::INSTR"
        self.communication.connect_device(gpib_address)
        self.communication.device.timeout = None

    def query_celsius(self, input_channel: str = "A"):
        return self.communication.query_response(f"CRDG? {input_channel}")

    def query_kelvin(self, input_channel: str = "A"):
        return self.communication.query_response(f"KRDG? {input_channel}")
