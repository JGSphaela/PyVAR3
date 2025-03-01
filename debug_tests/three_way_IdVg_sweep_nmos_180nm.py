# debug_tests/three_way_IdVg_sweep.py
from src.tests.advance_test import AdvanceTest
from datetime import datetime


def test_gpib_command():
    advance_test = AdvanceTest()

    measured_device = '20240626 TSMC 180nm TEG'
    device_id = 14
    temperature_k = 6.5
    output_file_path = 'data/' + measured_device + str(device_id) + ' ' + str(temperature_k) + 'K.csv'
    sweep_parameter = '\n#    Vg:[0V ~ 1.8V steps:37]\n#    Vd:[0V ~ 1.8V steps:37]\n#    Vsub:[0.4V ~ -0.4V steps:9]'
    const_parameter = '\n#    Vsource:[0V]\n#    VDD:[1.8V]\n#    GND:[0V]'

    start_time = datetime.now()
    date = start_time.strftime('%Y-%m-%d')
    start_time_formatted = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]

    smu_vdd = 1
    smu_drain = 3
    smu_gate = 4
    smu_source = 5
    smu_bulk = 2

    smu_offset = 2

    if smu_offset:
        smu_vdd = smu_vdd + smu_offset
        smu_drain = smu_drain + smu_offset
        smu_gate = smu_gate + smu_offset
        smu_source = smu_source + smu_offset
        smu_bulk = smu_bulk + smu_offset

    print(smu_drain)

    result = advance_test.three_way_sweep(17, smu_gate, 1, 0, 0.0,
                                          1.8, 37, 0.01,
                                          None, smu_drain, 0, 0.0,
                                          1.8, 37, 0.01, smu_bulk,
                                          0, 0.4, -0.4,
                                          9, 0.01, smu_source,
                                          0, 0, 0.01,
                                          None, None, smu_vdd, 0,
                                          1.8, 0.01, None,
                                          None)

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
        output_file.write('Vdd_I,Sub_I,Drain_I,Gate_I,Source_I,Gate_V,Drain_V,Sub_V\n')

    result.to_csv(output_file_path, mode='a', header=False, index=False)


if __name__ == "__main__":
    test_gpib_command()
