"""Measurement configuration dataclasses.

Provides structured configuration for sweep measurements that bridges
the GUI widgets, measurement execution, and file I/O.
"""

import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Any

logger = logging.getLogger(__name__)


@dataclass
class SweepChannelConfig:
    """Configuration for a single sweep channel.

    Maps directly to the parameters accepted by B1500GPIBCommand.set_voltage_sweep()
    and B1500GPIBCommand.force_voltage().
    """
    channel: int
    mode: int = 1
    range: int = 0
    start: float = 0.0
    stop: float = 0.0
    step: int = 0
    current_compliance: Optional[float] = None
    power_compliance: Optional[float] = None
    comp_polarity: int = 0
    current_range: Optional[int] = None

    def validate(self) -> list[str]:
        """Validate sweep channel parameters.

        :return: List of error messages. Empty if valid.
        """
        errors = []
        if self.channel < 1:
            errors.append(f"Channel must be >= 1, got {self.channel}")
        if self.step is None or self.step <= 0:
            errors.append(f"Step count must be > 0, got {self.step}")
        if self.step and self.step > 0 and self.start == self.stop and self.step > 1:
            errors.append(f"Start and stop are equal ({self.start}) but step > 1 ({self.step})")
        return errors


@dataclass
class MeasurementConfig:
    """Full measurement configuration.

    Contains all parameters needed to execute a sweep measurement,
    plus metadata for data provenance (device name, temperature, notes).
    """
    gpib_device_id: int = 17
    sweep_channels: list = field(default_factory=list)  # list[SweepChannelConfig]
    output_file: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    def validate(self) -> list[str]:
        """Validate the full measurement configuration.

        :return: List of error messages. Empty if valid.
        """
        errors = []
        if not self.sweep_channels:
            errors.append("At least one sweep channel is required")
        if len(self.sweep_channels) < 2:
            errors.append("At least 2 sweep channels are required for a measurement")
        if len(self.sweep_channels) > 3:
            errors.append(f"Maximum 3 sweep channels supported, got {len(self.sweep_channels)}")
        channels_seen = set()
        for i, ch in enumerate(self.sweep_channels):
            for err in ch.validate():
                errors.append(f"Sweep channel {i + 1}: {err}")
            if ch.channel in channels_seen:
                errors.append(f"Duplicate sweep channel {ch.channel} — each sweep must use a unique SMU channel")
            channels_seen.add(ch.channel)
        return errors

    def to_dict(self) -> dict:
        """Serialize to a JSON-compatible dictionary."""
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'MeasurementConfig':
        """Deserialize from a dictionary.

        :param d: Dictionary as produced by to_dict().
        :return: A MeasurementConfig instance.
        """
        sweep_channels = [
            SweepChannelConfig(**ch) for ch in d.get('sweep_channels', [])
        ]
        return cls(
            gpib_device_id=d.get('gpib_device_id', 17),
            sweep_channels=sweep_channels,
            output_file=d.get('output_file'),
            metadata=d.get('metadata', {}),
        )

    def to_advance_sweep_kwargs(self) -> dict[str, Any]:
        """Map this config to the keyword arguments expected by AdvanceTest methods.

        The first sweep_channel maps to sweep1_*, second to sweep2_*, third to sweep3_*.
        Any remaining channels beyond 3 are ignored (only 3-way sweep supported).

        :return: Dict of keyword arguments for three_way_sweep() or two_way_sweep().
        """
        if not self.sweep_channels:
            raise ValueError("No sweep channels configured")

        kwargs = {'gpib_device_id': self.gpib_device_id}

        def _map_channel(prefix: str, ch: SweepChannelConfig) -> dict:
            return {
                f'{prefix}_channel': ch.channel,
                f'{prefix}_mode': ch.mode,
                f'{prefix}_range': ch.range,
                f'{prefix}_start': ch.start,
                f'{prefix}_stop': ch.stop,
                f'{prefix}_step': ch.step,
                f'{prefix}_current_compliance': ch.current_compliance,
            }

        # First channel is always sweep1
        kwargs.update(_map_channel('sweep1', self.sweep_channels[0]))

        if len(self.sweep_channels) >= 2:
            ch = self.sweep_channels[1]
            kwargs.update({
                'sweep2_channel': ch.channel,
                'sweep2_range': ch.range,
                'sweep2_start': ch.start,
                'sweep2_stop': ch.stop,
                'sweep2_step': ch.step,
                'sweep2_current_compliance': ch.current_compliance,
            })

        if len(self.sweep_channels) >= 3:
            ch = self.sweep_channels[2]
            kwargs.update({
                'sweep3_channel': ch.channel,
                'sweep3_range': ch.range,
                'sweep3_start': ch.start,
                'sweep3_stop': ch.stop,
                'sweep3_step': ch.step,
                'sweep3_current_compliance': ch.current_compliance,
            })

        if self.sweep_channels[0].power_compliance is not None:
            kwargs['sweep1_power_compliance'] = self.sweep_channels[0].power_compliance

        return kwargs
