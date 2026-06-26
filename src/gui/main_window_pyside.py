import logging
import os

from PySide6.QtWidgets import QMainWindow, QStatusBar, QMessageBox, QFileDialog

from src.gui.sweep_window import SweepWindow
from src.gui.measurement_worker import MeasurementWorker
from src.measurement.profiles import save_profile, load_profile

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main PySide6 application window.

    Wires the SweepWindow configuration UI to the MeasurementWorker background
    thread. Handles profile save/load via the File menu.
    """

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.worker = None
        self.setWindowTitle("PyVAR3 — Semiconductor Parameter Measurement")
        self.menuBar().setNativeMenuBar(False)  # only needed on Mac

        # Menubar
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        save_profile_action = file_menu.addAction("Save Profile...")
        save_profile_action.triggered.connect(self.save_profile)
        load_profile_action = file_menu.addAction("Load Profile...")
        load_profile_action.triggered.connect(self.load_profile)
        file_menu.addSeparator()
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.app.quit)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")
        about_menu = help_menu.addAction("About")
        about_menu.triggered.connect(self.about_app)

        # Status Bar
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

        # Central widget
        self.sweep_window = SweepWindow()
        self.setCentralWidget(self.sweep_window)

        # Wire start/stop button
        self.sweep_window.start_stop_button.clicked.connect(self.on_start_stop)

    def on_start_stop(self):
        """Handle Start/Stop button click."""
        if self.worker and self.worker.isRunning():
            # Abort running measurement
            self.worker.abort()
            self.statusBar().showMessage("Aborting measurement...")
            return

        # Build config and validate
        config = self.sweep_window.get_config()
        errors = config.validate()
        if errors:
            QMessageBox.warning(self, "Configuration Error", "\n".join(errors))
            return

        # Start measurement in background thread
        self.worker = MeasurementWorker(config, parent=self)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.aborted.connect(self.on_aborted)
        self.worker.aborted_with_data.connect(self.on_aborted_with_data)

        self.sweep_window.set_running(True)
        self.statusBar().showMessage("Measurement running...")
        self.worker.start()

    def on_progress(self, current: int, total: int, eta_str: str):
        """Update progress display from worker."""
        self.sweep_window.update_progress(current, total, eta_str)
        self.statusBar().showMessage(f"Step {current}/{total} — ETA: {eta_str}")

    def on_finished(self, result):
        """Handle measurement completion."""
        self.sweep_window.set_running(False)
        self.statusBar().showMessage(f"Measurement complete — {len(result)} data points")
        logger.info(f"Measurement finished with {len(result)} rows")

        # Auto-save using the worker's config (not current UI state, which may have changed)
        config = self.worker.config
        if config.output_file:
            os.makedirs(os.path.dirname(config.output_file) or '.', exist_ok=True)
            result.to_csv(config.output_file, index=False)
            logger.info(f"Results saved to {config.output_file}")
        else:
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Save Measurement Results", "", "CSV Files (*.csv)")
            if filepath:
                os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
                result.to_csv(filepath, index=False)
                logger.info(f"Results saved to {filepath}")

    def on_error(self, message: str):
        """Handle measurement error."""
        self.sweep_window.set_running(False)
        self.statusBar().showMessage(f"Error: {message}")
        QMessageBox.critical(self, "Measurement Error", message)

    def on_aborted(self):
        """Handle measurement abort (no partial data)."""
        self.sweep_window.set_running(False)
        self.statusBar().showMessage("Measurement aborted")
        QMessageBox.information(self, "Aborted", "Measurement was aborted.")

    def on_aborted_with_data(self, result):
        """Handle measurement abort with partial data."""
        self.sweep_window.set_running(False)
        self.statusBar().showMessage(f"Measurement aborted — {len(result)} partial data points collected")

        # Persist partial results using the worker's config
        config = self.worker.config
        if config.output_file:
            os.makedirs(os.path.dirname(config.output_file) or '.', exist_ok=True)
            result.to_csv(config.output_file, index=False)
            logger.info(f"Partial results saved to {config.output_file}")
        else:
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Save Partial Results", "", "CSV Files (*.csv)")
            if filepath:
                os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
                result.to_csv(filepath, index=False)
                logger.info(f"Partial results saved to {filepath}")

        QMessageBox.warning(self, "Aborted with Partial Data",
                            f"Measurement was aborted after collecting {len(result)} data points.\n"
                            "The partial result is available but may be incomplete.")

    def save_profile(self):
        """Save current sweep configuration to a JSON file."""
        config = self.sweep_window.get_config()
        errors = config.validate()
        if errors:
            QMessageBox.warning(self, "Cannot Save", "\n".join(errors))
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Profile", "profiles/", "JSON Files (*.json)")
        if filepath:
            save_profile(config, filepath)
            self.statusBar().showMessage(f"Profile saved to {filepath}")

    def load_profile(self):
        """Load a sweep configuration from a JSON file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Load Profile", "profiles/", "JSON Files (*.json)")
        if filepath:
            try:
                config = load_profile(filepath)
                self.sweep_window.set_config(config)
                self.statusBar().showMessage(f"Profile loaded from {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load profile:\n{e}")

    def about_app(self):
        QMessageBox.about(self, "About PyVAR3",
                          "PyVAR3 — Multi-parameter sweep measurement tool\n"
                          "for semiconductor device characterization.\n\n"
                          "License: GPL v3")