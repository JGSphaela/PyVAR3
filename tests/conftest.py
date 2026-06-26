"""Shared test fixtures for PyVAR3 test suite."""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_device():
    """A mock PyVISA instrument device."""
    device = MagicMock()
    device.read.return_value = "WWA+1.23456E+00\r\n"
    device.query.return_value = "0,0,0,0\r\n"
    device.write.return_value = None
    device.read_ascii_values.return_value = [1.23456]
    return device


@pytest.fixture
def mock_communication(mock_device):
    """A GPIBCommunication instance with a mocked device and resource manager."""
    with patch('src.gpib.gpib_communication.pyvisa.ResourceManager') as mock_rm_cls:
        mock_rm = MagicMock()
        mock_rm.open_resource.return_value = mock_device
        mock_rm_cls.return_value = mock_rm
        from src.gpib.gpib_communication import GPIBCommunication
        comm = GPIBCommunication()
        comm.device = mock_device
        comm.rm = mock_rm
        return comm


@pytest.fixture
def mock_b1500(mock_communication):
    """A B1500GPIBCommand instance with mocked communication."""
    with patch('src.gpib.gpib_command_b1500.GPIBCommunication', return_value=mock_communication):
        from src.gpib.gpib_command_b1500 import B1500GPIBCommand
        cmd = B1500GPIBCommand()
        cmd.communication = mock_communication
        return cmd


@pytest.fixture
def mock_model335(mock_communication):
    """A Model335GPIBCommand instance with mocked communication."""
    with patch('src.gpib.gpib_command_model335.GPIBCommunication', return_value=mock_communication):
        from src.gpib.gpib_command_model335 import Model335GPIBCommand
        cmd = Model335GPIBCommand()
        cmd.communication = mock_communication
        return cmd


@pytest.fixture
def sample_b1500_response():
    """Raw B1500 response string — 2 sweep steps with 4 channels (A, B, C, D)."""
    return (
        "WWA+1.00000E-06,WWD+1.00000E+00,WVB+1.00000E-06,WVD+5.00000E-01,"
        "WWA+2.00000E-06,WWD+1.00000E+00,WVB+2.00000E-06,WVD+5.00000E-01,"
        "EWA+3.00000E-06,EWD+1.00000E+00,EWB+3.00000E-06,EWD+5.00000E-01"
    )


@pytest.fixture
def sample_b1500_single_step():
    """Raw B1500 response for a single sweep step (only E status)."""
    return "EWA+1.50000E-06,EWD+2.00000E+00,EWB+3.00000E-07,EWD+1.00000E+00"
