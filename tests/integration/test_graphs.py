import pytest
import os
import time
from orchestr8_next.city.topology import CityTopologyBuilder
from orchestr8_next.city.heatmap import TimeService

def test_c1_01_topology_builder(tmp_path):
    """Verify clean room topology generation."""
    builder = CityTopologyBuilder()
    
    # Create test structure in tmp_path (which is a pathlib Path)
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test.md"
    p.write_text("content")
    
    # Build
    # Note: build_from_fs takes str
    nodes, connections = builder.build_from_file_system(str(tmp_path))
    
    # Check
    assert len(nodes) >= 2 # Root + subdir
    # connections should exist
    assert len(connections) >= 1

def test_c1_02_heatmap_bucketing():
    """Verify clean room time bucketing logic."""
    service = TimeService()
    
    base_time = 1700000000.0 # Just a timestamp ~2023
    
    # Create events: 2 in first hour, 1 in second hour
    events = [
        {"timestamp": base_time + 10}, 
        {"timestamp": base_time + 50}, 
        {"timestamp": base_time + 3700}
    ]
    
    # Bucket by Hour
    buckets = service.bucket_events(events, interval_seconds=3600)
    
    # Verify
    assert len(buckets) == 2
    assert buckets[0].count == 2
    assert buckets[1].count == 1
    
    # Verify Intensity Normalization
    intensity = service.compute_heatmap_intensity(buckets)
    assert intensity[0] == 1.0 # 2/2
    assert intensity[1] == 0.5 # 1/2
