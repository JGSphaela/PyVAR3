"""Tests for measurement configuration dataclasses."""

import pytest
from src.measurement.config import SweepChannelConfig, MeasurementConfig


class TestSweepChannelConfig:
    def test_default_values(self):
        ch = SweepChannelConfig(channel=1)
        assert ch.channel == 1
        assert ch.mode == 1
        assert ch.range == 0
        assert ch.start == 0.0
        assert ch.stop == 0.0
        assert ch.step == 0

    def test_validate_valid(self):
        ch = SweepChannelConfig(channel=1, start=0.0, stop=1.0, step=101)
        assert ch.validate() == []

    def test_validate_invalid_channel(self):
        ch = SweepChannelConfig(channel=0)
        errors = ch.validate()
        assert any("Channel must be >= 1" in e for e in errors)

    def test_validate_negative_step(self):
        ch = SweepChannelConfig(channel=1, step=-1)
        errors = ch.validate()
        assert any("Step count" in e for e in errors)


class TestMeasurementConfig:
    def test_empty_config_validation(self):
        config = MeasurementConfig()
        errors = config.validate()
        assert any("At least one sweep channel" in e for e in errors)

    def test_too_many_channels(self):
        config = MeasurementConfig(
            sweep_channels=[SweepChannelConfig(channel=i) for i in range(4)]
        )
        errors = config.validate()
        assert any("Maximum 3" in e for e in errors)

    def test_valid_config(self):
        config = MeasurementConfig(
            sweep_channels=[
                SweepChannelConfig(channel=1, start=0.0, stop=1.0, step=101),
                SweepChannelConfig(channel=2, start=0.0, stop=0.5, step=6),
            ]
        )
        assert config.validate() == []


class TestConfigSerialization:
    def test_round_trip(self):
        config = MeasurementConfig(
            gpib_device_id=17,
            sweep_channels=[
                SweepChannelConfig(channel=1, mode=1, start=0.0, stop=-1.2, step=121, current_compliance=0.1),
                SweepChannelConfig(channel=2, mode=1, start=0.0, stop=-1.2, step=121),
            ],
            output_file="test.csv",
            metadata={"device": "TSMC_22nm", "temperature": "300K"},
        )
        d = config.to_dict()
        restored = MeasurementConfig.from_dict(d)

        assert restored.gpib_device_id == 17
        assert len(restored.sweep_channels) == 2
        assert restored.sweep_channels[0].channel == 1
        assert restored.sweep_channels[0].stop == -1.2
        assert restored.sweep_channels[0].current_compliance == 0.1
        assert restored.metadata["device"] == "TSMC_22nm"
        assert restored.output_file == "test.csv"

    def test_to_advance_sweep_kwargs_two_way(self):
        config = MeasurementConfig(
            gpib_device_id=17,
            sweep_channels=[
                SweepChannelConfig(channel=1, start=0.0, stop=1.0, step=101, current_compliance=0.1),
                SweepChannelConfig(channel=2, start=0.0, stop=0.5, step=6),
            ],
        )
        kwargs = config.to_advance_sweep_kwargs()
        assert kwargs['gpib_device_id'] == 17
        assert kwargs['sweep1_channel'] == 1
        assert kwargs['sweep1_stop'] == 1.0
        assert kwargs['sweep2_channel'] == 2
        assert kwargs['sweep2_step'] == 6
        assert 'sweep3_channel' not in kwargs

    def test_to_advance_sweep_kwargs_three_way(self):
        config = MeasurementConfig(
            sweep_channels=[
                SweepChannelConfig(channel=2, start=0.0, stop=-1.2, step=121),
                SweepChannelConfig(channel=1, start=0.0, stop=-1.2, step=121),
                SweepChannelConfig(channel=4, start=-0.6, stop=0.6, step=121),
            ],
        )
        kwargs = config.to_advance_sweep_kwargs()
        assert kwargs['sweep1_channel'] == 2
        assert kwargs['sweep2_channel'] == 1
        assert kwargs['sweep3_channel'] == 4
        assert kwargs['sweep3_start'] == -0.6
