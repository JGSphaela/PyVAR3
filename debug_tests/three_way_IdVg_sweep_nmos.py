# debug_tests/three_way_IdVg_sweep.py
from src.tests.advance_test import AdvanceTest
from datetime import datetime


def test_gpib_command():
    advance_test = AdvanceTest()

    output_file_path = 'data/Nov_No8VgVdVsub.csv'
    measured_device = '2023.11 TSMC 22nm TEG'
    device_id = 8
    temperature_k = 295
    sweep_parameter = '\n#    Vg:[0V ~ 0.8V steps:41]\n#    Vd:[0V ~ 0.8V steps:41]\n#    Vsub:[0V ~ -0.8V steps:41]'
    const_parameter = '\n#    Vsource:[0V]\n#    VDD:[0.8V]\n#    GND:[0V]'

    start_time = datetime.now()
    date = start_time.strftime('%Y-%m-%d')
    start_time_formatted = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    result = advance_test.three_way_sweep(17, 2, 1, 0, 0.0,
                                          0.8, 41, 0.01,
                                          None, 1, 0, 0.0,
                                          0.8, 41, 0.01, 4,
                                          0, 0, -0.8,
                                          41, 0.01, 3,
                                          0, 0, 0.01,
                                          None, None)

    end_time = datetime.now()
    end_time_formatted = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    comments = [
        'Measurement Date: ' + date,
        'Measured Device: ' + measured_device,
        'Device ID: ' + str(device_id),
        'Sweeping Parameter: ' + sweep_parameter,
        'Constant Parameter: ' + const_parameter,
        'Start Time: ' + start_time_formatted,
        'End Time: ' + end_time_formatted,
        'Temperature: ' + str(temperature_k) + 'K',
    ]

    with open(output_file_path, mode='w') as output_file:
        for comment in comments:
            output_file.write('# ' + comment + '\n')
        output_file.write('Drain_I,Gate_I,Source_I,Sub_I,Gate_V,Drain_V,Sub_V\n')

    result.to_csv(output_file_path, mode='a', header=False, index=False)


if __name__ == "__main__":
    test_gpib_command()
