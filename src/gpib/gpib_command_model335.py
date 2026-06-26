# src/gpib/gpib_command_model335.py
# This file implemented Model335 GPIB commands.

import logging
from src.gpib.gpib_communication import GPIBCommunication

logger = logging.getLogger(__name__)


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
        """Query temperature in Celsius from the specified input channel.

        :param input_channel: Input channel to query ('A' or 'B').
        :return: Temperature string in Celsius (e.g. '+25.0').
        """
        return self.communication.query_response(f"CRDG? {input_channel}")

    def query_kelvin(self, input_channel: str = "A"):
        """Query temperature in Kelvin from the specified input channel.

        :param input_channel: Input channel to query ('A' or 'B').
        :return: Temperature string in Kelvin (e.g. '+298.15').
        """
        return self.communication.query_response(f"KRDG? {input_channel}")

    def query_kelvin_float(self, input_channel: str = "A") -> float:
        """Query temperature in Kelvin as a float.

        :param input_channel: Input channel to query ('A' or 'B').
        :return: Temperature in Kelvin.
        """
        raw = self.query_kelvin(input_channel)
        return float(raw.strip())

    def set_setpoint(self, loop: int = 1, temperature: float = 300.0) -> None:
        """Set the temperature setpoint for a control loop.

        :param loop: Control loop number (1 or 2).
        :param temperature: Target temperature in the units configured on the instrument.
        """
        self.communication.send_command(f"SETP {loop},{temperature}")
        logger.info(f"Setpoint for loop {loop} set to {temperature}")

    def query_heater_output(self, loop: int = 1) -> float:
        """Query the heater output percentage.

        :param loop: Control loop number (1 or 2).
        :return: Heater output as a percentage (0-100).
        """
        raw = self.communication.query_response(f"HTR?")
        return float(raw.strip())
