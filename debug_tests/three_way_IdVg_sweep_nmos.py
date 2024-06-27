# debug_tests/three_way_IdVg_sweep.py
from src.tests.advance_test import AdvanceTest
from datetime import datetime

def test_gpib_command():
    advance_test = AdvanceTest()

    output_file_path = 'data/Nov_No2VgVdVsub.csv'
    measured_device = '2023.11 TSMC 22nm TEG'
    device_id = 2
    temperature_k = 300

    start_time = datetime.now()
    date = start_time.strftime('%Y%m%d')
    start_time_formatted = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    result = advance_test.three_way_sweep(17, 2, 1, 0, 0.0,
                                          0.8, 41, 0.1,
                                          None, 1, 0, 0.0,
                                          0.8, 41, 0.1, 4,
                                          0, 0, -0.8,
                                          41, 0.1, 3,
                                          0, 0, 0.1,
                                          None, None)

    end_time = datetime.now()
    end_time_formatted = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    comment = [
        'Measurement Date: ' + date,
        'Measured Device: ' + measured_device,
        'Device ID: ' + str(device_id),
        'Start Time' + start_time_formatted,
        'End Time' + end_time_formatted,
        'Temperature' + str(temperature_k),
    ]

    with open(output_file_path, mode='w') as output_file:
        for comment in comment:
            output_file.write('# ', comment + '\n')

    result.to_csv(output_file_path, mode='a', header=False, index=False)

if __name__ == "__main__":
    test_gpib_command()
