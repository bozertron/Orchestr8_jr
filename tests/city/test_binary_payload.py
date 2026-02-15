import pytest
import traitlets
import json
import uuid
from unittest.mock import MagicMock
from orchestr8_next.city.widget import CodeCityWidget

# Constants form widget
MAX_CHUNK_SIZE = 4 * 1024 * 1024

def test_send_small_payload():
    """Test sending a payload smaller than MAX_CHUNK_SIZE (single chunk)."""
    widget = CodeCityWidget()
    
    # Payload < 4MB
    data = {"nodes": [{"id": "n1", "val": 10}]}
    widget.send_scene_data(data)
    
    # Assert trait values
    assert widget.chunk_meta["chunk_total"] == 1
    assert widget.chunk_meta["chunk_index"] == 0
    assert len(widget.chunk_data) > 0
    
    # Verify content
    decoded = json.loads(widget.chunk_data.decode("utf-8"))
    assert decoded["nodes"][0]["id"] == "n1"

def test_send_large_payload_chunking():
    """Test sending a payload larger than MAX_CHUNK_SIZE (forces multiple chunks)."""
    
    # Mock the MAX_CHUNK_SIZE by monkeypatching? 
    # Since constants are imported at module level, difficult.
    # Instead, generate a HUGE payload > 4MB.
    
    # 5MB String
    large_str = "x" * (5 * 1024 * 1024)
    data = {"big_data": large_str}
    
    widget = CodeCityWidget()
    
    # We need to capture the trait changes because send_scene_data loops
    # and overwrites the trait values for each chunk.
    # We use a traitlets observer.
    
    captured_chunks = []
    captured_metas = []
    
    def on_change(change):
        if change['name'] == 'chunk_data':
            captured_chunks.append(change['new'])
        elif change['name'] == 'chunk_meta':
            captured_metas.append(change['new'])
            
    widget.observe(on_change, names=['chunk_data', 'chunk_meta'])
    
    widget.send_scene_data(data)
    
    # Verify multiple chunks were sent
    assert len(captured_chunks) >= 2
    assert len(captured_metas) >= 2
    
    # Verify metadata sequence
    first_meta = captured_metas[0]
    last_meta = captured_metas[-1]
    
    assert first_meta["chunk_index"] == 0
    assert last_meta["chunk_index"] == last_meta["chunk_total"] - 1
    assert first_meta["payload_id"] == last_meta["payload_id"]
    
    # Verify Reassembly
    total_bytes = b"".join(captured_chunks)
    decoded = json.loads(total_bytes.decode("utf-8"))
    assert decoded["big_data"] == large_str

def test_malformed_chunk_handling():
    """Test that ensures metadata is consistent."""
    widget = CodeCityWidget()
    data = {"test": "data"}
    widget.send_scene_data(data)
    
    # Metadata should have basic fields
    meta = widget.chunk_meta
    assert "payload_id" in meta
    assert "chunk_index" in meta
    assert "chunk_total" in meta
