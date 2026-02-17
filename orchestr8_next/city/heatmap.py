from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class TimeBucket:
    def __init__(self, start_ts: float, end_ts: float, count: int = 0):
        self.start = start_ts
        self.end = end_ts
        self.count = count

class TimeService:
    """
    Core Logic: Buckets activity events into temporal ranges for heatmap layers.
    Ref: P07-C1-02 ActivityGraph -> SessionActivityGraph.tsx (clean-room).
    """
    
    def bucket_events(self, events: List[Dict[str, Any]], interval_seconds: int = 3600) -> List[TimeBucket]:
        """
        Accepts generic events (must have 'timestamp' key).
        Returns list of uniform time buckets.
        """
        if not events:
            return []
            
        # Get Range
        timestamps = [e.get('timestamp', 0) for e in events]
        if not timestamps:
             return []
             
        min_ts = min(timestamps)
        max_ts = max(timestamps)
        
        # Round down to nearest interval start
        bucket_start = (min_ts // interval_seconds) * interval_seconds
        buckets = []
        
        current = bucket_start
        # Ensure we cover the full range
        while current <= max_ts:
            end = current + interval_seconds
            count = sum(1 for ts in timestamps if current <= ts < end)
            buckets.append(TimeBucket(current, end, count))
            current = end
            
        return buckets

    def compute_heatmap_intensity(self, buckets: List[TimeBucket]) -> List[float]:
        """
        Normalizes bucket counts to 0.0-1.0 intensity scale.
        """
        if not buckets: return []
        max_count = max((b.count for b in buckets), default=1)
        return [b.count / max_count for b in buckets]
