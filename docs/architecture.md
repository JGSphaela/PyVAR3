# Architecture

## Overview

PyVAR3 is a layered application for controlling semiconductor test instruments via GPIB/PyVISA. The architecture separates hardware communication, instrument command building, measurement orchestration, data processing, and user interface into distinct layers.

## Layer Diagram

```
┌─────────────────────────────────────────────────┐
│                   GUI Layer                      │
│  main_window_pyside.py  sweep_widget.py          │
│  sweep_window.py        plotly_viewer.py         │
├─────────────────────────────────────────────────┤
│              Measurement Layer                   │
│  basic_sweep.py    advance_sweep.py              │
│  preparation.py                                 │
├─────────────────────────────────────────────────┤
│            Data Processing Layer                 │
│  read_data_process.py    plot2d.py               │
│  plot3d.py    plot3d2.py    plot3d3.py           │
├─────────────────────────────────────────────────┤
│           GPIB Command Layer                     │
│  gpib_command_b1500.py    gpib_command_model335.py│
│  exceptions.py                                   │
├─────────────────────────────────────────────────┤
│         Communication Layer                      │
│  gpib_communication.py (PyVISA wrapper)          │
├─────────────────────────────────────────────────┤
│              Physical Instruments                │
│  B1500A/B1505A/B1506A/B1507A   Model 335        │
└─────────────────────────────────────────────────┘
```

## Data Flow

```
User/GUI
  │
  ▼
AdvanceTest.three_way_sweep()
  │  ┌─ for each sweep3 voltage
  │  │   ┌─ for each sweep2 voltage
  │  │   │
  │  │   ▼
  │  │   BasicTest.multichannel_sweep_voltage()
  │  │     │
  │  │     ├─ B1500GPIBCommand: configure channels, ADC, sweep
  │  │     ├─ B1500GPIBCommand: force constant voltages
  │  │     ├─ B1500GPIBCommand.trigger_measurement() → raw SCPI string
  │  │     │
  │  │     ▼
  │  │   DataProcess.data_into_dataframe()
  │  │     │  Parse "WWA+1.00E-06,WWD+1.00E+00,..." → DataFrame
  │  │     ▼
  │  │   DataFrame (one sweep step)
  │  │
  │  └─ pd.concat(all sweep2 results) → backup CSV
  │
  └─ pd.concat(all sweep3 results) → final DataFrame
       │
       ▼
     CSV file / Plotly visualization
```

## Key Design Decisions

### Direct SCPI commands
Rather than using a higher-level instrument abstraction library, PyVAR3 sends raw SCPI commands directly through PyVISA. This gives full control over the B1500's command set and avoids abstraction overhead, at the cost of coupling tightly to the B1500's command syntax.

### Measurement-first design
The measurement layer (`basic_sweep.py`, `advance_sweep.py`) was built before the GUI. This means the measurement logic is fully functional as standalone scripts — the GUI is a convenience layer on top, not a requirement.

### Pandas DataFrames as the data model
All measurement data flows through pandas DataFrames. The `DataProcess` parser converts raw B1500 SCPI responses directly into DataFrames, and the sweep methods concatenate them with `pd.concat`. This makes data manipulation, filtering, and export straightforward.

### Safety via voltage limits
The B1500 command layer enforces a 2V safety limit on `force_voltage` and `set_voltage_sweep`. This protects the device under test from accidental overvoltage. The limit is currently hardcoded but should be made configurable per device type.

## Exception Hierarchy

```
PyVARError (base)
├── GPIBError
│   ├── DeviceNotConnectedError
│   └── InstrumentError
└── VoltageLimitError
```

All hardware communication errors bubble up through this hierarchy. The GUI catches `PyVARError` to display error messages, while measurement scripts catch specific subclasses as needed.

## Threading Model

The application is currently single-threaded. Long-running sweeps block the main thread, which means the GUI freezes during measurements. This is a known limitation that should be addressed by running measurements in a `QThread` or using signals/slots for progress updates.
