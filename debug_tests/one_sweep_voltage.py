# debug_tests/multichannel_sweep_voltage.py
import time

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command_b1500 import GPIBCommand
from src.tests.basic_test import BasicTest


def test_gpib_command():
    basic_test = BasicTest()

    result = basic_test.multichannel_sweep_voltage(17, 1, 1, 0, 0.0, -1.2,
                                          801, 0.1, None,
                                          2, 0, 0, None,
                                          None, None, 3,
                                          0, 0, None,
                                          None, None, 4,
                                          0, 0, None,
                                          None, None,)

    result.to_csv('Jan_No10Vd_1mV.csv', index=False)

if __name__ == "__main__":
    test_gpib_command()
