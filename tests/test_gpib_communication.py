"""Tests for GPIBCommunication — the core PyVISA wrapper."""

import pytest
from unittest.mock import patch
import pyvisa

from src.gpib.gpib_communication import GPIBCommunication
from src.gpib.exceptions import DeviceNotConnectedError, GPIBError


class TestGPIBCommunicationInit:
    def test_init_success(self):
        with patch('src.gpib.gpib_communication.pyvisa.ResourceManager'):
            comm = GPIBCommunication()
            assert comm.rm is not None
            assert comm.device is None

    def test_init_failure(self):
        with patch('src.gpib.gpib_communication.pyvisa.ResourceManager', side_effect=ValueError("no visa")):
            comm = GPIBCommunication()
            assert comm.rm is None


class TestConnectDevice:
    def test_connect_success(self, mock_communication, mock_device):
        mock_communication.device = None  # Reset
        mock_communication.connect_device("GPIB0::17::INSTR")
        mock_communication.rm.open_resource.assert_called_with("GPIB0::17::INSTR")
        assert mock_communication.device is not None

    def test_connect_no_resource_manager(self):
        with patch('src.gpib.gpib_communication.pyvisa.ResourceManager', side_effect=ValueError("no visa")):
            comm = GPIBCommunication()
            with pytest.raises(DeviceNotConnectedError, match="ResourceManager not initialized"):
                comm.connect_device("GPIB0::17::INSTR")

    def test_connect_visa_error(self, mock_communication):
        mock_communication.rm.open_resource.side_effect = pyvisa.VisaIOError(-1)
        with pytest.raises(GPIBError, match="Failed to connect"):
            mock_communication.connect_device("GPIB0::99::INSTR")


class TestSendCommand:
    def test_send_success(self, mock_communication, mock_device):
        mock_communication.send_command("*RST")
        mock_device.write.assert_called_with("*RST")

    def test_send_no_device(self, mock_communication):
        mock_communication.device = None
        with pytest.raises(DeviceNotConnectedError, match="No device connected"):
            mock_communication.send_command("*RST")

    def test_send_visa_error(self, mock_communication, mock_device):
        mock_device.write.side_effect = pyvisa.VisaIOError(-1)
        with pytest.raises(GPIBError, match="Failed to send command"):
            mock_communication.send_command("*RST")


class TestReadResponse:
    def test_read_success(self, mock_communication, mock_device):
        mock_device.read.return_value = "Hello\r\n"
        result = mock_communication.read_response()
        assert result == "Hello\r\n"

    def test_read_no_device(self, mock_communication):
        mock_communication.device = None
        with pytest.raises(DeviceNotConnectedError, match="No device connected"):
            mock_communication.read_response()

    def test_read_visa_error(self, mock_communication, mock_device):
        mock_device.read.side_effect = pyvisa.VisaIOError(-1)
        with pytest.raises(GPIBError, match="Failed to read response"):
            mock_communication.read_response()


class TestQueryResponse:
    def test_query_success(self, mock_communication, mock_device):
        mock_device.query.return_value = "0,0,0,0\r\n"
        result = mock_communication.query_response("ERR?")
        assert result == "0,0,0,0\r\n"
        mock_device.query.assert_called_with("ERR?")

    def test_query_no_device(self, mock_communication):
        mock_communication.device = None
        with pytest.raises(DeviceNotConnectedError, match="No device connected"):
            mock_communication.query_response("ERR?")


class TestReadAscii:
    def test_read_ascii_success(self, mock_communication, mock_device):
        mock_device.read_ascii_values.return_value = [1.234, 5.678]
        result = mock_communication.read_ascii()
        assert result == [1.234, 5.678]

    def test_read_ascii_no_device(self, mock_communication):
        mock_communication.device = None
        with pytest.raises(DeviceNotConnectedError, match="No device connected"):
            mock_communication.read_ascii()
