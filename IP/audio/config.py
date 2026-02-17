"""Audio configuration module for Orchestr8 Code City visualization.

Provides deterministic frequency band definitions and calibration settings
for audio-reactive visualization effects.
"""

from dataclasses import dataclass
from typing import Tuple, List, Optional


# Deterministic frequency bands (Hz)
LOW_BAND = (10, 250)  # Bass/sub-bass
MID_BAND = (250, 2000)  # Mids/vocals
HIGH_BAND = (2000, 20000)  # Treble/air

# Calibration constants
DEFAULT_FFT_SIZE = 256
DEFAULT_SMOOTHING = 0.82
SENSITIVITY_RANGE = (1, 100)


@dataclass(frozen=True)
class FrequencyBand:
    """Immutable frequency band definition.

    Attributes:
        name: Band identifier ("low", "mid", "high")
        range_hz: Tuple of (min_hz, max_hz) frequency boundaries
    """

    name: str
    range_hz: Tuple[int, int]

    @property
    def low_hz(self) -> int:
        """Lower frequency boundary in Hz."""
        return self.range_hz[0]

    @property
    def high_hz(self) -> int:
        """Upper frequency boundary in Hz."""
        return self.range_hz[1]

    @property
    def center_hz(self) -> int:
        """Geometric center frequency of the band."""
        return int((self.low_hz * self.high_hz) ** 0.5)

    @property
    def bandwidth(self) -> int:
        """Width of the frequency band in Hz."""
        return self.high_hz - self.low_hz


@dataclass
class AudioCalibration:
    """Audio processing calibration settings.

    Attributes:
        fft_size: FFT window size (power of 2, default 256)
        smoothing: Exponential smoothing factor (0-1, default 0.82)
        sensitivity: Overall sensitivity multiplier (1-100, default 50)
    """

    fft_size: int = DEFAULT_FFT_SIZE
    smoothing: float = DEFAULT_SMOOTHING
    sensitivity: int = 50

    def __post_init__(self):
        """Validate calibration parameters after initialization."""
        if self.fft_size < 64 or self.fft_size > 4096:
            raise ValueError(
                f"fft_size must be between 64 and 4096, got {self.fft_size}"
            )
        if self.fft_size & (self.fft_size - 1) != 0:
            raise ValueError(f"fft_size must be a power of 2, got {self.fft_size}")
        if not 0.0 <= self.smoothing <= 1.0:
            raise ValueError(
                f"smoothing must be between 0.0 and 1.0, got {self.smoothing}"
            )
        if not SENSITIVITY_RANGE[0] <= self.sensitivity <= SENSITIVITY_RANGE[1]:
            raise ValueError(
                f"sensitivity must be between {SENSITIVITY_RANGE[0]} and {SENSITIVITY_RANGE[1]}, got {self.sensitivity}"
            )

    @property
    def sensitivity_multiplier(self) -> float:
        """Return sensitivity as a normalized float (0.01 to 1.0)."""
        return self.sensitivity / 100.0

    def with_fft_size(self, size: int) -> "AudioCalibration":
        """Return a new calibration with updated FFT size."""
        return AudioCalibration(
            fft_size=size, smoothing=self.smoothing, sensitivity=self.sensitivity
        )

    def with_smoothing(self, value: float) -> "AudioCalibration":
        """Return a new calibration with updated smoothing factor."""
        return AudioCalibration(
            fft_size=self.fft_size, smoothing=value, sensitivity=self.sensitivity
        )

    def with_sensitivity(self, value: int) -> "AudioCalibration":
        """Return a new calibration with updated sensitivity."""
        return AudioCalibration(
            fft_size=self.fft_size, smoothing=self.smoothing, sensitivity=value
        )


# Predefined frequency band instances
_LOW_BAND = FrequencyBand(name="low", range_hz=LOW_BAND)
_MID_BAND = FrequencyBand(name="mid", range_hz=MID_BAND)
_HIGH_BAND = FrequencyBand(name="high", range_hz=HIGH_BAND)


def get_band_by_name(name: str) -> Optional[FrequencyBand]:
    """Retrieve a frequency band by its name.

    Args:
        name: Band identifier ("low", "mid", "high")

    Returns:
        FrequencyBand instance if found, None otherwise
    """
    name_lower = name.lower().strip()
    if name_lower == "low":
        return _LOW_BAND
    elif name_lower == "mid":
        return _MID_BAND
    elif name_lower == "high":
        return _HIGH_BAND
    return None


def get_all_bands() -> List[FrequencyBand]:
    """Return all defined frequency bands in order (low, mid, high).

    Returns:
        List of FrequencyBand instances
    """
    return [_LOW_BAND, _MID_BAND, _HIGH_BAND]
