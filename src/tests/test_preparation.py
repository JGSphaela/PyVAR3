# src/config/test_preparation.py

from typing import Optional

import pandas as pd

from src.gpib.gpib_command_b1500 import GPIBCommand
from src.data_process.read_data_process import DataProcess


class TestPreparation():
    def __init__(self):
        self.command = GPIBCommand()
        self.data_process = DataProcess()

    def pre_test_setup(self, gpib_id: int, output_format: Optional[int] = None, output_mode: Optional[int] = None,
                       time_stamp_enable: Optional[bool] = None, smu_filter_enable: Optional[bool] = None,
                       averaging_number: Optional[int] = None, averaging_mode: Optional[int] = None):
        self.command.init_connection(gpib_id)

        if output_format is not None and output_mode is not None:
            self.command.set_output_format(out_format=output_format, mode=output_mode)
        if time_stamp_enable is not None:
            self.command.time_stamp(time_stamp_enable)
        if smu_filter_enable is not None:
            self.command.set_filter(mode=smu_filter_enable)
        if averaging_number is not None and averaging_mode is not None:
            self.command.set_averaging(number=averaging_number, mode=averaging_mode)

    def run_test(self, gpib_id, auto_abort_enable: Optional[bool] = None) -> pd.DataFrame:
        self.command.init_connection(gpib_id=gpib_id)
        if auto_abort_enable:
            self.command.auto_abort(abort=2)

        self.command.trigger_measurement()
        self.command.wait_pending()
        read_data = self.command.read_response()
        self.command.reset_channel()
        return self.data_process.data_into_dataframe(read_data)
