# tests/test_gpib.py

from src.gpib.gpib_communication import GPIBCommunication


def test_gpib_communication():
    gpib_comm = GPIBCommunication()
    print(gpib_comm.rm.list_resources())
    # gpib_comm.connect_device("GPIB0::1::INSTR")
    gpib_comm.send_command("*IDN?")
    response = gpib_comm.read_response()
    print(response)


if __name__ == "__main__":
    test_gpib_communication()
