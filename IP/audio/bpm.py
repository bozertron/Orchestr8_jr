"""BPM detection and event clock for discrete audio beat events.

Provides beat detection from audio energy peaks and an event-driven clock
for triggering discrete visual effects on beats (no continuous animation loops).
"""

from dataclasses import dataclass, field
from typing import Callable, Optional
import time


@dataclass
class BeatEvent:
    """Represents a detected beat for discrete event triggering.

    Attributes:
        bpm: Estimated BPM from recent beat intervals
        beat_strength: Intensity of beat (0.0-1.0)
        timestamp: Unix timestamp when beat was detected
        beat_number: Sequential count since detector start
    """

    bpm: float
    beat_strength: float
    timestamp: float
    beat_number: int


class BPMDetector:
    """Detect BPM from audio energy peaks (onset detection).

    Uses a peak picking algorithm to detect onsets and estimates BPM
    from the intervals between detected beats.
    """

    def __init__(
        self,
        min_bpm: float = 60.0,
        max_bpm: float = 200.0,
        onset_threshold: float = 0.3,
        history_size: int = 43,  # ~1 second at 60fps, ~2s at 30fps
        min_onset_interval: float = 0.2,  # Minimum 300 BPM gap
    ):
        """Initialize BPM detector.

        Args:
            min_bpm: Minimum expected BPM (default 60)
            max_bpm: Maximum expected BPM (default 200)
            onset_threshold: Energy threshold to trigger onset detection (0.0-1.0)
            history_size: Number of energy samples to track for peak detection
            min_onset_interval: Minimum seconds between onsets
        """
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm
        self.onset_threshold = onset_threshold
        self.history_size = history_size
        self.min_onset_interval = min_onset_interval

        self._energy_history: list[float] = []
        self._onset_times: list[float] = []
        self._last_beat_time: float = 0.0
        self._beat_count: int = 0
        self._peak_buffer: float = 0.0
        self._peak_decay: float = 0.95  # Exponential decay for adaptive threshold

    def detect(self, energy: float) -> Optional[BeatEvent]:
        """Detect if current energy is an onset (beat).

        Args:
            energy: Current audio energy (0.0-1.0)

        Returns:
            BeatEvent if onset detected, None otherwise
        """
        current_time = time.time()

        # Add energy to history
        self._energy_history.append(energy)
        if len(self._energy_history) > self.history_size:
            self._energy_history.pop(0)

        # Update adaptive peak buffer with decay
        self._peak_buffer = max(self._peak_buffer * self._peak_decay, energy)

        # Check minimum interval since last beat
        if self._last_beat_time > 0:
            time_since_last = current_time - self._last_beat_time
            if time_since_last < self.min_onset_interval:
                return None

        # Peak picking: detect onset if energy exceeds adaptive threshold
        adaptive_threshold = max(
            self.onset_threshold,
            self._peak_buffer * 0.6,  # Must be 60% of recent peak
        )

        if energy >= adaptive_threshold:
            # Validate it's a local peak (not just sustained energy)
            if self._is_local_peak():
                return self._create_beat_event(current_time, energy)

        return None

    def _is_local_peak(self) -> bool:
        """Check if current energy is a local peak in history.

        Compares current sample to neighbors to avoid detecting
        sustained energy as repeated beats.
        """
        if len(self._energy_history) < 3:
            return True  # Not enough history, allow first beats

        current = self._energy_history[-1]
        # Check if current is greater than both neighbors
        if len(self._energy_history) >= 3:
            prev1 = self._energy_history[-2]
            prev2 = self._energy_history[-3]

            # Must be at least as strong as recent samples to be a peak
            # This prevents sustained energy from triggering multiple beats
            return current >= prev1 and current >= prev2 * 0.9

        return True

    def _create_beat_event(self, timestamp: float, energy: float) -> BeatEvent:
        """Create a BeatEvent and update internal state."""
        # Record onset time
        self._onset_times.append(timestamp)
        self._last_beat_time = timestamp
        self._beat_count += 1

        # Keep only recent onset times (last 20 beats for BPM calculation)
        if len(self._onset_times) > 20:
            self._onset_times.pop(0)

        # Calculate beat strength based on energy relative to peak
        beat_strength = min(1.0, energy / max(self._peak_buffer, 0.01))

        # Reset peak buffer on beat detection
        self._peak_buffer = energy * 0.7

        return BeatEvent(
            bpm=self.get_current_bpm(),
            beat_strength=beat_strength,
            timestamp=timestamp,
            beat_number=self._beat_count,
        )

    def get_current_bpm(self) -> float:
        """Get estimated BPM from recent beats.

        Returns:
            Estimated BPM, or 0.0 if insufficient data
        """
        if len(self._onset_times) < 2:
            return 0.0

        # Calculate intervals between consecutive beats
        intervals = []
        for i in range(1, len(self._onset_times)):
            interval = self._onset_times[i] - self._onset_times[i - 1]
            # Filter out intervals outside expected BPM range
            interval_bpm = 60.0 / interval if interval > 0 else 0
            if self.min_bpm <= interval_bpm <= self.max_bpm:
                intervals.append(interval)

        if not intervals:
            return 0.0

        # Use median interval for robustness against outliers
        intervals.sort()
        median_interval = intervals[len(intervals) // 2]

        if median_interval > 0:
            bpm = 60.0 / median_interval
            # Clamp to valid range
            return max(self.min_bpm, min(self.max_bpm, bpm))

        return 0.0

    def reset(self):
        """Reset detector state for fresh BPM detection."""
        self._energy_history.clear()
        self._onset_times.clear()
        self._last_beat_time = 0.0
        self._beat_count = 0
        self._peak_buffer = 0.0


class EventClock:
    """Clock for discrete event bursts (no continuous loops).

    Provides event-driven callbacks that fire exactly once per detected beat.
    Users define what happens on each beat - no continuous animation tied to audio.
    """

    def __init__(self, bpm_detector: Optional[BPMDetector] = None):
        """Initialize event clock.

        Args:
            bpm_detector: Optional BPM detector instance.
                         If None, creates a default BPMDetector.
        """
        self.detector = bpm_detector or BPMDetector()
        self._beat_callbacks: list[Callable[[BeatEvent], None]] = []
        self._last_beat_number: int = -1
        self._start_time: float = time.time()

    def on_beat(
        self, callback: Callable[[BeatEvent], None]
    ) -> Callable[[BeatEvent], None]:
        """Register callback for beat events.

        Callback receives BeatEvent - caller decides what to do.
        NO continuous animation loops - discrete events only.

        Args:
            callback: Function to call on each beat

        Returns:
            The callback (for decorator pattern compatibility)
        """
        self._beat_callbacks.append(callback)
        return callback

    def tick(self, energy: float) -> Optional[BeatEvent]:
        """Process one audio sample tick.

        Args:
            energy: Current audio energy (0.0-1.0)

        Returns:
            BeatEvent if new beat detected, None otherwise
        """
        beat = self.detector.detect(energy)

        # Fire callbacks only on new beats (not repeated)
        if beat and beat.beat_number > self._last_beat_number:
            self._last_beat_number = beat.beat_number
            for cb in self._beat_callbacks:
                cb(beat)  # Fire discrete event

        return beat

    def get_beat_phase(self) -> float:
        """Get phase within current beat (0.0-1.0) for interpolation.

        Returns:
            0.0 at beat, approaching 1.0 just before next beat.
            Returns 0.0 if no beats detected yet.
        """
        if self._last_beat_number < 0:
            return 0.0

        current_time = time.time()
        bpm = self.detector.get_current_bpm()

        if bpm <= 0:
            return 0.0

        beat_duration = 60.0 / bpm
        time_since_beat = current_time - self.detector._last_beat_time

        # Phase grows from 0 to 1 over the beat duration
        phase = time_since_beat / beat_duration

        # Clamp to 0-1 range
        return min(1.0, max(0.0, phase))

    def get_bpm(self) -> float:
        """Get current estimated BPM.

        Returns:
            Current BPM estimate from detector
        """
        return self.detector.get_current_bpm()

    def get_beat_count(self) -> int:
        """Get total number of beats detected since start.

        Returns:
            Beat count
        """
        return self._last_beat_number + 1

    def reset(self):
        """Reset clock state."""
        self.detector.reset()
        self._last_beat_number = -1
        self._start_time = time.time()


# Convenience function for quick setup
def create_event_clock(
    min_bpm: float = 60.0,
    max_bpm: float = 200.0,
    onset_threshold: float = 0.3,
) -> EventClock:
    """Create an EventClock with a configured BPMDetector.

    Args:
        min_bpm: Minimum expected BPM
        max_bpm: Maximum expected BPM
        onset_threshold: Energy threshold for beat detection

    Returns:
        Configured EventClock instance
    """
    detector = BPMDetector(
        min_bpm=min_bpm,
        max_bpm=max_bpm,
        onset_threshold=onset_threshold,
    )
    return EventClock(bpm_detector=detector)
