# debug_tests/three_way_sweep.py
import time

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command import GPIBCommand
from src.tests.basic_test import BasicTest
from src.tests.advance_test import AdvanceTest


def test_gpib_command():
    advance_test = AdvanceTest()

    result = advance_test.three_way_sweep(17, 2, 1, 0, 0.0,
                                     1.0, 3, None,
                                     None, 3, 0, 0.0,
                                     2.0, 5, None, 1,
                                     0, 0.0, 1.0,
                                     4, None, 4,
                                     0, 1.2, None,
                                     None, None)

    result.to_csv('output.csv', index=False)


if __name__ == "__main__":
    test_gpib_command()
