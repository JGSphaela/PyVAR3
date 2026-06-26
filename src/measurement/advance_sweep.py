# src/measurement/advance_sweep.py
import datetime
import logging
import threading
import time

import pandas as pd

from src.gpib.exceptions import MeasurementAbortedError, PyVARError
from src.measurement.basic_sweep import BasicTest
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Type alias for progress callbacks: (current_step, total_steps, elapsed_seconds)
ProgressCallback = Optional[Callable[[int, int, float], None]]


class AdvanceTest:
    """Orchestrates multi-way (2 or 3 parameter) sweep measurements.

    Wraps BasicTest to perform nested sweeps: the outer sweep controls constant
    voltages while the inner sweep performs the actual staircase measurement.
    Includes progress tracking with ETA estimation and backup data saving.
    """

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
                      const2_current_range: Optional[int] = None,
                      progress_callback: ProgressCallback = None,
                      abort_flag: Optional[threading.Event] = None) -> pd.DataFrame:

        if sweep2_step == 1:
            step_value = sweep2_start
        else:
            step_value = (sweep2_stop - sweep2_start) / (sweep2_step - 1)
        sweep2_column_name = f"{chr(sweep2_channel + 64)}_V"
        results = []
        start_time = time.time()

        for step in range(0, sweep2_step):
            if abort_flag and abort_flag.is_set():
                partial = pd.concat(results, ignore_index=True) if results else pd.DataFrame()
                raise MeasurementAbortedError("Two-way sweep aborted by user", partial_data=partial)

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
            results.append(step_result)

            if progress_callback:
                progress_callback(step + 1, sweep2_step, time.time() - start_time)

        return pd.concat(results, ignore_index=True) if results else pd.DataFrame()

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
                        const2_current_range: Optional[int] = None,
                        progress_callback: ProgressCallback = None,
                        abort_flag: Optional[threading.Event] = None,
                        temperature_callback: Optional[Callable[[], dict]] = None) -> pd.DataFrame:

        if sweep2_step == 1:
            sweep2_step_value = sweep2_start
        else:
            sweep2_step_value = (sweep2_stop - sweep2_start) / (sweep2_step - 1)

        if sweep3_step == 1:
            sweep3_step_value = sweep3_start
        else:
            sweep3_step_value = (sweep3_stop - sweep3_start) / (sweep3_step - 1)

        sweep2_column_name = f"{chr(sweep2_channel + 64)}_V"
        sweep3_column_name = f"{chr(sweep3_channel + 64)}_V"
        all_results = []
        counter = 0
        total_step = sweep3_step * sweep2_step
        last_finish_time = time.time()
        time_list = []
        sweep_start_time = time.time()

        for sweep3_step_index in range(0, sweep3_step):
            if abort_flag and abort_flag.is_set():
                partial = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
                raise MeasurementAbortedError("Three-way sweep aborted by user", partial_data=partial)

            sweep3_step_voltage = round(sweep3_start + sweep3_step_index * sweep3_step_value, 6)

            # Get temperature reading if callback provided
            temps = {}
            if temperature_callback:
                try:
                    temps = temperature_callback()
                except Exception as e:
                    logger.warning(f"Temperature read failed: {e}")

            sweep2_results = []
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
                sweep2_results.append(sweep2_step_result)
                counter += 1

                duration = time.time() - last_finish_time
                time_list.append(duration)
                if len(time_list) > 5:
                    time_list.pop(0)

                average_time = sum(time_list) / len(time_list)
                elapsed = time.time() - sweep_start_time

                estimate_finish = datetime.datetime.fromtimestamp(time.time() + average_time * (total_step - counter))
                estimate_finish_str = estimate_finish.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
                logger.info(f'Progress: ({counter}/{total_step}) - {round(counter / (total_step) * 100, 2)}% done!')
                logger.info(f'Last session took {duration:.2f} seconds!')
                if counter != total_step:
                    logger.info(f'Estimated finish time: {estimate_finish_str}')

                if progress_callback:
                    progress_callback(counter, total_step, elapsed)

                last_finish_time = time.time()

            sweep2_result = pd.concat(sweep2_results, ignore_index=True)
            sweep2_result[sweep3_column_name] = sweep3_step_voltage

            # Add temperature columns if available
            for ch, temp in temps.items():
                sweep2_result[f'Temp_{ch}_K'] = temp

            if sweep2_result.shape[0] != (sweep1_step * sweep2_step):
                sweep2_result.to_csv('data/error_data.csv', index=False)
                raise PyVARError('The number of output data is less than sweep step, an error may occurred. '
                                'Check data/error_data.csv file.')
            sweep2_result.to_csv('data/backup_data.csv', mode='a', header=False, index=False)
            all_results.append(sweep2_result)

        return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
