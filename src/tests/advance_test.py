# src/tests/advance_tset.py

from src.data_process.read_data_process import DataProcess
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
                      const2_current_range: Optional[int] = None):
        step_value = (sweep2_stop - sweep2_start) / sweep1_step
        for step in range(0, sweep2_step + 1):
            step_voltage = 0.0 + step * step_value
            result = self.basic_test.multichannel_sweep_voltage(gpib_device_id=gpib_device_id,
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
