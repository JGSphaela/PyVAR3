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
                                   const1_channel: int = 2,
                                   const1_range: int = 0, const1_voltage: float = 0.0,
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
        # Set measurement mode
        self.command.set_measurement_mode(16, [sweep_channel])
