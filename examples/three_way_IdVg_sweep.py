# debug_tests/three_way_IdVg_sweep.py
from src.measurement.advance_sweep import AdvanceTest


def test_gpib_command():
    advance_test = AdvanceTest()

    result = advance_test.three_way_sweep(17, 2, 1, 0, 0.0,
                                          -1.2, 121, 0.1,
                                          None, 1, 0, 0.0,
                                          -1.2, 121, 0.1, 4,
                                          0, -0.6, 0.6,
                                          121, 0.1, 3,
                                          0, 0, 0.1,
                                          None, None)

    result.to_csv('data/Jan_No10Vg.csv', index=False)


if __name__ == "__main__":
    test_gpib_command()
