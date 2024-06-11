# tests/test_gpib_command.py

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.gpib_command import GPIBCommand


def test_gpib_command():
    gpib_comm = GPIBCommunication()
    gpib_command = GPIBCommand(gpib_comm)

    # Test enabling channels
    gpib_command.enable_channels([1, 2, 3])

    # Test disabling channels
    gpib_command.disable_channels([1, 2, 3])

    # Test setting voltage sweep
    gpib_command.set_voltage_sweep(channel=1, mode=1, v_range=0, start=0.0, stop=5.0, step=0.1, icomp=0.01)

    # Test forcing voltage
    gpib_command.force_voltage(channel=1, v_range=0, voltage=5.0, icomp=0.01)

    # Test setting measurement mode
    gpib_command.set_measurement_mode(mode=1, channels=[1])

    # Test triggering measurement
    gpib_command.trigger_measurement()


if __name__ == "__main__":
    test_gpib_command()
