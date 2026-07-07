<img src="/src/logo.png" width="300" />

# PyVAR3

Multi-parameter sweep measurement tool for semiconductor device characterization.

Keysight's B1500 software only supports 2 sweep variables (VAR1, VAR2). PyVAR3 extends this to 3+ sweep parameters, enabling complex characterization of MOSFETs, FinFETs, and other devices — including cryogenic measurements down to 6.5K.

## Features

- **3+ parameter sweeps** — overcome the VAR1/VAR2 limitation with nested voltage sweeps
- **B1500A/B1505A/B1506A/B1507A support** — full SCPI command set for SMU control
- **Lakeshore Model 335** — integrated temperature reading for temperature-dependent measurements
- **Live progress tracking** — ETA estimation during long multi-hour sweeps
- **Data processing** — automatic parsing of B1500 responses into pandas DataFrames
- **3D visualization** — interactive Plotly plots for multi-parameter data

## Installation

### Prerequisites

- Python 3.10+
- A VISA backend:
  - **Windows**: [Keysight IO Libraries Suite](https://www.keysight.com/find/iosuite)
  - **macOS/Linux**: [NI-VISA](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html) or `pyvisa-py`

### Install

```bash
git clone https://github.com/JGSphaela/PyVAR3.git
cd PyVAR3
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Quick Start

### From a script

```python
from src.measurement.advance_sweep import AdvanceTest

test = AdvanceTest()
result = test.three_way_sweep(
    gpib_device_id=17,
    sweep1_channel=1, sweep1_mode=1, sweep1_range=0,
    sweep1_start=0.0, sweep1_stop=1.0, sweep1_step=101,
    sweep2_channel=2, sweep2_range=0,
    sweep2_start=0.0, sweep2_stop=0.5, sweep2_step=6,
    sweep3_channel=3, sweep3_range=0,
    sweep3_start=0.0, sweep3_stop=0.3, sweep3_step=4,
)
result.to_csv("measurement_result.csv", index=False)
```

### Run the GUI

```bash
python src/main.py
```

## Project Structure

```
src/
├── main.py                      # Application entry point (PySide6 GUI)
├── gpib/
│   ├── gpib_communication.py    # PyVISA wrapper for GPIB devices
│   ├── gpib_command_b1500.py    # B1500 SCPI command set
│   ├── gpib_command_model335.py # Lakeshore Model 335 commands
│   └── exceptions.py            # Custom exception hierarchy
├── measurement/
│   ├── basic_sweep.py           # Single-channel sweep execution
│   ├── advance_sweep.py         # Multi-way (2/3) sweep orchestration
│   └── preparation.py           # Pre-test setup (format, filters, averaging)
├── data_process/
│   ├── read_data_process.py     # B1500 response parser → DataFrame
│   ├── plot2d.py                # Matplotlib 2D plotting
│   ├── plot3d.py                # Plotly interactive 3D plotting
│   └── plot3d2.py, plot3d3.py   # Additional 3D visualization variants
├── gui/
│   ├── main_window_pyside.py    # Main PySide6 application window
│   ├── sweep_widget.py          # Sweep parameter input widget
│   ├── sweep_window.py          # Sweep configuration container
│   └── translations/            # i18n (English, Japanese)
└── utils/
    └── helper.py                # Translation loading utility

examples/                        # Usage examples and manual test scripts
tests/                           # Automated pytest test suite
docs/                            # Architecture and design documentation
```

## Development

### Running tests

```bash
pytest tests/ -v
```

### Running tests with coverage

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## Hardware Requirements

| Device | Purpose | Connection |
|--------|---------|------------|
| Keysight B1500A/B1505A/B1506A/B1507A | Semiconductor Device Analyzer | GPIB |
| Lakeshore Model 335 | Temperature Controller | GPIB |
| GPIB adapter | Host-to-instrument communication | USB/GPIB |

## Platform Notes

| Platform | VISA Backend | Status |
|----------|-------------|--------|
| Windows | Keysight IO Libraries Suite | Primary, fully supported |
| macOS | NI-VISA | Works, tested |
| Linux | NI-VISA or pyvisa-py | Should work, limited testing |

## Roadmap

### Short-term
- Wire GUI Start button to measurement code
- Temperature sweep integration (voltage sweep at multiple temperatures)
- Measurement profiles (save/load sweep configurations as JSON)

### Medium-term
- Live plotting during measurement
- Safety interlocks (configurable voltage limits, emergency stop)
- CSV export with metadata headers (device, temperature, timestamp)

### Long-term
- Plugin architecture for additional instruments
- Remote monitoring / network control
- Automated measurement sequences (e.g., Id-Vg at multiple temperatures overnight)

## License

[GNU General Public License v3.0](LICENSE)
