import pytest
import time
from orchestr8_next.city.temporal_state import TemporalStateService, Epoch, Snapshot
from orchestr8_next.city.tour_service import TourService

def test_epoch_lifecycle():
    """Verify Epoch management (MSL-MOD-03)."""
    service = TemporalStateService()
    
    # Start
    e1_id = service.start_epoch("P07-B5")
    assert e1_id
    active = service.get_active_epoch()
    assert active.id == e1_id
    assert active.status == "active"
    
    # End
    service.end_epoch(e1_id)
    assert service.get_active_epoch() is None
    
    # Start New
    e2_id = service.start_epoch("P08")
    assert e2_id != e1_id
    assert service.get_active_epoch().id == e2_id

def test_quantum_stream():
    """Verify Quantum event recording."""
    service = TemporalStateService()
    
    # Record events
    q1 = service.record_quantum("commit", "agent-x", {"lines": 10})
    q2 = service.record_quantum("log", "system", {"level": "info"})
    
    timeline = service.get_timeline()
    assert len(timeline) == 2
    assert timeline[0].type == "commit"

def test_snapshot_creation():
    """Verify Snapshot logic."""
    service = TemporalStateService()
    
    # No active epoch -> None
    s1 = service.create_snapshot("desc", [])
    assert s1 is None
    
    # Active Epoch
    eid = service.start_epoch("Test")
    s2 = service.create_snapshot("Checkpoint 1", ["/file/path"])
    assert s2
    
    # Retrieve
    assert s2 in service._snapshots
    assert service._snapshots[s2].epoch_id == eid
    assert service._snapshots[s2].artifact_refs == ["/file/path"]

def test_persistence(tmp_path):
    """Verify save/load to disk."""
    service = TemporalStateService()
    service.start_epoch("P07")
    service.record_quantum("event", "user", {"data": 1})
    
    file_path = tmp_path / "temporal_state.json"
    service.export_persistence(str(file_path))
    
    # Load back
    new_service = TemporalStateService.import_persistence(str(file_path))
    assert len(new_service._epochs) == 1
    assert len(new_service._timeline) == 1
    assert new_service._timeline[0].payload["data"] == 1

def test_tour_integration():
    """Verify TourService records quantum events."""
    temporal = TemporalStateService()
    tour = TourService(temporal_service=temporal)
    
    from orchestr8_next.city.tour_service import TourStep
    tour.load_tour([TourStep("1", "Title", "Content")])
    
    tour.start_tour()
    assert len(temporal.get_timeline()) == 1
    assert temporal.get_timeline()[0].type == "tour_start"

def test_conversation_integration():
    """Verify AgentConversationService records quantum events."""
    temporal = TemporalStateService()
    from orchestr8_next.city.agent_conversation import AgentConversationService, MessageType
    conv = AgentConversationService(temporal_service=temporal)
    
    conv.post_message(MessageType.USER, "Hello", "user-1")
    assert len(temporal.get_timeline()) == 1
    assert temporal.get_timeline()[0].type == "conversation_msg"
    
def test_quantum_increment():
    """Verify MSL-04 3.1: Atomic increment."""
    service = TemporalStateService()
    service.start_epoch("P07")
    
    q1 = service.advance_quantum("test_trigger")
    assert q1 == 1
    
    q2 = service.advance_quantum("test_trigger")
    assert q2 == 2
    assert q2 > q1

def test_historical_snapshot_retrieval():
    """Verify MSL-04 3.2: Immutable access."""
    service = TemporalStateService()
    service.start_epoch("P07")
    
    # Create snapshot pinned to a specific ID
    sid = "1450"
    service._snapshots[sid] = Snapshot(
        id=sid,
        timestamp=time.time(),
        epoch_id="P07",
        artifact_refs=["hash1"],
        description="Historical"
    )
    
    snap = service.get_snapshot_by_quantum(1450)
    assert snap is not None
    assert snap.artifact_refs == ["hash1"]

def test_full_city_cycle():
    """Verify MSL-04 4: Sync Loop."""
    # This test proves interoperability between services using temporal state as a bus
    temporal = TemporalStateService()
    temporal.start_epoch("P07")
    
    # 1. Citizen Moves
    temporal.record_quantum("CITIZEN_MOVED", "orchestr8_jr", {"to": "shell"})
    
    # 2. Grid Outage
    temporal.record_quantum("GRID_OUTAGE", "power_grid", {"severity": "RED"})
    
    # 3. Quantum Tick
    tid = temporal.advance_quantum("QUANTUM_TICK")
    
    timeline = temporal.get_timeline()
    assert len(timeline) == 3
    assert timeline[0].type == "CITIZEN_MOVED"
    assert timeline[1].type == "GRID_OUTAGE"
    assert timeline[2].id == str(tid)

def test_bucketed_activity():
    """Verify MSL-04 3.1 / P07-C5-01: Activity Bucketization."""
    service = TemporalStateService()
    service.start_epoch("P07")
    
    now = time.time()
    # Record events at different times
    service.record_quantum("e1", "u1", {}, timestamp=now - 50)
    service.record_quantum("e2", "u1", {}, timestamp=now - 40)
    service.record_quantum("e3", "u1", {}, timestamp=now - 10)
    
    # Bucketize last 60 seconds into 3 buckets (20s each)
    buckets = service.get_bucketed_activity(now - 60, now, bucket_count=3)
    
    assert len(buckets) == 3
    # Bucket 0: [now-60, now-40) -> e1
    assert buckets[0]["count"] == 1
    # Bucket 1: [now-40, now-20) -> e2
    assert buckets[1]["count"] == 1
    # Bucket 2: [now-20, now) -> e3
    assert buckets[2]["count"] == 1

def test_search_history():
    """Verify P07-C5-02: History Search/Filtering."""
    service = TemporalStateService()
    service.start_epoch("P07")
    
    service.record_quantum("type_a", "user_1", {"key": "secret_data"})
    service.record_quantum("type_b", "user_2", {"key": "other_data"})
    
    # Search by type
    results = service.search_history(type_filter="type_a")
    assert len(results) == 1
    assert results[0].source_id == "user_1"
    
    # Search by query (payload)
    results = service.search_history(query="secret")
    assert len(results) == 1
    assert results[0].payload["key"] == "secret_data"
    
    # Search by query (source)
    results = service.search_history(query="user_2")
    assert len(results) == 1
    assert results[0].type == "type_b"
