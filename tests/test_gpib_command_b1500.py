"""Tests for B1500GPIBCommand — B1500 SCPI command builder.

Includes regression tests for:
- Bug 1: set_output_format sends "FMT 11,None" when mode is None
- Bug 5: set_auto_zero has dead command variable
- Bug 7: sweep_delay falsy checks fail when value is 0
"""

import pytest
from unittest.mock import MagicMock, patch

from src.gpib.gpib_command_b1500 import B1500GPIBCommand
from src.gpib.exceptions import InstrumentError, VoltageLimitError


@pytest.fixture
def b1500(mock_communication):
    """B1500GPIBCommand with mocked communication, already connected."""
    cmd = B1500GPIBCommand()
    cmd.communication = mock_communication
    return cmd


class TestInitConnection:
    def test_init_connection_address_format(self, b1500, mock_communication):
        mock_communication.device = MagicMock()
        with patch.object(mock_communication, 'connect_device') as mock_connect:
            b1500.init_connection(gpib_id=17)
            mock_connect.assert_called_once_with("GPIB0::17::INSTR")

    def test_init_connection_default_id(self, b1500, mock_communication, mock_device):
        mock_communication.device = MagicMock()
        with patch.object(mock_communication, 'connect_device') as mock_connect:
            b1500.init_connection()
            mock_connect.assert_called_once_with("GPIB0::17::INSTR")


class TestCheckError:
    def test_check_error_ok(self, b1500, mock_device):
        mock_device.query.return_value = "0,0,0,0\r\n"
        b1500.check_error()  # Should not raise

    def test_check_error_raises(self, b1500, mock_device):
        mock_device.query.return_value = "1,101,0,0\r\n"
        with pytest.raises(InstrumentError, match="B1500 Error"):
            b1500.check_error()


class TestEnableDisableChannels:
    def test_enable_channels(self, b1500, mock_device):
        b1500.enable_channels([1, 2, 3])
        mock_device.write.assert_called_with("CN 1,2,3")

    def test_enable_channels_none(self, b1500, mock_device):
        b1500.enable_channels()
        mock_device.write.assert_called_with("CN")

    def test_disable_channels(self, b1500, mock_device):
        b1500.disable_channels([1, 2])
        mock_device.write.assert_called_with("CL 1,2")


class TestVoltageSweep:
    def test_set_voltage_sweep(self, b1500, mock_device):
        b1500.set_voltage_sweep(channel=1, mode=1, v_range=0, start=0.0, stop=1.0, step=101)
        mock_device.write.assert_called_with("WV 1,1,0,0.0,1.0,101")

    def test_set_voltage_sweep_with_compliance(self, b1500, mock_device):
        b1500.set_voltage_sweep(channel=1, mode=1, v_range=0, start=0.0, stop=1.0, step=101, icomp=0.01, pcomp=0.1)
        mock_device.write.assert_called_with("WV 1,1,0,0.0,1.0,101,0.01,0.1")

    def test_set_voltage_sweep_limit_exceeded(self, b1500):
        with pytest.raises(VoltageLimitError, match="exceeds limit"):
            b1500.set_voltage_sweep(channel=1, mode=1, v_range=0, start=0.0, stop=3.0, step=101)

    def test_set_voltage_sweep_start_limit_exceeded(self, b1500):
        """Start voltage is now also checked against the limit."""
        with pytest.raises(VoltageLimitError, match="exceeds limit"):
            b1500.set_voltage_sweep(channel=1, mode=1, v_range=0, start=-3.0, stop=0.0, step=101)

    def test_set_voltage_sweep_custom_limit(self, mock_communication):
        """Voltage limit is configurable via constructor."""
        from unittest.mock import MagicMock
        cmd = B1500GPIBCommand(voltage_limit=5.0)
        cmd.communication = mock_communication
        # 3.0V should be OK with 5V limit
        cmd.set_voltage_sweep(channel=1, mode=1, v_range=0, start=0.0, stop=3.0, step=101)


class TestForceVoltage:
    def test_force_voltage(self, b1500, mock_device):
        """comp_polarity defaults to 0, so it appears in the command."""
        b1500.force_voltage(channel=1, v_range=0, voltage=1.0)
        mock_device.write.assert_called_with("DV 1,0,1.0,0")

    def test_force_voltage_with_compliance(self, b1500, mock_device):
        b1500.force_voltage(channel=1, v_range=0, voltage=0.5, icomp=0.01)
        mock_device.write.assert_called_with("DV 1,0,0.5,0.01,0")

    def test_force_voltage_limit_exceeded(self, b1500):
        with pytest.raises(VoltageLimitError, match="exceeds limit"):
            b1500.force_voltage(channel=1, v_range=0, voltage=2.5)

    def test_set_voltage_limit_runtime(self, b1500):
        """Voltage limit can be changed at runtime."""
        b1500.set_voltage_limit(5.0)
        assert b1500.voltage_limit == 5.0


class TestSetOutputFormat:
    """Regression test for Bug 1: 'FMT 11,None' when mode is None."""

    def test_set_output_format_with_mode(self, b1500, mock_device):
        b1500.set_output_format(out_format=11, mode=1)
        mock_device.write.assert_called_with("FMT 11,1")

    def test_set_output_format_no_mode(self, b1500, mock_device):
        """Bug 1 regression: mode=None should NOT produce 'FMT 11,None'."""
        b1500.set_output_format(out_format=11, mode=None)
        mock_device.write.assert_called_with("FMT 11")
        # Verify the invalid command was NOT sent
        for call in mock_device.write.call_args_list:
            assert "None" not in call[0][0]

    def test_set_output_format_defaults(self, b1500, mock_device):
        b1500.set_output_format()
        mock_device.write.assert_called_with("FMT 11")


class TestSetMeasurementMode:
    def test_set_measurement_mode_with_channels(self, b1500, mock_device):
        b1500.set_measurement_mode(mode=16, channels=[1, 2, 3])
        mock_device.write.assert_called_with("MM 16,1,2,3")

    def test_set_measurement_mode_no_channels(self, b1500, mock_device):
        b1500.set_measurement_mode(mode=16)
        mock_device.write.assert_called_with("MM 16")


class TestSweepDelay:
    """Regression test for Bug 7: falsy checks fail when value is 0."""

    def test_sweep_delay_defaults(self, b1500, mock_device):
        b1500.sweep_delay()
        mock_device.write.assert_called_with("WT 0,0")

    def test_sweep_delay_with_values(self, b1500, mock_device):
        b1500.sweep_delay(hold=1.0, delay=0.5, sdelay=0.1)
        mock_device.write.assert_called_with("WT 1.0,0.5,0.1")

    def test_sweep_delay_with_zero_values(self, b1500, mock_device):
        """Bug 7 regression: explicit 0 values must be included in command."""
        b1500.sweep_delay(hold=0, delay=0, sdelay=0, tdelay=0, mdelay=0)
        cmd = mock_device.write.call_args[0][0]
        assert cmd == "WT 0,0,0,0,0"


class TestSetAutoZero:
    """Regression test for Bug 5: dead command variable."""

    def test_set_auto_zero(self, b1500, mock_device):
        b1500.set_auto_zero(mode=1)
        mock_device.write.assert_called_with("AZ 1")

    def test_set_auto_zero_default(self, b1500, mock_device):
        b1500.set_auto_zero()
        mock_device.write.assert_called_with("AZ 0")


class TestFilter:
    def test_set_filter(self, b1500, mock_device):
        b1500.set_filter(mode=True, channels=[1, 2, 3])
        mock_device.write.assert_called_with("FL 1 1,2,3")


class TestAveraging:
    def test_set_averaging(self, b1500, mock_device):
        b1500.set_averaging(number=10)
        mock_device.write.assert_called_with("AV 10")

    def test_set_averaging_with_mode(self, b1500, mock_device):
        b1500.set_averaging(number=10, mode=1)
        mock_device.write.assert_called_with("AV 10,1")


class TestTriggerMeasurement:
    def test_trigger(self, b1500, mock_device):
        mock_device.query.return_value = "some_data"
        result = b1500.trigger_measurement()
        mock_device.query.assert_called_with("XE")
        assert result == "some_data"


class TestVoltageMeasurementRange:
    def test_docstring_says_voltage(self, b1500):
        """Verify the docstring was fixed (was incorrectly saying 'current')."""
        assert "voltage" in b1500.voltage_measurement_range.__doc__.lower()
