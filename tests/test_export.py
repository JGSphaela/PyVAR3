"""Tests for CSV export with metadata."""

import os
import pandas as pd

from src.data_process.export import export_with_metadata, read_csv_with_metadata
from src.measurement.config import MeasurementConfig, SweepChannelConfig


class TestExportWithMetadata:
    def test_export_creates_file(self, tmp_path):
        df = pd.DataFrame({'A_I': [1e-6, 2e-6], 'A_V': [0.0, 0.5]})
        config = MeasurementConfig(
            gpib_device_id=17,
            sweep_channels=[SweepChannelConfig(channel=1, start=0.0, stop=1.0, step=101)],
            metadata={"device": "TSMC_22nm", "temperature": "300K"},
        )
        filepath = str(tmp_path / "test.csv")
        export_with_metadata(df, config, filepath)

        assert os.path.exists(filepath)

        # Read raw file and check comment headers
        with open(filepath) as f:
            lines = f.readlines()
        assert any("PyVAR3" in line for line in lines)
        assert any("TSMC_22nm" in line for line in lines)
        assert any("300K" in line for line in lines)

    def test_round_trip(self, tmp_path):
        df = pd.DataFrame({
            'A_I': [1e-6, 2e-6, 3e-6],
            'A_V': [0.0, 0.5, 1.0],
            'B_I': [1e-7, 2e-7, 3e-7],
        })
        config = MeasurementConfig(
            gpib_device_id=17,
            sweep_channels=[
                SweepChannelConfig(channel=1, start=0.0, stop=1.0, step=101, current_compliance=0.1),
            ],
            metadata={"device": "FinFET_7nm", "operator": "test"},
        )
        filepath = str(tmp_path / "roundtrip.csv")
        export_with_metadata(df, config, filepath)

        # Read back
        loaded_df, metadata = read_csv_with_metadata(filepath)

        assert len(loaded_df) == 3
        assert list(loaded_df.columns) == ['A_I', 'A_V', 'B_I']
        assert metadata.get('device') == 'FinFET_7nm'
        assert metadata.get('operator') == 'test'

    def test_creates_parent_directory(self, tmp_path):
        df = pd.DataFrame({'x': [1, 2]})
        config = MeasurementConfig()
        filepath = str(tmp_path / "subdir" / "test.csv")
        export_with_metadata(df, config, filepath)
        assert os.path.exists(filepath)
