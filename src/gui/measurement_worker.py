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
        finished(result: object) — emitted when measurement completes (carries DataFrame)
        error(message: str) — emitted on error (carries error description)
        aborted() — emitted when measurement is gracefully aborted
    """

    progress = Signal(int, int, str)
    finished = Signal(object)  # pd.DataFrame
    error = Signal(str)
    aborted = Signal()

    def __init__(self, config: MeasurementConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self._abort_flag = threading.Event()

    def abort(self):
        """Request graceful abort of the running measurement."""
        self._abort_flag.set()
        logger.info("Abort requested")

    def run(self):
        """Execute the measurement in a background thread."""
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

            self.finished.emit(result)

        except MeasurementAbortedError as e:
            logger.info(f"Measurement aborted: {e}")
            if e.partial_data is not None and len(e.partial_data) > 0:
                self.finished.emit(e.partial_data)
            else:
                self.aborted.emit()

        except PyVARError as e:
            logger.error(f"Measurement error: {e}")
            self.error.emit(str(e))

        except Exception as e:
            logger.exception(f"Unexpected error during measurement: {e}")
            self.error.emit(f"Unexpected error: {e}")
