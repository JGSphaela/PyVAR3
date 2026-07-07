"""Measurement profile save/load functionality.

Profiles are JSON files that store a MeasurementConfig, allowing users to
save and recall sweep configurations for repeated experiments.
"""

import json
import logging
from pathlib import Path

from src.measurement.config import MeasurementConfig

logger = logging.getLogger(__name__)


def save_profile(config: MeasurementConfig, filepath: str) -> None:
    """Save a measurement configuration to a JSON file.

    :param config: Measurement configuration to save.
    :param filepath: Output file path (should end in .json).
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = config.to_dict()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved profile to {filepath}")


def load_profile(filepath: str) -> MeasurementConfig:
    """Load a measurement configuration from a JSON file.

    :param filepath: Path to the JSON profile file.
    :return: MeasurementConfig instance.
    :raises FileNotFoundError: If the file does not exist.
    :raises json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    config = MeasurementConfig.from_dict(data)
    logger.info(f"Loaded profile from {filepath}: {len(config.sweep_channels)} sweep channels")
    return config


def list_profiles(directory: str) -> list:
    """List all JSON profile files in a directory.

    :param directory: Directory to search for .json files.
    :return: List of file paths (as strings).
    """
    path = Path(directory)
    if not path.is_dir():
        return []

    profiles = sorted(str(p) for p in path.glob("*.json"))
    logger.info(f"Found {len(profiles)} profiles in {directory}")
    return profiles
