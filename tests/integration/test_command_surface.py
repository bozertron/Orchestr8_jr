import pytest
from orchestr8_next.city.temporal_state import TemporalStateService
from orchestr8_next.city.command_surface import CommandSurface

def test_command_surface_temporal_integration():
    """Verify CommandSurface can query temporal state."""
    temporal = TemporalStateService()
    temporal.start_epoch("P07")
    temporal.record_quantum("test_event", "user_1", {"data": "find_me"})
    
    surface = CommandSurface()
    surface.register_default_commands(temporal)
    
    # 1. Test query_history command
    results = surface.execute_command("query_history", query="find_me")
    assert len(results) == 1
    assert results[0].payload["data"] == "find_me"
    
    # 2. Test time_machine (snapshot)
    # create_snapshot returns sid and stores Snapshot object in temporal._snapshots
    sid = temporal.create_snapshot("Checkpoint", [])
    
    # We need a predictable ID for the test
    temporal._snapshots[sid].id = "100" 
    
    snap = surface.execute_command("time_machine", quantum_id=100)
    assert snap is not None
    assert snap.description == "Checkpoint"
