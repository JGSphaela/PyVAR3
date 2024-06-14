# tests/test_gpib_command.py
import time

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command import GPIBCommand
from src.tests.basic_test import BasicTest


def test_gpib_command():
    basic_test = BasicTest()

    print(basic_test.multichannel_sweep_voltage(17, 2, 1, 0, 0.0, 1.0,
                                          21, 0.01, None,
                                          1, 0, 1, None,
                                          None, None, 3,
                                          0, 1, None,
                                          None, None, 4,
                                          0, 1, None,
                                          None, None,))


if __name__ == "__main__":
    test_gpib_command()
