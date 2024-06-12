# tests/test_gpib_command.py

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command import GPIBCommand


def test_gpib_command():
    gpib_comm = GPIBCommunication()
    gpib_command = GPIBCommand(gpib_comm)
    gpib_comm.connect_device("GPIB0::17::INSTR")

    # Set output format
    gpib_command.set_output_format(1, 1)

    # Enable timer
    gpib_command.time_stamp(enable=True)

    # Set measurement mode
    gpib_command.set_measurement_mode(16, [1])

    # Test enabling channels
    gpib_command.enable_channels([1, 2])

    # Test disabling channels
    gpib_command.disable_channels([3, 4])

    # Test setting voltage sweep
    gpib_command.set_voltage_sweep(channel=1, mode=1, v_range=0, start=0.0, stop=1.0, step=0.5, icomp=0.01)

    # Test forcing voltage
    gpib_command.force_voltage(channel=2, v_range=0, voltage=1.0, icomp=0.01)

    # Test setting measurement mode
    # gpib_command.set_measurement_mode(mode=1, channels=[1])

    # Reset timer count
    gpib_command.reset_time(channels=[1])

    # Test triggering measurement
    gpib_command.trigger_measurement()

    # Wait for measurement complete
    print(gpib_command.wait_pending())

    print(gpib_command.number_of_measurements())

    # Read the return data
    # print(gpib_comm.read_response())
    print(gpib_comm.read_ascii())


if __name__ == "__main__":
    test_gpib_command()
