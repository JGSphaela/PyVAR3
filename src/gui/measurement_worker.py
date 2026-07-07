"""QThread worker for running measurements in the background.

Runs AdvanceTest sweep methods in a separate thread so the GUI remains
responsive during long measurements. Emits signals for progress, completion,
errors, and abort.
"""

import logging
import threading

from PySide6.QtCore import QThread, Signal

from src.gpib.exceptions import MeasurementAbortedError, PyVARError
from src.measurement.advance_sweep import AdvanceTest
from src.measurement.config import MeasurementConfig

logger = logging.getLogger(__name__)


class MeasurementWorker(QThread):
    """Background thread that executes a sweep measurement.

    Signals:
        progress(current: int, total: int, eta_str: str) — emitted at each sweep step
        result_ready(result: object) — emitted when measurement completes (carries DataFrame)
        error(message: str) — emitted on error (carries error description)
        aborted() — emitted when measurement is gracefully aborted
        reset_failed(message: str) — emitted when post-run SMU reset fails
    """

    progress = Signal(int, int, str)
    result_ready = Signal(object)  # pd.DataFrame — measurement completed successfully
    error = Signal(str)
    aborted = Signal()
    aborted_with_data = Signal(object)  # pd.DataFrame (partial data from abort)
    reset_failed = Signal(str)

    def __init__(self, config: MeasurementConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self._abort_flag = threading.Event()

    def abort(self):
        """Request graceful abort of the running measurement."""
        self._abort_flag.set()
        logger.info("Abort requested")

    def _instrument_session_opened(self, advance_test: AdvanceTest | None) -> bool:
        """Return True only after the B1500 command layer has an open device session."""
        if advance_test is None:
            return False
        basic_test = getattr(advance_test, "basic_test", None)
        command = getattr(basic_test, "command", None)
        communication = getattr(command, "communication", None)
        return getattr(communication, "device", None) is not None

    def _reset_smus(self, advance_test: AdvanceTest | None, reason: str) -> str | None:
        """Disable all SMU channels after a worker run path touches an instrument session.

        Returns:
            A user-visible critical warning if reset failed, otherwise None.
        """
        if not self._instrument_session_opened(advance_test):
            logger.debug("Skipping SMU reset after %s because no instrument session is open", reason)
            return None
        try:
            advance_test.basic_test.command.reset_channel()
            logger.info("SMU channels reset after %s", reason)
            return None
        except Exception as reset_err:
            message = (
                f"Failed to reset SMU channels after {reason}: {reset_err}. "
                "The B1500 may still be biasing the DUT. Check the instrument output state immediately."
            )
            logger.exception(message)
            return message

    def _emit_reset_failure_if_needed(self, reset_error: str | None) -> None:
        """Surface cleanup failures to the GUI after data/error handlers run."""
        if reset_error:
            self.reset_failed.emit(reset_error)

    def run(self):
        """Execute the measurement in a background thread."""
        advance_test = None
        try:
            advance_test = AdvanceTest()

            def on_progress(current: int, total: int, elapsed: float):
                """Callback wired to the progress signal."""
                if total > 0 and current > 0:
                    avg_time = elapsed / current
                    remaining = avg_time * (total - current)
                    mins, secs = divmod(int(remaining), 60)
                    eta_str = f"{mins}m {secs}s" if mins else f"{secs}s"
                else:
                    eta_str = "—"
                self.progress.emit(current, total, eta_str)

            kwargs = self.config.to_advance_sweep_kwargs()
            kwargs['progress_callback'] = on_progress
            kwargs['abort_flag'] = self._abort_flag

            num_sweeps = len(self.config.sweep_channels)
            if num_sweeps >= 3:
                result = advance_test.three_way_sweep(**kwargs)
            elif num_sweeps >= 2:
                result = advance_test.two_way_sweep(**kwargs)
            else:
                self.error.emit("At least 2 sweep channels are required for a measurement")
                return

            reset_error = self._reset_smus(advance_test, "successful measurement")
            self.result_ready.emit(result)
            self._emit_reset_failure_if_needed(reset_error)

        except MeasurementAbortedError as e:
            logger.info("Measurement aborted: %s", e)
            # Reset SMUs to clear any biased voltages left by the sweep
            reset_error = self._reset_smus(advance_test, "abort")
            if e.partial_data is not None and len(e.partial_data) > 0:
                self.aborted_with_data.emit(e.partial_data)
            else:
                self.aborted.emit()
            self._emit_reset_failure_if_needed(reset_error)

        except PyVARError as e:
            logger.error("Measurement error: %s", e)
            # Reset SMUs to clear biased voltages, same as abort path
            reset_error = self._reset_smus(advance_test, "measurement error")
            self.error.emit(str(e))
            self._emit_reset_failure_if_needed(reset_error)

        except Exception as e:
            logger.exception("Unexpected error during measurement: %s", e)
            # Reset SMUs to clear biased voltages, same as abort path
            reset_error = self._reset_smus(advance_test, "unexpected error")
            self.error.emit(f"Unexpected error: {e}")
            self._emit_reset_failure_if_needed(reset_error)
