"""CSV export with metadata headers.

Provides export_with_metadata() to write DataFrames with comment-header
metadata (device name, temperature, sweep config) and read_csv_with_metadata()
to parse them back.
"""

import logging
from pathlib import Path

import pandas as pd

from src.measurement.config import MeasurementConfig

logger = logging.getLogger(__name__)


def export_with_metadata(df: pd.DataFrame, config: MeasurementConfig, filepath: str) -> None:
    """Export a measurement DataFrame to CSV with metadata comment headers.

    The CSV file will contain lines starting with '#' at the top with metadata
    (device info, temperature, sweep parameters), followed by the standard CSV data.

    :param df: Measurement data to export.
    :param config: Measurement configuration used for the measurement.
    :param filepath: Output file path.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', newline='') as f:
        # Write metadata header
        f.write("# PyVAR3 Measurement Data\n")
        f.write(f"# gpib_device_id: {config.gpib_device_id}\n")

        for key, value in config.metadata.items():
            f.write(f"# {key}: {value}\n")

        # Write sweep configuration summary
        for i, ch in enumerate(config.sweep_channels):
            f.write(f"# sweep{i + 1}: channel={ch.channel} mode={ch.mode} "
                    f"range={ch.range} start={ch.start} stop={ch.stop} step={ch.step} "
                    f"compliance={ch.current_compliance}\n")

        # Write column header and data
        df.to_csv(f, index=False)

    logger.info(f"Exported {len(df)} rows to {filepath} with metadata")


def read_csv_with_metadata(filepath: str) -> tuple:
    """Read a CSV file with metadata comment headers.

    :param filepath: Path to the CSV file.
    :return: Tuple of (DataFrame, metadata_dict).
    """
    metadata = {}
    header_lines = 0

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                header_lines += 1
                # Parse "# key: value" format
                content = line[1:].strip()
                if ':' in content and not content.startswith('PyVAR3'):
                    key, _, value = content.partition(':')
                    metadata[key.strip()] = value.strip()
            else:
                break  # First non-comment line is the CSV header

    df = pd.read_csv(filepath, skiprows=header_lines)
    logger.info(f"Read {len(df)} rows from {filepath} with {len(metadata)} metadata keys")
    return df, metadata
