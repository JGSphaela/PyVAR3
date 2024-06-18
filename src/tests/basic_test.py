# src/tests/basic_test.py

from typing import Optional

import pandas as pd

from src.gpib.gpib_command import GPIBCommand
from src.data_process.read_data_process import DataProcess


class BasicTest:
    def __init__(self):
        self.command = GPIBCommand()
        self.data_process = DataProcess()

    def multichannel_sweep_voltage(self, gpib_device_id: int = 17, sweep_channel: int = 1, sweep_mode: int = 1,
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
                                   const3_current_range: Optional[int] = None, counter: Optional[int] = None) -> pd.DataFrame:
        if not counter:
            # Pretest prep
            # note: FMT is needed to get sweep voltage output
            self.command.init_connection(gpib_device_id)
            self.command.set_output_format(11, 1)

            # Get all in-use channels
            all_channels = [sweep_channel]
            if const1_channel is not None:
                all_channels.append(const1_channel)
            if const2_channel is not None:
                all_channels.append(const2_channel)
            if const3_channel is not None:
                all_channels.append(const3_channel)

            if const1_channel is not None or const2_channel is not None or const3_channel is not None:
                all_channels = sorted(all_channels)

            # for channel in all_channels:
            #     self.command.set_adc_type(channel=channel, adc_type=1)
            #
            # self.command.set_adc_mode(adc_type=1, mode=1, coefficient=1)
            #
            # Set measurement mode
            self.command.set_measurement_mode(mode=16, channels=all_channels)
            #
            # for channel in all_channels:
            #     self.command.set_smu_mode(channel=channel, mode=0)
            #     self.command.current_measurement_range(channel=channel, current_range=0)
            #     self.command.voltage_measurement_range(channel=channel, voltage_range=0)
            #
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

        out_data = self.data_process.data_into_dataframe(self.command.trigger_measurement())
        if out_data.shape[0] != sweep_step:
            out_data.to_csv('data/error_data.csv', index=False)
            raise Exception('The number of output data is less than sweep step, an error may occurred')
        return out_data
