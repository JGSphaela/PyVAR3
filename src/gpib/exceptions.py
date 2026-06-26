"""Custom exception hierarchy for PyVAR3."""


class PyVARError(Exception):
    """Base exception for PyVAR3."""


class GPIBError(PyVARError):
    """GPIB communication error."""


class DeviceNotConnectedError(GPIBError):
    """Attempted to communicate with a device that is not connected."""


class InstrumentError(GPIBError):
    """The instrument returned an error response."""


class VoltageLimitError(PyVARError):
    """Attempted to set a voltage beyond the safety limit."""


class MeasurementAbortedError(PyVARError):
    """Measurement was aborted by the user.

    Attributes:
        partial_data: DataFrame with data collected before the abort, or None.
    """

    def __init__(self, message: str, partial_data=None):
        super().__init__(message)
        self.partial_data = partial_data
