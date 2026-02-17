"""Effect mapper module for Orchestr8 Code City visualization.

Maps audio band energies to effect parameters for audio-reactive
particle system effects.
"""

from dataclasses import dataclass
from typing import Tuple

from IP.audio.analyzer import AnalysisResult


@dataclass
class EffectParams:
    """Effect parameters driven by audio bands.

    Attributes:
        amplitude: Driven by high frequency band (controls particle brightness/intensity)
        offset_gain: Driven by mid frequency band (controls swirl/offset strength)
        time_step: Driven by low frequency band (controls movement speed/flow)
    """

    amplitude: float  # Driven by high band (0.0-1.0)
    offset_gain: float  # Driven by mid band (0.0-1.0)
    time_step: float  # Driven by low band (0.0-1.0)

    def clamp(self) -> "EffectParams":
        """Clamp all values to safe 0.0-1.0 bounds.

        Returns:
            New EffectParams with all values clamped to [0.0, 1.0]
        """
        return EffectParams(
            amplitude=max(0.0, min(1.0, self.amplitude)),
            offset_gain=max(0.0, min(1.0, self.offset_gain)),
            time_step=max(0.0, min(1.0, self.time_step)),
        )


@dataclass
class MappingConfig:
    """Configuration for band → parameter mapping.

    Defines input ranges from audio analysis and output ranges
    for effect parameters.

    Attributes:
        input_min: Minimum input value from audio bands (default 0.0)
        input_max: Maximum input value from audio bands (default 1.0)
        amplitude_range: Output range for amplitude parameter (default 0.0-1.0)
        offset_gain_range: Output range for offset_gain parameter (default 0.0-1.0)
        time_step_range: Output range for time_step parameter (default 0.0-1.0)
    """

    # Input ranges (audio band normalized values)
    input_min: float = 0.0
    input_max: float = 1.0

    # Output ranges (effect parameter bounds)
    amplitude_range: Tuple[float, float] = (0.0, 1.0)
    offset_gain_range: Tuple[float, float] = (0.0, 1.0)
    time_step_range: Tuple[float, float] = (0.0, 1.0)


class EffectMapper:
    """Maps audio band energies to effect parameters.

    Provides deterministic mapping from frequency band analysis
    to particle system effect parameters:
    - high band → amplitude (particle brightness/intensity)
    - mid band → offset_gain (swirl/offset strength)
    - low band → time_step (movement speed/flow)

    All outputs are clamped to safe bounds for stability.
    """

    def __init__(self, config: MappingConfig = None):
        """Initialize the effect mapper.

        Args:
            config: Mapping configuration (uses defaults if None)
        """
        self.config = config or MappingConfig()

    def map(self, analysis: AnalysisResult) -> EffectParams:
        """Convert band energies to effect parameters.

        Maps frequency band analysis results to effect parameters
        using configured mapping ranges.

        Args:
            analysis: Band energies from audio analyzer

        Returns:
            EffectParams with clamped values (0.0-1.0)
        """
        # high -> amplitude (particle brightness/intensity)
        high_val = analysis.high.normalized
        amplitude = self._map_range(
            high_val,
            self.config.input_min,
            self.config.input_max,
            *self.config.amplitude_range,
        )

        # mid -> offset_gain (swirl/offset strength)
        mid_val = analysis.mid.normalized
        offset_gain = self._map_range(
            mid_val,
            self.config.input_min,
            self.config.input_max,
            *self.config.offset_gain_range,
        )

        # low -> time_step (movement speed/flow)
        low_val = analysis.low.normalized
        time_step = self._map_range(
            low_val,
            self.config.input_min,
            self.config.input_max,
            *self.config.time_step_range,
        )

        return EffectParams(amplitude, offset_gain, time_step).clamp()

    def _map_range(
        self, value: float, in_min: float, in_max: float, out_min: float, out_max: float
    ) -> float:
        """Map value from input range to output range with clamping.

        Uses linear mapping with output bounds clamping for stability.

        Args:
            value: Input value to map
            in_min: Input range minimum
            in_max: Input range maximum
            out_min: Output range minimum
            out_max: Output range maximum

        Returns:
            Mapped value clamped to [out_min, out_max]
        """
        # Avoid division by zero
        if in_max == in_min:
            return out_min

        # Linear map: value -> output range
        mapped = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        # Clamp to output bounds for stability
        return max(out_min, min(out_max, mapped))

    def get_mapping_summary(self, analysis: AnalysisResult) -> dict:
        """Get detailed mapping information for debugging/visualization.

        Args:
            analysis: Band energies from audio analyzer

        Returns:
            Dictionary with input values, mapped outputs, and config used
        """
        params = self.map(analysis)

        return {
            "inputs": {
                "high": analysis.high.normalized,
                "mid": analysis.mid.normalized,
                "low": analysis.low.normalized,
            },
            "outputs": {
                "amplitude": params.amplitude,
                "offset_gain": params.offset_gain,
                "time_step": params.time_step,
            },
            "mapping": {
                "high -> amplitude": f"{analysis.high.normalized:.3f} → {params.amplitude:.3f}",
                "mid -> offset_gain": f"{analysis.mid.normalized:.3f} → {params.offset_gain:.3f}",
                "low -> time_step": f"{analysis.low.normalized:.3f} → {params.time_step:.3f}",
            },
        }
