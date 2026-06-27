"""QThread worker for running measurements in the background.

Runs AdvanceTest sweep methods in a separate thread so the GUI remains
responsive during long measurements. Emits signals for progress, completion,
errors, and abort.
"""

import logging
import threading

import pandas as pd
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
    """

    progress = Signal(int, int, str)
    result_ready = Signal(object)  # pd.DataFrame — measurement completed successfully
    error = Signal(str)
    aborted = Signal()
    aborted_with_data = Signal(object)  # pd.DataFrame (partial data from abort)

    def __init__(self, config: MeasurementConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self._abort_flag = threading.Event()

    def abort(self):
        """Request graceful abort of the running measurement."""
        self._abort_flag.set()
        logger.info("Abort requested")

    def _reset_smus(self, advance_test: AdvanceTest | None, reason: str):
        """Disable all SMU channels after a worker run path touches the instrument."""
        if advance_test is None:
            logger.debug("Skipping SMU reset after %s because the instrument was not initialized", reason)
            return
        try:
            advance_test.basic_test.command.reset_channel()
            logger.info("SMU channels reset after %s", reason)
        except Exception as reset_err:
            logger.warning("Failed to reset SMU channels after %s: %s", reason, reset_err)

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

            self._reset_smus(advance_test, "successful measurement")
            self.result_ready.emit(result)

        except MeasurementAbortedError as e:
            logger.info(f"Measurement aborted: {e}")
            # Reset SMUs to clear any biased voltages left by the sweep
            self._reset_smus(advance_test, "abort")
            if e.partial_data is not None and len(e.partial_data) > 0:
                self.aborted_with_data.emit(e.partial_data)
            else:
                self.aborted.emit()

        except PyVARError as e:
            logger.error(f"Measurement error: {e}")
            # Reset SMUs to clear biased voltages, same as abort path
            self._reset_smus(advance_test, "measurement error")
            self.error.emit(str(e))

        except Exception as e:
            logger.exception(f"Unexpected error during measurement: {e}")
            # Reset SMUs to clear biased voltages, same as abort path
            self._reset_smus(advance_test, "unexpected error")
            self.error.emit(f"Unexpected error: {e}")
