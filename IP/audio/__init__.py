"""Audio module for Orchestr8 Code City visualization.

Provides FFT analysis and frequency band extraction for audio-reactive
visualization effects.

Exports:
    FrequencyAnalyzer: Main class for processing FFT data
    BandEnergy: Normalized energy for a frequency band
    AnalysisResult: Complete analysis result for all bands
    AudioCalibration: Calibration settings
    FrequencyBand: Frequency band definition
"""

from IP.audio.config import (
    FrequencyBand,
    AudioCalibration,
    get_band_by_name,
    get_all_bands,
    LOW_BAND,
    MID_BAND,
    HIGH_BAND,
    DEFAULT_FFT_SIZE,
    DEFAULT_SMOOTHING,
    SENSITIVITY_RANGE,
)

from IP.audio.analyzer import (
    FrequencyAnalyzer,
    BandEnergy,
    AnalysisResult,
)

from IP.audio.mapper import (
    EffectMapper,
    EffectParams,
    MappingConfig,
)

from IP.audio.bpm import (
    BeatEvent,
    BPMDetector,
    EventClock,
    create_event_clock,
)

from IP.audio.bridge import (
    AudioBridge,
    AudioBridgeConfig,
    create_bridge,
    get_audio_bridge,
    reset_audio_bridge,
)

__all__ = [
    # Config exports
    "FrequencyBand",
    "AudioCalibration",
    "get_band_by_name",
    "get_all_bands",
    "LOW_BAND",
    "MID_BAND",
    "HIGH_BAND",
    "DEFAULT_FFT_SIZE",
    "DEFAULT_SMOOTHING",
    "SENSITIVITY_RANGE",
    # Analyzer exports
    "FrequencyAnalyzer",
    "BandEnergy",
    "AnalysisResult",
    # Mapper exports
    "EffectMapper",
    "EffectParams",
    "MappingConfig",
    # BPM exports
    "BeatEvent",
    "BPMDetector",
    "EventClock",
    "create_event_clock",
    # Bridge exports
    "AudioBridge",
    "AudioBridgeConfig",
    "create_bridge",
    "get_audio_bridge",
    "reset_audio_bridge",
]
