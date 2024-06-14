# src/gpib/gpib_command.py

from typing import List, Optional
from src.gpib.gpib_communication import GPIBCommunication


class GPIBCommand:
    def __init__(self):
        """
        Initializes the GPIBCommand class with a GPIBCommunication instance.
        """
        self.communication = GPIBCommunication()

    def init_connection(self, gpib_id: int = 17):
        """
        Initializes connection to the GPIB device.

        :param gpib_id: gpib address of the GPIB device.
        """
        gpib_address = f"GPIB0::{gpib_id}::INSTR"
        self.communication.connect_device(gpib_address)
        self.communication.device.timeout = None

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

    def set_voltage_sweep(self, channel: int, mode: int, v_range: int, start: float, stop: float, step: int,
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
        [Query] Waits until pending operation is complete.

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

    def set_smu_mode(self, channel: int, mode: int) -> None:
        """
        Sets the SMU measurement operation mode.

        :param channel: SMU channel numbers.
        :param mode: SMU measurement mode.
        """
        self.communication.send_command(f"CMM {channel},{mode}")

    def set_output_format(self, out_format: int = 11, mode: int = None) -> None:
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

    def set_filter(self, mode: bool = False, channels: Optional[List[int]] = None) -> None:
        """
        Sets the connection mode of a SMU filter for each channel.

        :param mode: Status of the filter
        :param channels: SMU channel number.
        """
        command = f"FL {int(mode)}"
        if channels:
            command += " " + ",".join(map(str, channels))
        self.communication.send_command(command)

    def set_averaging(self, number: int = 1, mode: int = 0) -> None:
        """
        Sets the number of averaging samples. High-speed ADC only.

        :param number: number of averaging samples.
        :param mode: Averaging mode.
        """
        command = f"AV {number}"
        if mode:
            command += f",{mode}"
        self.communication.send_command(command)

    def current_measurement_range(self, channel: int, current_range: int) -> None:
        """
        Sets the current measurement range.

        :param channel: SMU channel number.
        :param current_range: Measurement range.
        """
        self.communication.send_command(f"RI {channel},{current_range}")

    def voltage_measurement_range(self, channel: int, voltage_range: int) -> None:
        """
        Sets the current measurement range.

        :param channel: SMU channel number.
        :param voltage_range: Measurement range.
        """
        self.communication.send_command(f"RV {channel},{voltage_range}")

    def sweep_delay(self, hold: float = 0, delay: float = 0, sdelay: Optional[float] = 0, tdelay: Optional[float] = 0,
                    mdelay: Optional[float] = 0) -> None:
        """
        Sets the hold time, delay time, and step delay time for the staircase sweep or multichannel sweep measurement.

        :param hold: Hold time in seconds.
        :param delay: Delay time in seconds.
        :param sdelay: Step delay time in seconds.
        :param tdelay: Step source trigger delay time in seconds.
        :param mdelay: Step measurement trigger delay time in seconds.
        """
        command = f"WT {hold},{delay}"
        if sdelay:
            command += f",{sdelay}"
        if tdelay:
            command += f",{tdelay}"
        if mdelay:
            command += f",{mdelay}"
        self.communication.send_command(command)

    def auto_abort(self, abort: int = 0, post: Optional[int] = 1) -> None:
        """
        Enables or disables automatic abort function.

        :param abort: Automatic abort function mode.
        :param post: Source output value after the measurement is normally completed.
        """
        command = f"WM {abort}"
        if post is not None:
            command += f",{post}"
        self.communication.send_command(command)

    def query_error(self, mode: Optional[int] = 0) -> str:
        """
        [Query] Query error code.

        :param mode: Error code output mode.
        """
        command = "ERR?"
        if mode:
            command += f" {mode}"
        return self.communication.query_response(command)

    def read_response(self):
        return self.communication.read_response()
