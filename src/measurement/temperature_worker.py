"""QThread worker for polling the Lakeshore Model 335 temperature controller.

Runs in the background, continuously querying temperature at a configurable
interval. Emits signals so the GUI can display live temperature readings.
"""

import logging
import time

from PySide6.QtCore import QThread, Signal

from src.gpib.gpib_command_model335 import Model335GPIBCommand

logger = logging.getLogger(__name__)


class TemperatureWorker(QThread):
    """Background thread that polls the Model 335 for temperature readings.

    Signals:
        temperature_updated(channel: str, kelvin: float) — emitted on each reading
        error(message: str) — emitted on communication error
    """

    temperature_updated = Signal(str, float)
    error = Signal(str)

    def __init__(self, gpib_id: int = 12, channels: list = None,
                 interval: float = 1.0, parent=None):
        """
        :param gpib_id: GPIB address of the Model 335.
        :param channels: List of input channels to poll (default ['A', 'B']).
        :param interval: Polling interval in seconds (default 1.0).
        :param parent: Qt parent widget.
        """
        super().__init__(parent)
        self.gpib_id = gpib_id
        self.channels = channels or ['A', 'B']
        self.interval = interval
        self._running = True
        self._model335 = None

    def stop(self):
        """Request the worker to stop polling."""
        self._running = False

    def get_latest_temperatures(self) -> dict:
        """Get the most recently read temperatures.

        :return: Dict mapping channel to temperature in Kelvin.
        """
        temps = {}
        if self._model335:
            for ch in self.channels:
                try:
                    raw = self._model335.query_kelvin(input_channel=ch)
                    temps[ch] = float(raw.strip())
                except Exception:
                    pass
        return temps

    def run(self):
        """Poll temperature in a background thread."""
        try:
            self._model335 = Model335GPIBCommand()
            self._model335.init_connection(gpib_id=self.gpib_id)
        except Exception as e:
            self.error.emit(f"Failed to connect to Model 335: {e}")
            return

        while self._running:
            for ch in self.channels:
                try:
                    raw = self._model335.query_kelvin(input_channel=ch)
                    temp_k = float(raw.strip())
                    self.temperature_updated.emit(ch, temp_k)
                except Exception as e:
                    self.error.emit(f"Temperature read error (ch {ch}): {e}")

            time.sleep(self.interval)
