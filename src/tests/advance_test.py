# src/tests/advance_tset.py
import datetime
import time

import pandas as pd

from src.tests.basic_test import BasicTest
from typing import Optional


class AdvanceTest:
    def __init__(self):
        self.basic_test = BasicTest()

    def two_way_sweep(self, gpib_device_id: int = 17, sweep1_channel: int = 1, sweep1_mode: int = 1,
                      sweep1_range: int = 0, sweep1_start: float = 0.0, sweep1_stop: float = 0.0,
                      sweep1_step: int = 0, sweep1_current_compliance: Optional[float] = None,
                      sweep1_power_compliance: Optional[float] = None, sweep2_channel: int = 1,
                      sweep2_range: int = 0, sweep2_start: float = 0.0, sweep2_stop: float = 0.0,
                      sweep2_step: int = 0, sweep2_current_compliance: Optional[float] = None,
                      const1_channel: Optional[int] = None,
                      const1_range: Optional[int] = None, const1_voltage: Optional[float] = None,
                      const1_current_compliance: Optional[float] = None,
                      const1_current_compliance_polarity: Optional[float] = None,
                      const1_current_range: Optional[int] = None,
                      const2_channel: Optional[int] = None,
                      const2_range: Optional[int] = None, const2_voltage: Optional[float] = None,
                      const2_current_compliance: Optional[float] = None,
                      const2_current_compliance_polarity: Optional[float] = None,
                      const2_current_range: Optional[int] = None) -> pd.DataFrame:

        step_value = (sweep2_stop - sweep2_start) / (sweep2_step - 1)
        sweep2_column_name = f"{chr(sweep2_channel + 64)}_V"
        result = pd.DataFrame()

        for step in range(0, sweep2_step):
            step_voltage = round(sweep2_start + step * step_value, 6)
            step_result = self.basic_test.multichannel_sweep_voltage(gpib_device_id=gpib_device_id,
                                                                     sweep_channel=sweep1_channel,
                                                                     sweep_mode=sweep1_mode, sweep_range=sweep1_range,
                                                                     sweep_start=sweep1_start, sweep_stop=sweep1_stop,
                                                                     sweep_step=sweep1_step,
                                                                     sweep_current_compliance=sweep1_current_compliance,
                                                                     sweep_power_compliance=sweep1_power_compliance,
                                                                     const1_channel=sweep2_channel,
                                                                     const1_range=sweep2_range,
                                                                     const1_voltage=step_voltage,
                                                                     const1_current_compliance=sweep2_current_compliance,
                                                                     const2_channel=const1_channel,
                                                                     const2_range=const1_range,
                                                                     const2_voltage=const1_voltage,
                                                                     const2_current_compliance=const1_current_compliance,
                                                                     const2_current_compliance_polarity=const1_current_compliance_polarity,
                                                                     const2_current_range=const1_current_range,
                                                                     const3_channel=const2_channel,
                                                                     const3_range=const2_range,
                                                                     const3_voltage=const2_voltage,
                                                                     const3_current_compliance=const2_current_compliance,
                                                                     const3_current_compliance_polarity=const2_current_compliance_polarity,
                                                                     const3_current_range=const2_current_range)
            step_result[sweep2_column_name] = step_voltage
            result = pd.concat([result, step_result], ignore_index=True)

        return result

    def three_way_sweep(self, gpib_device_id: int = 17, sweep1_channel: int = 1, sweep1_mode: int = 1,
                        sweep1_range: int = 0, sweep1_start: float = 0.0, sweep1_stop: float = 0.0,
                        sweep1_step: int = 0, sweep1_current_compliance: Optional[float] = None,
                        sweep1_power_compliance: Optional[float] = None, sweep2_channel: int = 1,
                        sweep2_range: int = 0, sweep2_start: float = 0.0, sweep2_stop: float = 0.0,
                        sweep2_step: int = 0, sweep2_current_compliance: Optional[float] = None,
                        sweep3_channel: int = 1,
                        sweep3_range: int = 0, sweep3_start: float = 0.0, sweep3_stop: float = 0.0,
                        sweep3_step: int = 0, sweep3_current_compliance: Optional[float] = None,
                        const1_channel: Optional[int] = None,
                        const1_range: Optional[int] = None, const1_voltage: Optional[float] = None,
                        const1_current_compliance: Optional[float] = None,
                        const1_current_compliance_polarity: Optional[float] = None,
                        const1_current_range: Optional[int] = None,
                        const2_channel: Optional[int] = None,
                        const2_range: Optional[int] = None, const2_voltage: Optional[float] = None,
                        const2_current_compliance: Optional[float] = None,
                        const2_current_compliance_polarity: Optional[float] = None,
                        const2_current_range: Optional[int] = None) -> pd.DataFrame:

        sweep2_step_value = (sweep2_stop - sweep2_start) / (sweep2_step - 1)
        sweep3_step_value = (sweep3_stop - sweep3_start) / (sweep3_step - 1)
        sweep2_column_name = f"{chr(sweep2_channel + 64)}_V"
        sweep3_column_name = f"{chr(sweep3_channel + 64)}_V"
        result = pd.DataFrame()
        counter = 0
        total_step = sweep3_step * sweep2_step
        last_finish_time = time.time()

        for sweep3_step_index in range(0, sweep3_step):
            sweep3_step_voltage = round(sweep3_start + sweep3_step_index * sweep3_step_value, 6)
            sweep2_result = pd.DataFrame()
            for sweep2_step_index in range(0, sweep2_step):
                sweep2_step_voltage = round(sweep2_start + sweep2_step_index * sweep2_step_value, 6)
                sweep2_step_result = self.basic_test.multichannel_sweep_voltage(gpib_device_id=gpib_device_id,
                                                                                sweep_channel=sweep1_channel,
                                                                                sweep_mode=sweep1_mode,
                                                                                sweep_range=sweep1_range,
                                                                                sweep_start=sweep1_start,
                                                                                sweep_stop=sweep1_stop,
                                                                                sweep_step=sweep1_step,
                                                                                sweep_current_compliance=sweep1_current_compliance,
                                                                                sweep_power_compliance=sweep1_power_compliance,
                                                                                const1_channel=sweep2_channel,
                                                                                const1_range=sweep2_range,
                                                                                const1_voltage=sweep2_step_voltage,
                                                                                const1_current_compliance=sweep2_current_compliance,
                                                                                const2_channel=sweep3_channel,
                                                                                const2_range=sweep3_range,
                                                                                const2_voltage=sweep3_step_voltage,
                                                                                const2_current_compliance=sweep3_current_compliance,
                                                                                const3_channel=const1_channel,
                                                                                const3_range=const1_range,
                                                                                const3_voltage=const1_voltage,
                                                                                const3_current_compliance=const1_current_compliance,
                                                                                const3_current_compliance_polarity=const1_current_compliance_polarity,
                                                                                const3_current_range=const1_current_range,
                                                                                const4_channel=const2_channel,
                                                                                const4_range=const2_range,
                                                                                const4_voltage=const2_voltage,
                                                                                const4_current_compliance=const2_current_compliance,
                                                                                const4_current_compliance_polarity=const2_current_compliance_polarity,
                                                                                const4_current_range=const2_current_range,
                                                                                counter=counter)
                sweep2_step_result[sweep2_column_name] = sweep2_step_voltage
                sweep2_result = pd.concat([sweep2_result, sweep2_step_result], ignore_index=True)
                counter += 1
                duration = time.time() - last_finish_time
                estimate_finish = datetime.datetime.fromtimestamp(time.time() + duration * (total_step - counter))
                estimate_finish_str = estimate_finish.strftime('%Y-%m-%d %H:%M:%S.%f')
                print('---')
                print(f'Progress: ({counter}/{total_step}) - {round(counter / (total_step) * 100, 2)}% done!')
                print(f'last session took {duration:.2f} seconds!')
                print(f'Estimated finish time: {estimate_finish_str}')
                print('---')
                last_finish_time = time.time()

            sweep2_result[sweep3_column_name] = sweep3_step_voltage

            if sweep2_result.shape[0] != (sweep1_step * sweep2_step):
                sweep2_result.to_csv('data/error_data.csv', index=False)
                raise Exception('The number of output data is less than sweep step, an error may occurred.'
                                'Check data/error_data.csv file.')
            sweep2_result.to_csv('data/backup_data.csv', mode='a', header=False, index=False)
            result = pd.concat([result, sweep2_result], ignore_index=True)

        return result
