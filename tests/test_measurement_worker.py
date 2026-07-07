"""Tests for GUI measurement worker cleanup signaling."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd

from src.gpib.exceptions import MeasurementAbortedError, PyVARError
from src.gui.measurement_worker import MeasurementWorker
from src.measurement.config import MeasurementConfig, SweepChannelConfig


def _config() -> MeasurementConfig:
    return MeasurementConfig(
        sweep_channels=[
            SweepChannelConfig(channel=1, start=0.0, stop=0.1, step=2),
            SweepChannelConfig(channel=2, start=0.0, stop=0.1, step=2),
        ]
    )


class _FakeAdvanceTest:
    def __init__(self, *, result=None, exc=None, reset_exc=None, session_open=True):
        self.result = result if result is not None else pd.DataFrame({"A_I": [1e-9]})
        self.exc = exc
        self.basic_test = MagicMock()
        self.basic_test.command.communication.device = object() if session_open else None
        if reset_exc is not None:
            self.basic_test.command.reset_channel.side_effect = reset_exc

    def two_way_sweep(self, **kwargs):
        if self.exc is not None:
            raise self.exc
        return self.result

    def three_way_sweep(self, **kwargs):
        if self.exc is not None:
            raise self.exc
        return self.result


def test_worker_surfaces_reset_failure_after_success():
    result = pd.DataFrame({"A_I": [1e-9, 2e-9]})
    fake = _FakeAdvanceTest(result=result, reset_exc=RuntimeError("DZ failed"))
    worker = MeasurementWorker(_config())
    emitted_results = []
    emitted_reset_errors = []
    events = []
    worker.result_ready.connect(lambda value: (emitted_results.append(value), events.append("result")))
    worker.reset_failed.connect(lambda value: (emitted_reset_errors.append(value), events.append("reset_failed")))

    with patch("src.gui.measurement_worker.AdvanceTest", return_value=fake):
        worker.run()

    assert emitted_results == [result]
    assert len(emitted_reset_errors) == 1
    assert events == ["result", "reset_failed"]
    assert "DZ failed" in emitted_reset_errors[0]
    assert "may still be biasing the DUT" in emitted_reset_errors[0]


def test_worker_surfaces_reset_failure_while_preserving_partial_abort_data():
    partial = pd.DataFrame({"A_I": [1e-9]})
    fake = _FakeAdvanceTest(
        exc=MeasurementAbortedError("user abort", partial_data=partial),
        reset_exc=RuntimeError("GPIB dropped"),
    )
    worker = MeasurementWorker(_config())
    emitted_partial = []
    emitted_reset_errors = []
    events = []
    worker.aborted_with_data.connect(lambda value: (emitted_partial.append(value), events.append("partial")))
    worker.reset_failed.connect(lambda value: (emitted_reset_errors.append(value), events.append("reset_failed")))

    with patch("src.gui.measurement_worker.AdvanceTest", return_value=fake):
        worker.run()

    assert emitted_partial == [partial]
    assert len(emitted_reset_errors) == 1
    assert events == ["partial", "reset_failed"]
    assert "GPIB dropped" in emitted_reset_errors[0]


def test_worker_surfaces_reset_failure_on_measurement_error():
    fake = _FakeAdvanceTest(exc=PyVARError("bad row count"), reset_exc=RuntimeError("DZ timeout"))
    worker = MeasurementWorker(_config())
    emitted_errors = []
    emitted_reset_errors = []
    events = []
    worker.error.connect(lambda value: (emitted_errors.append(value), events.append("error")))
    worker.reset_failed.connect(lambda value: (emitted_reset_errors.append(value), events.append("reset_failed")))

    with patch("src.gui.measurement_worker.AdvanceTest", return_value=fake):
        worker.run()

    assert emitted_errors == ["bad row count"]
    assert len(emitted_reset_errors) == 1
    assert events == ["error", "reset_failed"]
    assert "DZ timeout" in emitted_reset_errors[0]


def test_worker_skips_reset_warning_when_no_instrument_session_opened():
    fake = _FakeAdvanceTest(exc=PyVARError("connection failed"), session_open=False)
    worker = MeasurementWorker(_config())
    emitted_errors = []
    emitted_reset_errors = []
    worker.error.connect(emitted_errors.append)
    worker.reset_failed.connect(emitted_reset_errors.append)

    with patch("src.gui.measurement_worker.AdvanceTest", return_value=fake):
        worker.run()

    assert emitted_errors == ["connection failed"]
    assert emitted_reset_errors == []
    fake.basic_test.command.reset_channel.assert_not_called()


def test_worker_skips_reset_warning_on_abort_before_first_instrument_session():
    fake = _FakeAdvanceTest(
        exc=MeasurementAbortedError("pre-step abort", partial_data=pd.DataFrame()),
        session_open=False,
    )
    worker = MeasurementWorker(_config())
    emitted_aborts = []
    emitted_reset_errors = []
    worker.aborted.connect(lambda: emitted_aborts.append("aborted"))
    worker.reset_failed.connect(emitted_reset_errors.append)

    with patch("src.gui.measurement_worker.AdvanceTest", return_value=fake):
        worker.run()

    assert emitted_aborts == ["aborted"]
    assert emitted_reset_errors == []
    fake.basic_test.command.reset_channel.assert_not_called()
