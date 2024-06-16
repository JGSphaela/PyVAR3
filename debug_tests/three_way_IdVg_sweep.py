# debug_tests/three_way_IdVg_sweep.py
import time

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command import GPIBCommand
from src.tests.basic_test import BasicTest
from src.tests.advance_test import AdvanceTest


def test_gpib_command():
    advance_test = AdvanceTest()

    result = advance_test.three_way_sweep(17, 2, 1, 0, 0.0,
                                          -0.8, 81, 0.1,
                                          None, 1, 0, 0.0,
                                          -0.8, 9, 0.01, 4,
                                          0, -0.4, 0.4,
                                          9, 0.0001, 3,
                                          0, 0, 0.1,
                                          None, None)

    result.to_csv('Nov_No17IdVg.csv', index=False)


if __name__ == "__main__":
    test_gpib_command()
