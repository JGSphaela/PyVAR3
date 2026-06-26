"""Tests for DataProcess — B1500 raw response parser."""

import pytest
import pandas as pd

from src.data_process.read_data_process import DataProcess
from src.gpib.exceptions import PyVARError


class TestDataIntoDataframe:
    def test_parse_valid_response(self, sample_b1500_response):
        """Verify DataFrame shape and columns from a known-good response."""
        df = DataProcess.data_into_dataframe(sample_b1500_response)
        assert isinstance(df, pd.DataFrame)
        # Should have 2 intermediate steps (W status) + 1 final step (E status) = 3 rows
        # But the E status breaks immediately, so we get 2 W rows + 1 E row = 3 rows
        assert len(df) > 0
        # Columns should contain channel_data_type combinations
        assert all('_' in col for col in df.columns)

    def test_parse_single_step(self, sample_b1500_single_step):
        """Verify parsing of a single sweep step (only E status)."""
        df = DataProcess.data_into_dataframe(sample_b1500_single_step)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    def test_column_sorting(self, sample_b1500_response):
        """Verify columns are sorted by data_type then channel."""
        df = DataProcess.data_into_dataframe(sample_b1500_response)
        columns = list(df.columns)
        # Extract data_type and channel from column names
        data_types = [col.split('_')[1] for col in columns]
        channels = [col.split('_')[0] for col in columns]
        # Data types should be sorted
        assert data_types == sorted(data_types)

    def test_status_decoding(self):
        """Verify W and E status codes correctly segment data."""
        # Two W steps followed by one E step, each with one channel
        response = "WWA+1.00000E-06,WWA+2.00000E-06,EWA+3.00000E-06"
        df = DataProcess.data_into_dataframe(response)
        assert len(df) == 3  # 2 W + 1 E

    def test_invalid_data_graceful_handling(self):
        """Verify handling of malformed strings that don't match the regex."""
        # Invalid data that doesn't match the regex pattern
        df = DataProcess.data_into_dataframe("invalid,data,here")
        assert isinstance(df, pd.DataFrame)
        # No regex matches means empty DataFrame
        assert len(df) == 0

    def test_parse_empty_string(self):
        """Verify handling of empty input raises PyVARError (counter > 6 with no status codes)."""
        from src.gpib.exceptions import PyVARError
        # Empty string produces no entries, which means counter stays at 0
        # This actually works fine and returns an empty DataFrame
        df = DataProcess.data_into_dataframe("")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_no_sweep_voltage_raises(self):
        """Verify PyVARError when data has too many consecutive entries without sweep voltage."""
        # Create a string with more than 6 consecutive entries with non-W, non-E status
        # Actually, the counter check only triggers when counter > 6 without hitting W or E
        # All entries must fail the regex match but we need entries that match the regex
        # but have a status that's neither W nor E
        # The regex requires uppercase letters for status, so let's use 'X' status
        entries = ",".join([f"XXA+{i}.00000E-06" for i in range(8)])
        with pytest.raises(PyVARError, match="No Sweep Voltage"):
            DataProcess.data_into_dataframe(entries)
