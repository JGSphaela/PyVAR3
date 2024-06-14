# src/tests/basic_test.py

from typing import List, Optional
from src.gpib.gpib_command import GPIBCommand


class BasicTest:
    def __init__(self):
        self.command = GPIBCommand()

    def multichannel_sweep_voltage(self, sweep_channel: int = 1, sweep_mode: int = 1,
                                   sweep_range: int = 0, sweep_start: float = 0.0, sweep_stop: float = 0.0,
                                   sweep_step: int = 0, sweep_current_compliance: Optional[float] = None,
                                   sweep_power_compliance: Optional[float] = None,
                                   const1_channel: Optional[int] = None,
                                   const1_range: Optional[int] = None, const1_voltage: Optional[float] = None,
                                   const1_current_compliance: Optional[float] = None,
                                   const1_current_compliance_polarity: Optional[float] = None,
                                   const1_current_range: Optional[int] = None,
                                   const2_channel: Optional[int] = None,
                                   const2_range: Optional[int] = None, const2_voltage: Optional[float] = None,
                                   const2_current_compliance: Optional[float] = None,
                                   const2_current_compliance_polarity: Optional[float] = None,
                                   const2_current_range: Optional[int] = None,
                                   const3_channel: Optional[int] = None,
                                   const3_range: Optional[int] = None, const3_voltage: Optional[float] = None,
                                   const3_current_compliance: Optional[float] = None,
                                   const3_current_compliance_polarity: Optional[float] = None,
                                   const3_current_range: Optional[int] = None):
        # Get all in-use channels
        all_channels = [sweep_channel]
        if const1_channel is not None:
            all_channels.append(const1_channel)
        if const2_channel is not None:
            all_channels.append(const2_channel)
        if const3_channel is not None:
            all_channels.append(const3_channel)

        # Set measurement mode
        self.command.set_measurement_mode(mode=16, channels=all_channels)

        # Enable channels
        self.command.enable_channels(all_channels)

        # Set voltage sweep
        self.command.set_voltage_sweep(channel=sweep_channel, mode=sweep_mode, v_range=sweep_range, start=sweep_start,
                                       stop=sweep_stop, step=sweep_step, icomp=sweep_current_compliance,
                                       pcomp=sweep_power_compliance)

        # Set constant voltage
        if const1_channel is not None:
            self.command.force_voltage(channel=const1_channel, v_range=const1_range, voltage=const1_voltage,
                                       icomp=const1_current_compliance,
                                       comp_polarity=const1_current_compliance_polarity,
                                       i_range=const1_current_range)
        if const2_channel is not None:
            self.command.force_voltage(channel=const2_channel, v_range=const2_range, voltage=const2_voltage,
                                       icomp=const2_current_compliance,
                                       comp_polarity=const2_current_compliance_polarity,
                                       i_range=const2_current_range)
        if const3_channel is not None:
            self.command.force_voltage(channel=const3_channel, v_range=const3_range, voltage=const3_voltage,
                                       icomp=const3_current_compliance,
                                       comp_polarity=const3_current_compliance_polarity,
                                       i_range=const3_current_range)