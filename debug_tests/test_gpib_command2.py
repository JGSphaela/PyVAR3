# tests/test_gpib_command.py
import time

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command import GPIBCommand
from src.tests.basic_test import BasicTest


def test_gpib_command():
    gpib_comm = GPIBCommunication()
    gpib_command = GPIBCommand()
    basic_test = BasicTest()
    gpib_comm.connect_device("GPIB0::17::INSTR")

    gpib_comm.device.timeout = None

    # Initialize connection
    gpib_command.init_connection(gpib_id=17)

    # Set output format
    gpib_command.set_output_format(11, 1)

    # Query error
    gpib_command.query_error(mode=1)

    # Enable timer
    gpib_command.time_stamp(enable=False)

    # Query error
    gpib_command.query_error(mode=1)

    # Set filter
    gpib_command.set_filter(True)

    # Query error
    gpib_command.query_error(mode=1)

    # Set sample averaging
    gpib_command.set_averaging(10, 1)

    # Query error
    gpib_command.query_error(mode=1)

    # Set measurement mode
    gpib_command.set_measurement_mode(2, [1, 2, 3, 4])

    # Query error
    gpib_command.query_error(mode=1)

    # Set SMU measurement mode
    gpib_command.set_smu_mode(1, 0)
    # Query error
    gpib_command.query_error(mode=1)
    gpib_command.set_smu_mode(2, 0)
    # Query error
    gpib_command.query_error(mode=1)
    gpib_command.set_smu_mode(3, 0)
    # Query error
    gpib_command.query_error(mode=1)
    gpib_command.set_smu_mode(4, 0)

    # Query error
    gpib_command.query_error(mode=1)

    # Set current measuring range
    for channel in range(1, 5):
        gpib_command.current_measurement_range(channel=channel, current_range=0)
        gpib_command.voltage_measurement_range(channel=channel, voltage_range=0)

    # Query error
    gpib_command.query_error(mode=1)

    # Set sweep delay time
    # gpib_command.sweep_delay(hold=0)

    # Set auto abort
    gpib_command.auto_abort(2, 1)

    # Query error
    gpib_command.query_error(mode=1)

    # # Test enabling channels
    # gpib_command.enable_channels([1, 2, 3, 4])
    #
    # # Test disabling channels
    # # gpib_command.disable_channels([3, 4])
    #
    # # Test setting voltage sweep
    # gpib_command.set_voltage_sweep(channel=2, mode=1, v_range=0, start=0.0, stop=1.0, step=21, icomp=0.01)
    #
    # # Query error
    # gpib_command.query_error(mode=1)
    #
    # # Test forcing voltage
    # gpib_command.force_voltage(channel=1, v_range=0, voltage=1.0, icomp=0.01)
    # gpib_command.force_voltage(channel=3, v_range=0, voltage=1.0, icomp=0.01)
    # gpib_command.force_voltage(channel=4, v_range=0, voltage=1.0, icomp=0.01)

    basic_test.multichannel_sweep_voltage(17, 2, 1, 0, 0.0, 1.0,
                                          21, 0.01, None,
                                          1, 0, 1, None,
                                          None, None, 2,
                                          0, 1, None,
                                          None, None, 3,
                                          0, 1, None,
                                          None, None,)

    # Query error
    gpib_command.query_error(mode=1)

    # Test setting measurement mode
    # gpib_command.set_measurement_mode(mode=1, channels=[1])

    # Reset timer count
    # gpib_command.reset_time(channels=[1])

    # Query error
    # gpib_command.query_error(mode=1)

    # Test triggering measurement
    gpib_command.trigger_measurement()

    # Wait for measurement complete
    print(gpib_command.wait_pending())

    # Query error
    gpib_command.query_error(mode=1)

    print(gpib_command.number_of_measurements())

    # Read the return data
    print(gpib_comm.read_response())

    # Query error
    gpib_command.query_error(mode=1)

    # Reset all channels
    gpib_command.reset_channel()

    # Query error
    gpib_command.query_error(mode=1)


if __name__ == "__main__":
    test_gpib_command()
