# tests/test_gpib_command.py

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command import GPIBCommand


def test_gpib_command():
    gpib_comm = GPIBCommunication()
    gpib_command = GPIBCommand()

    # Initialize connection
    gpib_command.init_connection(gpib_id=17)

    # Set output format
    gpib_command.set_output_format(11, 1)

    # Query error
    gpib_command.query_error(mode=1)

    # Enable timer
    gpib_command.time_stamp(enable=True)

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
    gpib_command.set_measurement_mode(16, [1])

    # Query error
    gpib_command.query_error(mode=1)

    # Set SMU measurement mode
    gpib_command.set_smu_mode([1], 1)
    gpib_command.set_smu_mode([2], 1)

    # Query error
    gpib_command.query_error(mode=1)

    # Set current measuring range
    gpib_command.current_measurement_range(channel=1, current_range=-19)
    gpib_command.current_measurement_range(channel=2, current_range=-19)

    # Query error
    gpib_command.query_error(mode=1)

    # Set sweep delay time
    # gpib_command.sweep_delay(hold=0)

    # Set auto abort
    gpib_command.auto_abort(2, 1)

    # Query error
    gpib_command.query_error(mode=1)

    # Test enabling channels
    # gpib_command.enable_channels([1, 2])

    # Test disabling channels
    # gpib_command.disable_channels([3, 4])

    # Test setting voltage sweep
    gpib_command.set_voltage_sweep(channel=1, mode=1, v_range=0, start=0.0, stop=1.0, step=20, icomp=0.01)

    # Query error
    gpib_command.query_error(mode=1)

    # Test forcing voltage
    gpib_command.force_voltage(channel=2, v_range=0, voltage=1.0, icomp=0.01)

    # Query error
    gpib_command.query_error(mode=1)

    # Test setting measurement mode
    # gpib_command.set_measurement_mode(mode=1, channels=[1])

    # Reset timer count
    gpib_command.reset_time(channels=[1])

    # Query error
    gpib_command.query_error(mode=1)

    # Test triggering measurement
    gpib_command.trigger_measurement()

    # Query error
    gpib_command.query_error(mode=1)

    # Wait for measurement complete
    print(gpib_command.wait_pending())

    # Query error
    gpib_command.query_error(mode=1)

    print(gpib_command.number_of_measurements())

    # Read the return data
    # print(gpib_comm.read_response())
    print(gpib_comm.read_response())

    # Query error
    gpib_command.query_error(mode=1)


if __name__ == "__main__":
    test_gpib_command()
