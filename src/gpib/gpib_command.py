# src/gpib/gpib_command.py

from typing import List, Optional
from src.gpib.gpib_communication import GPIBCommunication


class GPIBCommand:
    def __init__(self, communication: GPIBCommunication):
        """
        Initializes the GPIBCommand class with a GPIBCommunication instance.

        :param communication: An instance of GPIBCommunication for sending GPIB commands.
        """
        self.communication = communication

    def enable_channels(self, channels: Optional[List[int]] = None) -> None:
        """
        Enables the specified channels.

        :param channels: A list of channel numbers to enable. If None, enables all channels.
        """
        command = "CN"
        if channels:
            command += " " + ",".join(map(str, channels))
        self.communication.send_command(command)

    def disable_channels(self, channels: Optional[List[int]] = None) -> None:
        """
        Disables the specified channels.

        :param channels: A list of channel numbers to disable. If None, disables all channels.
        """
        command = "CL"
        if channels:
            command += " " + ",".join(map(str, channels))
        self.communication.send_command(command)

    def set_voltage_sweep(self, channel: int, mode: int, v_range: int, start: float, stop: float, step: float,
                          icomp: Optional[float] = None, pcomp: Optional[float] = None) -> None:
        """
        Sets the staircase sweep voltage source and its parameters.

        :param channel: SMU sweep source channel number.
        :param mode: Sweep mode.
        :param v_range: Ranging type for staircase sweep voltage output.
        :param start: Start voltage.
        :param stop: Stop voltage.
        :param step: Number of steps for staircase sweep.
        :param icomp: Current compliance (optional).
        :param pcomp: Power compliance (optional).
        """
        command = f"WV {channel},{mode},{v_range},{start},{stop},{step}"
        if icomp is not None:
            command += f",{icomp}"
        if pcomp is not None:
            command += f",{pcomp}"
        self.communication.send_command(command)

    def set_current_sweep(self, channel: int, mode: int, i_range: int, start: float, stop: float, step: float,
                          vcomp: Optional[float] = None, pcomp: Optional[float] = None) -> None:
        """
        Sets the current sweep source and its parameters.

        :param channel: SMU sweep source channel number.
        :param mode: Sweep mode.
        :param i_range: Ranging type for staircase sweep current output.
        :param start: Start current.
        :param stop: Stop current.
        :param step: Number of steps for staircase sweep.
        :param vcomp: Voltage compliance (optional).
        :param pcomp: Power compliance (optional).
        """
        command = f"WI {channel},{mode},{i_range},{start},{stop},{step}"
        if vcomp is not None:
            command += f",{vcomp}"
        if pcomp is not None:
            command += f",{pcomp}"
        self.communication.send_command(command)

    def force_voltage(self, channel: int, v_range: int, voltage: float, icomp: Optional[float] = None,
                      comp_polarity: Optional[int] = 0, i_range: Optional[int] = None) -> None:
        """
        Forces DC voltage from the specified SMU.

        :param channel: SMU source channel number.
        :param v_range: Ranging type for voltage output.
        :param voltage: Output voltage value.
        :param icomp: Current compliance value (optional).
        :param comp_polarity: Polarity of current compliance (optional).
        :param i_range: Current compliance ranging type (optional).
        """
        command = f"DV {channel},{v_range},{voltage}"
        if icomp is not None:
            command += f",{icomp}"
        if comp_polarity is not None:
            command += f",{comp_polarity}"
        if i_range is not None:
            command += f",{i_range}"
        self.communication.send_command(command)

    def force_current(self, channel: int, i_range: int, current: float, vcomp: Optional[float] = None,
                      comp_polarity: Optional[int] = 0, v_range: Optional[int] = None) -> None:
        """
        Forces constant current from the specified SMU.

        :param channel: SMU source channel number.
        :param i_range: Ranging type for current output.
        :param current: Output current value.
        :param vcomp: Voltage compliance value (optional).
        :param comp_polarity: Polarity of voltage compliance (optional).
        :param v_range: Voltage compliance ranging type (optional).
        """
        command = f"DI {channel},{i_range},{current}"
        if vcomp is not None:
            command += f",{vcomp}"
        if comp_polarity is not None:
            command += f",{comp_polarity}"
        if v_range is not None:
            command += f",{v_range}"
        self.communication.send_command(command)

    # Note: can be rewritten in the future to better comply with the official syntax
    def set_measurement_mode(self, mode: int, channels: Optional[List[int]] = None) -> None:
        """
        Specifies the measurement mode and the channels used for measurements.

        :param mode: Measurement mode.
        :param channels: List of measurement channel numbers (optional).
        """
        command = f"MM {mode}"
        if channels:
            command += "," + ",".join(map(str, channels))
        self.communication.send_command(command)

    def trigger_measurement(self) -> None:
        """
        Triggers the B1500 to start measurement.
        """
        self.communication.send_command("XE")

    def wait_pending(self) -> str:
        """
        Waits until pending operation is complete.

        :return:
        """
        return self.communication.query_response("*OPC?")

    def reset_channel(self, channels: Optional[List[int]] = None) -> None:
        """
        Resets the channels used for measurements.

        :param channels: A list of channel numbers to reset. If None, disables all channels.
        """
        command = "DZ"
        if channels:
            command += " " + ",".join(map(str, channels))
        self.communication.send_command(command)

    def set_smu_mode(self, channels: List[int], mode: int) -> None:
        """
        Sets the SMU measurement operation mode.

        :param channels: SMU channel numbers.
        :param mode: SMU measurement mode.
        """
        command = "CMM"
        command += " " + ",".join(map(str, channels)) + ',' + str(mode)
        self.communication.send_command(command)

    def set_output_format(self, out_format: int, mode: int = None) -> None:
        """
        Sets the output format of the measurement.

        :param out_format: Data output format.
        :param mode: Data output mode.
        """
        command = "FMT"
        command += " " + str(out_format) + ',' + str(mode)
        self.communication.send_command(command)

    def number_of_measurements(self) -> str:
        """
        [Query] Query the number of measurements.

        :return:
        """
        return self.communication.query_response("NUB?")

    def time_stamp(self, enable: bool = False) -> None:
        """
        Enables or disables time stamp function.

        :param enable:
        """
        command = f"TSC {int(enable)}"
        self.communication.send_command(command)

    def reset_time(self, channels: Optional[List[int]] = None) -> None:
        """
        Clears the timer count.

        :param channels: SMU or MFCMU channel number.
        """
        command = "TSR"
        if channels:
            command += " " + ",".join(map(str, channels))
        self.communication.send_command(command)
