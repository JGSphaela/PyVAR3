"""Tests for measurement profile save/load."""

import json
import os
import pytest

from src.measurement.config import MeasurementConfig, SweepChannelConfig
from src.measurement.profiles import save_profile, load_profile, list_profiles


class TestSaveLoadProfile:
    def test_round_trip(self, tmp_path):
        config = MeasurementConfig(
            gpib_device_id=17,
            sweep_channels=[
                SweepChannelConfig(channel=1, start=0.0, stop=-1.2, step=121, current_compliance=0.1),
                SweepChannelConfig(channel=2, start=0.0, stop=-1.2, step=121),
            ],
            metadata={"device": "TSMC_22nm"},
        )
        filepath = str(tmp_path / "test_profile.json")
        save_profile(config, filepath)

        # Verify file exists and is valid JSON
        assert os.path.exists(filepath)
        with open(filepath) as f:
            data = json.load(f)
        assert data['gpib_device_id'] == 17
        assert len(data['sweep_channels']) == 2

        # Load and verify round-trip
        loaded = load_profile(filepath)
        assert loaded.gpib_device_id == 17
        assert len(loaded.sweep_channels) == 2
        assert loaded.sweep_channels[0].current_compliance == 0.1
        assert loaded.metadata["device"] == "TSMC_22nm"

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_profile("/nonexistent/profile.json")

    def test_load_invalid_json(self, tmp_path):
        filepath = tmp_path / "bad.json"
        filepath.write_text("not json")
        with pytest.raises(json.JSONDecodeError):
            load_profile(str(filepath))


class TestListProfiles:
    def test_list_profiles(self, tmp_path):
        # Create some profile files
        config = MeasurementConfig(sweep_channels=[SweepChannelConfig(channel=1)])
        save_profile(config, str(tmp_path / "profile1.json"))
        save_profile(config, str(tmp_path / "profile2.json"))

        # Create a non-JSON file (should not be listed)
        (tmp_path / "notes.txt").write_text("not a profile")

        profiles = list_profiles(str(tmp_path))
        assert len(profiles) == 2
        assert all(p.endswith('.json') for p in profiles)

    def test_list_empty_directory(self, tmp_path):
        profiles = list_profiles(str(tmp_path))
        assert profiles == []

    def test_list_nonexistent_directory(self):
        profiles = list_profiles("/nonexistent/dir")
        assert profiles == []
