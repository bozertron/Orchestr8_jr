"""Audio bridge module for Orchestr8 Code City visualization.

Provides JavaScript integration helpers to bridge Python audio modules
with the frontend Web Audio API.

The JavaScript frontend captures audio via Web Audio API and sends raw
FFT data to Python. This bridge module:
1. Accepts FFT data from JS
2. Processes through analyzer + mapper
3. Returns effect params to JS
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, Callable, List
import json

from IP.audio.config import AudioCalibration, DEFAULT_FFT_SIZE, DEFAULT_SMOOTHING
from IP.audio.analyzer import FrequencyAnalyzer, AnalysisResult
from IP.audio.mapper import EffectMapper, EffectParams
from IP.audio.bpm import BPMDetector, EventClock, BeatEvent


@dataclass
class AudioBridgeConfig:
    """Configuration for the audio bridge.

    Attributes:
        fft_size: FFT window size (power of 2, default 256)
        smoothing: Exponential smoothing factor (0-1, default 0.82)
        sensitivity: Overall sensitivity multiplier (1-100, default 50)
        enable_bpm: Whether to enable BPM detection
        bpm_min: Minimum expected BPM (default 60.0)
        bpm_max: Maximum expected BPM (default 200.0)
    """

    fft_size: int = DEFAULT_FFT_SIZE
    smoothing: float = DEFAULT_SMOOTHING
    sensitivity: int = 50
    enable_bpm: bool = True
    bpm_min: float = 60.0
    bpm_max: float = 200.0

    def __post_init__(self):
        """Validate configuration parameters."""
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
        if not 1 <= self.sensitivity <= 100:
            raise ValueError(
                f"sensitivity must be between 1 and 100, got {self.sensitivity}"
            )
        if self.bpm_min < 30.0 or self.bpm_max > 300.0:
            raise ValueError(
                f"BPM range must be between 30 and 300, got {self.bpm_min}-{self.bpm_max}"
            )
        if self.bpm_min >= self.bpm_max:
            raise ValueError(
                f"bpm_min must be less than bpm_max, got {self.bpm_min}-{self.bpm_max}"
            )


class AudioBridge:
    """Bridge between JavaScript Web Audio API and Python audio modules.

    This class provides the main integration point for JavaScript frontend
    code (woven_maps.js) to send FFT data to Python for processing.

    Usage:
        # Initialize bridge
        bridge = AudioBridge()

        # Process incoming FFT data from JavaScript
        result = bridge.process_fft([128, 64, 32, ...])  # List of FFT magnitudes

        # Get result for JavaScript
        # {
        #     "bands": {"low": 0.5, "mid": 0.3, "high": 0.2},
        #     "effects": {"amplitude": 0.2, "offset_gain": 0.3, "time_step": 0.5},
        #     "beat": {"bpm": 120.0, "beat_strength": 0.8, ...} or None
        # }
    """

    def __init__(self, config: Optional[AudioBridgeConfig] = None):
        """Initialize the audio bridge.

        Args:
            config: AudioBridgeConfig instance (uses defaults if None)
        """
        self.config = config or AudioBridgeConfig()

        # Initialize Python audio pipeline
        calibration = AudioCalibration(
            fft_size=self.config.fft_size,
            smoothing=self.config.smoothing,
            sensitivity=self.config.sensitivity,
        )
        self.analyzer = FrequencyAnalyzer(calibration)
        self.mapper = EffectMapper()

        # BPM detection (optional)
        self.bpm_detector: Optional[BPMDetector] = None
        self.event_clock: Optional[EventClock] = None
        if self.config.enable_bpm:
            self.bpm_detector = BPMDetector(
                min_bpm=self.config.bpm_min, max_bpm=self.config.bpm_max
            )
            self.event_clock = EventClock(self.bpm_detector)

    def process_fft(self, fft_data: List[float]) -> Dict[str, Any]:
        """Process raw FFT data from JavaScript.

        This is the main entry point for JavaScript → Python communication.

        Args:
            fft_data: List of FFT magnitude values (0-255) from Web Audio API

        Returns:
            Dictionary with:
                - bands: Normalized band energies (low, mid, high)
                - effects: Effect parameters for visualization
                - beat: BeatEvent dict if beat detected, None otherwise
        """
        # Analyze FFT data
        analysis = self.analyzer.analyze(fft_data)

        # Map to effect parameters
        effects = self.mapper.map(analysis)

        # Check for beat detection
        beat_event: Optional[Dict[str, Any]] = None
        if self.event_clock:
            # Use low frequency energy for beat detection
            beat = self.event_clock.tick(analysis.low.raw_value / 255.0)
            if beat:
                beat_event = asdict(beat)

        # Build response dict
        return {
            "bands": {
                "low": analysis.low.normalized,
                "mid": analysis.mid.normalized,
                "high": analysis.high.normalized,
            },
            "effects": asdict(effects),
            "beat": beat_event,
        }

    def get_config_json(self) -> str:
        """Get JavaScript-side configuration for Web Audio API setup.

        Returns:
            JSON string with configuration for JS Web Audio API
        """
        return json.dumps(
            {
                "fftSize": self.config.fft_size,
                "smoothing": self.config.smoothing,
                "sensitivity": self.config.sensitivity,
            }
        )

    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as a dictionary.

        Returns:
            Configuration dictionary
        """
        return {
            "fftSize": self.config.fft_size,
            "smoothing": self.config.smoothing,
            "sensitivity": self.config.sensitivity,
            "enableBpm": self.config.enable_bpm,
            "bpmMin": self.config.bpm_min,
            "bpmMax": self.config.bpm_max,
        }

    def register_beat_callback(self, callback: Callable[[BeatEvent], None]) -> None:
        """Register a Python callback for beat events.

        This allows Python code to react to detected beats for
        triggering discrete visual effects.

        Args:
            callback: Function to call on each beat detection
        """
        if self.event_clock:
            self.event_clock.on_beat(callback)

    def reset(self) -> None:
        """Reset the bridge state.

        Clears smoothing buffers and BPM detector state.
        Call this when starting a new audio stream or after a pause.
        """
        self.analyzer.reset_smoothing()
        if self.event_clock:
            self.event_clock.reset()

    def get_current_state(self) -> Dict[str, Any]:
        """Get current bridge state for debugging/visualization.

        Returns:
            Dictionary with current band energies and BPM state
        """
        state = {
            "bands": self.analyzer.get_current_smoothing_values(),
            "bpm": 0.0,
            "beatCount": 0,
        }

        if self.event_clock:
            state["bpm"] = self.event_clock.get_bpm()
            state["beatCount"] = self.event_clock.get_beat_count()

        return state

    @staticmethod
    def from_json(json_str: str) -> "AudioBridge":
        """Create bridge from JSON config (for session restore).

        Args:
            json_str: JSON string with configuration

        Returns:
            New AudioBridge instance with loaded config
        """
        config_data = json.loads(json_str)
        # Handle both full config and JS-side config
        config = AudioBridgeConfig(
            fft_size=config_data.get("fftSize", DEFAULT_FFT_SIZE),
            smoothing=config_data.get("smoothing", DEFAULT_SMOOTHING),
            sensitivity=config_data.get("sensitivity", 50),
            enable_bpm=config_data.get("enableBpm", True),
            bpm_min=config_data.get("bpmMin", 60.0),
            bpm_max=config_data.get("bpmMax", 200.0),
        )
        return AudioBridge(config)

    def to_json(self) -> str:
        """Serialize bridge configuration to JSON.

        Returns:
            JSON string representation of config
        """
        return json.dumps(self.get_config_dict())


# Convenience function for quick setup
def create_bridge(
    fft_size: int = DEFAULT_FFT_SIZE,
    smoothing: float = DEFAULT_SMOOTHING,
    sensitivity: int = 50,
    enable_bpm: bool = True,
) -> AudioBridge:
    """Create an AudioBridge with simple parameters.

    Args:
        fft_size: FFT window size
        smoothing: Smoothing factor
        sensitivity: Sensitivity (1-100)
        enable_bpm: Whether to enable BPM detection

    Returns:
        Configured AudioBridge instance
    """
    config = AudioBridgeConfig(
        fft_size=fft_size,
        smoothing=smoothing,
        sensitivity=sensitivity,
        enable_bpm=enable_bpm,
    )
    return AudioBridge(config)


# Global bridge instance for consistent state across the application
_bridge: Optional[AudioBridge] = None


def get_audio_bridge() -> AudioBridge:
    """Get global AudioBridge instance.

    Returns:
        Global AudioBridge instance
    """
    global _bridge
    if _bridge is None:
        _bridge = AudioBridge()
    return _bridge


def reset_audio_bridge(
    fft_size: int = DEFAULT_FFT_SIZE,
    smoothing: float = DEFAULT_SMOOTHING,
    sensitivity: int = 50,
    enable_bpm: bool = True,
) -> AudioBridge:
    """Reset global AudioBridge with new configuration.

    Args:
        fft_size: FFT window size
        smoothing: Smoothing factor
        sensitivity: Sensitivity (1-100)
        enable_bpm: Whether to enable BPM detection

    Returns:
        New AudioBridge instance
    """
    global _bridge
    config = AudioBridgeConfig(
        fft_size=fft_size,
        smoothing=smoothing,
        sensitivity=sensitivity,
        enable_bpm=enable_bpm,
    )
    _bridge = AudioBridge(config)
    return _bridge
