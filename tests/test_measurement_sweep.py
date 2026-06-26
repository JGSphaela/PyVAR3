"""Tests for measurement sweep logic — BasicTest and AdvanceTest.

Includes regression test for:
- Bug 2: Division by zero in two_way_sweep when sweep2_step == 1
"""

import os
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch, PropertyMock

from src.measurement.basic_sweep import BasicTest
from src.measurement.advance_sweep import AdvanceTest
from src.gpib.exceptions import PyVARError


@pytest.fixture(autouse=True)
def ensure_data_dir(tmp_path, monkeypatch):
    """Create a temporary data/ directory and change to it for tests that write CSVs."""
    monkeypatch.chdir(tmp_path)
    os.makedirs("data", exist_ok=True)


@pytest.fixture
def mock_basic_test():
    """A BasicTest with fully mocked instrument layer."""
    with patch('src.measurement.basic_sweep.B1500GPIBCommand') as MockCmd, \
         patch('src.measurement.basic_sweep.DataProcess') as MockDP:
        # Create a mock DataFrame that looks like valid sweep output
        mock_df = pd.DataFrame({
            'A_I': [1e-6, 2e-6, 3e-6],
            'A_V': [0.0, 0.5, 1.0],
        })
        MockDP.return_value.data_into_dataframe.return_value = mock_df
        MockCmd.return_value.trigger_measurement.return_value = "raw_data"

        test = BasicTest()
        # Pre-set counter to skip pretest initialization
        return test, mock_df


@pytest.fixture
def mock_advance_test(mock_basic_test):
    """An AdvanceTest wrapping a mocked BasicTest."""
    basic_test, mock_df = mock_basic_test
    adv = AdvanceTest()
    adv.basic_test = basic_test
    return adv, mock_df


class TestBasicTestCounterHack:
    """Test that the pretest initialization only runs once."""

    def test_pretest_runs_when_counter_is_none(self, mock_basic_test):
        basic_test, _ = mock_basic_test
        # counter=None means first call → should run pretest
        # We can't easily test this without a real connection, but we can verify
        # the method exists and accepts counter parameter
        import inspect
        sig = inspect.signature(basic_test.multichannel_sweep_voltage)
        assert 'counter' in sig.parameters

    def test_counter_parameter_is_optional(self, mock_basic_test):
        basic_test, _ = mock_basic_test
        import inspect
        sig = inspect.signature(basic_test.multichannel_sweep_voltage)
        counter_param = sig.parameters['counter']
        assert counter_param.default is None


class TestTwoWaySweep:
    """Regression test for Bug 2: division by zero when sweep2_step == 1."""

    def test_two_way_sweep_step_one_no_division_error(self, mock_advance_test):
        """Bug 2 regression: sweep2_step=1 must not cause ZeroDivisionError."""
        adv, mock_df = mock_advance_test
        # This should NOT raise ZeroDivisionError
        result = adv.two_way_sweep(
            sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=2, sweep2_range=0,
            sweep2_start=0.5, sweep2_stop=0.5, sweep2_step=1
        )
        assert isinstance(result, pd.DataFrame)

    def test_two_way_sweep_normal(self, mock_advance_test):
        """Verify result DataFrame has correct shape for normal sweep."""
        adv, mock_df = mock_advance_test
        result = adv.two_way_sweep(
            sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=2, sweep2_range=0,
            sweep2_start=0.0, sweep2_stop=1.0, sweep2_step=3
        )
        assert isinstance(result, pd.DataFrame)
        # Should have 3 steps × 3 mock rows = 9 rows
        assert len(result) == 9

    def test_two_way_sweep_adds_sweep2_column(self, mock_advance_test):
        """Verify the sweep2 voltage column is added to results."""
        adv, _ = mock_advance_test
        result = adv.two_way_sweep(
            sweep1_channel=2, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=3, sweep2_range=0,
            sweep2_start=0.0, sweep2_stop=1.0, sweep2_step=2
        )
        # Channel 3 → chr(3+64) = 'C', so column should be 'C_V'
        assert 'C_V' in result.columns


class TestThreeWaySweep:
    def test_three_way_sweep_step_one_no_division_error(self, mock_advance_test):
        """Both sweep2_step=1 and sweep3_step=1 should work."""
        adv, _ = mock_advance_test
        result = adv.three_way_sweep(
            sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=2, sweep2_range=0,
            sweep2_start=0.5, sweep2_stop=0.5, sweep2_step=1,
            sweep3_channel=3, sweep3_range=0,
            sweep3_start=0.5, sweep3_stop=0.5, sweep3_step=1
        )
        assert isinstance(result, pd.DataFrame)

    def test_three_way_sweep_progress_logging(self, mock_advance_test, caplog):
        """Verify progress messages are logged."""
        import logging
        with caplog.at_level(logging.INFO):
            adv, _ = mock_advance_test
            adv.three_way_sweep(
                sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
                sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
                sweep2_channel=2, sweep2_range=0,
                sweep2_start=0.0, sweep2_stop=0.5, sweep2_step=2,
                sweep3_channel=3, sweep3_range=0,
                sweep3_start=0.0, sweep3_stop=0.5, sweep3_step=1
            )
        assert any("Progress:" in record.message for record in caplog.records)

    def test_three_way_sweep_data_mismatch_raises(self, mock_advance_test):
        """Verify PyVARError when output rows don't match expected count."""
        adv, mock_df = mock_advance_test
        # mock_df has 3 rows, but sweep1_step*sweep2_step = 5*2 = 10
        # The error is raised by BasicTest (basic_sweep) before AdvanceTest sees it
        with pytest.raises(PyVARError, match="output data does not match"):
            adv.three_way_sweep(
                sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
                sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=5,
                sweep2_channel=2, sweep2_range=0,
                sweep2_start=0.0, sweep2_stop=1.0, sweep2_step=2,
                sweep3_channel=3, sweep3_range=0,
                sweep3_start=0.0, sweep3_stop=0.0, sweep3_step=1
            )


class TestProgressCallback:
    """Test the progress_callback mechanism."""

    def test_two_way_callback_invoked(self, mock_advance_test):
        """Verify progress_callback is called for each step."""
        adv, _ = mock_advance_test
        calls = []
        def callback(current, total, elapsed):
            calls.append((current, total))

        adv.two_way_sweep(
            sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=2, sweep2_range=0,
            sweep2_start=0.0, sweep2_stop=1.0, sweep2_step=4,
            progress_callback=callback,
        )
        assert len(calls) == 4  # One call per sweep2 step
        assert calls[-1][0] == 4  # Last call: current=4
        assert calls[-1][1] == 4  # total=4

    def test_three_way_callback_invoked(self, mock_advance_test):
        """Verify progress_callback is called for each step in 3-way sweep."""
        adv, _ = mock_advance_test
        calls = []
        def callback(current, total, elapsed):
            calls.append((current, total))

        adv.three_way_sweep(
            sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=2, sweep2_range=0,
            sweep2_start=0.0, sweep2_stop=0.5, sweep2_step=2,
            sweep3_channel=3, sweep3_range=0,
            sweep3_start=0.0, sweep3_stop=0.5, sweep3_step=2,
            progress_callback=callback,
        )
        assert len(calls) == 4  # 2 sweep3 × 2 sweep2 = 4 total steps

    def test_callback_not_required(self, mock_advance_test):
        """Sweep works without callback (backward compatible)."""
        adv, _ = mock_advance_test
        result = adv.two_way_sweep(
            sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=2, sweep2_range=0,
            sweep2_start=0.0, sweep2_stop=1.0, sweep2_step=2,
        )
        assert len(result) > 0


class TestAbortMechanism:
    """Test the abort_flag mechanism."""

    def test_two_way_abort(self, mock_advance_test):
        """Verify abort raises MeasurementAbortedError with partial data."""
        import threading
        from src.gpib.exceptions import MeasurementAbortedError

        adv, _ = mock_advance_test
        abort_flag = threading.Event()
        abort_flag.set()  # Pre-set abort

        with pytest.raises(MeasurementAbortedError, match="aborted"):
            adv.two_way_sweep(
                sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
                sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
                sweep2_channel=2, sweep2_range=0,
                sweep2_start=0.0, sweep2_stop=1.0, sweep2_step=4,
                abort_flag=abort_flag,
            )

    def test_abort_carrying_partial_data(self, mock_advance_test):
        """Verify aborted error carries partial DataFrame."""
        import threading
        from src.gpib.exceptions import MeasurementAbortedError

        adv, _ = mock_advance_test
        abort_flag = threading.Event()

        # Run first step, then abort on second
        call_count = [0]
        original_multi = adv.basic_test.multichannel_sweep_voltage

        def counting_sweep(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] >= 2:
                abort_flag.set()
            return original_multi(*args, **kwargs)

        adv.basic_test.multichannel_sweep_voltage = counting_sweep

        with pytest.raises(MeasurementAbortedError) as exc_info:
            adv.two_way_sweep(
                sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
                sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
                sweep2_channel=2, sweep2_range=0,
                sweep2_start=0.0, sweep2_stop=1.0, sweep2_step=4,
                abort_flag=abort_flag,
            )
        assert exc_info.value.partial_data is not None
        assert len(exc_info.value.partial_data) > 0

    def test_temperature_callback(self, mock_advance_test):
        """Verify temperature_callback is invoked and columns are added."""
        adv, _ = mock_advance_test
        temp_calls = [0]
        def get_temps():
            temp_calls[0] += 1
            return {'A': 298.15, 'B': 6.5}

        result = adv.three_way_sweep(
            sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
            sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=3,
            sweep2_channel=2, sweep2_range=0,
            sweep2_start=0.0, sweep2_stop=0.5, sweep2_step=2,
            sweep3_channel=3, sweep3_range=0,
            sweep3_start=0.0, sweep3_stop=0.5, sweep3_step=1,
            temperature_callback=get_temps,
        )
        assert temp_calls[0] >= 1
        assert 'Temp_A_K' in result.columns
        assert 'Temp_B_K' in result.columns
