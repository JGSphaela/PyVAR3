"""Tests for Model335GPIBCommand — Lakeshore Model 335 temperature controller."""

import pytest
from unittest.mock import MagicMock, patch

from src.gpib.gpib_command_model335 import Model335GPIBCommand


@pytest.fixture
def model335(mock_communication):
    """Model335GPIBCommand with mocked communication."""
    cmd = Model335GPIBCommand()
    cmd.communication = mock_communication
    return cmd


class TestInitConnection:
    def test_init_connection_address_format(self, model335, mock_communication):
        mock_communication.device = MagicMock()
        with patch.object(mock_communication, 'connect_device') as mock_connect:
            model335.init_connection(gpib_id=12)
            mock_connect.assert_called_once_with("GPIB0::12::INSTR")

    def test_init_connection_custom_id(self, model335, mock_communication):
        mock_communication.device = MagicMock()
        with patch.object(mock_communication, 'connect_device') as mock_connect:
            model335.init_connection(gpib_id=5)
            mock_connect.assert_called_once_with("GPIB0::5::INSTR")


class TestQueryTemperature:
    def test_query_celsius_default_channel(self, model335, mock_device):
        mock_device.query.return_value = "+25.0\r\n"
        result = model335.query_celsius()
        mock_device.query.assert_called_with("CRDG? A")
        assert result == "+25.0\r\n"

    def test_query_celsius_channel_b(self, model335, mock_device):
        mock_device.query.return_value = "+120.5\r\n"
        assert model335.query_celsius(input_channel="B") == "+120.5\r\n"
        mock_device.query.assert_called_with("CRDG? B")

    def test_query_kelvin_default_channel(self, model335, mock_device):
        mock_device.query.return_value = "+298.15\r\n"
        result = model335.query_kelvin()
        mock_device.query.assert_called_with("KRDG? A")
        assert result == "+298.15\r\n"

    def test_query_kelvin_channel_b(self, model335, mock_device):
        mock_device.query.return_value = "+6.50\r\n"
        assert model335.query_kelvin(input_channel="B") == "+6.50\r\n"
        mock_device.query.assert_called_with("KRDG? B")
