"""Audio frequency analyzer module for Orchestr8 Code City visualization.

Processes raw FFT data from Web Audio API into normalized band energies
for audio-reactive visualization effects.
"""

from dataclasses import dataclass
from typing import List, Dict

from IP.audio.config import FrequencyBand, AudioCalibration, get_all_bands


@dataclass
class BandEnergy:
    """Normalized energy for a frequency band (0.0 - 1.0).

    Attributes:
        band_name: Band identifier ("low", "mid", "high")
        raw_value: Unnormalized energy value (0-255 from Web Audio API)
        normalized: Normalized value clamped to 0.0-1.0 range
    """

    band_name: str
    raw_value: float
    normalized: float


@dataclass
class AnalysisResult:
    """Complete frequency analysis result for all bands.

    Attributes:
        low: Energy for low frequency band (bass/sub-bass)
        mid: Energy for mid frequency band (vocals/mids)
        high: Energy for high frequency band (treble/air)
        timestamp: Unix timestamp when analysis was performed
    """

    low: BandEnergy
    mid: BandEnergy
    high: BandEnergy
    timestamp: float


class FrequencyAnalyzer:
    """Process raw FFT data into normalized band energies.

    This analyzer maps FFT bins to frequency bands defined in config,
    applies exponential moving average smoothing, and normalizes
    values to 0-1 range for visualization.

    Attributes:
        calibration: AudioCalibration settings for FFT size, smoothing, sensitivity
    """

    def __init__(self, calibration: AudioCalibration):
        """Initialize the frequency analyzer.

        Args:
            calibration: AudioCalibration instance with processing parameters
        """
        self.calibration = calibration
        # Initialize smoothing buffer for EMA
        self._smoothing_buffer: Dict[str, float] = {"low": 0.0, "mid": 0.0, "high": 0.0}
        # Cache frequency bands
        self._bands = get_all_bands()

    def analyze(self, fft_data: List[float]) -> AnalysisResult:
        """Extract band energies from FFT bins.

        Maps FFT magnitude values to frequency bands based on sample rate
        and FFT size, applies smoothing, and normalizes to 0-1 range.

        Args:
            fft_data: Raw FFT magnitude values (0-255 from Web Audio API)

        Returns:
            AnalysisResult with normalized band energies for all frequency bands
        """
        import time

        # Calculate bin range for each band
        fft_size = self.calibration.fft_size
        sample_rate = 44100  # Standard Web Audio API sample rate

        # Process each band
        band_energies: Dict[str, BandEnergy] = {}

        for band in self._bands:
            band_name = band.name

            # Convert frequency boundaries to bin indices
            start_bin = self._hz_to_bin(band.low_hz, sample_rate, fft_size)
            end_bin = self._hz_to_bin(band.high_hz, sample_rate, fft_size)

            # Clamp bin indices to valid range
            start_bin = max(1, min(start_bin, len(fft_data) - 1))
            end_bin = max(start_bin + 1, min(end_bin, len(fft_data)))

            # Calculate average energy in the band
            raw_energy = self._calculate_band_energy(fft_data, start_bin, end_bin)

            # Apply smoothing (exponential moving average)
            smoothed_energy = self._apply_smoothing(band_name, raw_energy)

            # Normalize to 0-1 range with sensitivity
            normalized = self._normalize_energy(smoothed_energy)

            band_energies[band_name] = BandEnergy(
                band_name=band_name, raw_value=raw_energy, normalized=normalized
            )

        return AnalysisResult(
            low=band_energies["low"],
            mid=band_energies["mid"],
            high=band_energies["high"],
            timestamp=time.time(),
        )

    def _calculate_band_energy(
        self, fft_data: List[float], start_bin: int, end_bin: int
    ) -> float:
        """Calculate average energy across FFT bins in a frequency range.

        Args:
            fft_data: Raw FFT magnitude values
            start_bin: Starting bin index (inclusive)
            end_bin: Ending bin index (exclusive)

        Returns:
            Average energy value across the bin range
        """
        if end_bin <= start_bin:
            return 0.0

        # Sum energy in the bin range
        total = 0.0
        count = 0
        for i in range(start_bin, end_bin):
            if i < len(fft_data):
                total += fft_data[i]
                count += 1

        if count == 0:
            return 0.0

        return total / count

    def _apply_smoothing(self, band_name: str, new_value: float) -> float:
        """Apply exponential moving average smoothing.

        Uses the calibration's smoothing factor to blend current value
        with previous smoothed value, reducing jitter.

        Args:
            band_name: Band identifier ("low", "mid", "high")
            new_value: New raw energy value

        Returns:
            Smoothed energy value
        """
        smoothing_factor = self.calibration.smoothing
        previous_value = self._smoothing_buffer.get(band_name, 0.0)

        # EMA formula: smoothed = smoothing * previous + (1 - smoothing) * new
        smoothed = (
            smoothing_factor * previous_value + (1.0 - smoothing_factor) * new_value
        )

        # Update buffer
        self._smoothing_buffer[band_name] = smoothed

        return smoothed

    def _normalize_energy(self, energy: float) -> float:
        """Normalize energy to 0-1 range with sensitivity applied.

        Applies sensitivity multiplier and clamps result to 0.0-1.0 range.

        Args:
            energy: Raw or smoothed energy value

        Returns:
            Normalized value clamped to 0.0-1.0
        """
        # Apply sensitivity (maps 0-255 to adjusted range)
        sensitivity = self.calibration.sensitivity_multiplier
        normalized = energy * sensitivity

        # Clamp to 0-1 range
        return max(0.0, min(1.0, normalized))

    def _fft_bin_to_hz(self, bin_index: int, sample_rate: int = 44100) -> float:
        """Convert FFT bin index to frequency in Hz.

        Args:
            bin_index: FFT bin index
            sample_rate: Audio sample rate in Hz (default 44100)

        Returns:
            Frequency in Hz corresponding to the bin
        """
        fft_size = self.calibration.fft_size
        return bin_index * sample_rate / fft_size

    def _hz_to_bin(
        self, freq_hz: float, sample_rate: int = 44100, fft_size: int = None
    ) -> int:
        """Convert frequency in Hz to FFT bin index.

        Args:
            freq_hz: Frequency in Hz
            sample_rate: Audio sample rate in Hz (default 44100)
            fft_size: FFT size (defaults to calibration value)

        Returns:
            FFT bin index (integer, rounded)
        """
        if fft_size is None:
            fft_size = self.calibration.fft_size
        return int(freq_hz * fft_size / sample_rate)

    def reset_smoothing(self) -> None:
        """Reset smoothing buffer to zero for all bands.

        Call this when starting a new audio stream or after a pause
        to prevent stale values from affecting new analysis.
        """
        self._smoothing_buffer = {"low": 0.0, "mid": 0.0, "high": 0.0}

    def get_current_smoothing_values(self) -> Dict[str, float]:
        """Get current smoothed values without processing new data.

        Returns:
            Dictionary of current smoothed values by band name
        """
        return self._smoothing_buffer.copy()
