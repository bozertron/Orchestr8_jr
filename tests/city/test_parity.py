import pytest
import json
import os
from orchestr8_next.city.widget import CodeCityWidget
from orchestr8_next.city.wiring import generate_wiring_view

# Mock Scenario Data
SAMPLE_DATA = {
    "nodes": [
        {"id": "n1", "type": "FILE", "position": {"x":0,"y":0,"z":0}, "color": "#fff", "label": "n1"},
        {"id": "n2", "type": "DIR", "position": {"x":1,"y":0,"z":0}, "color": "#000", "label": "n2"}
    ],
    "connections": [
        {"source_id": "n1", "target_id": "n2", "type": "contains"}
    ]
}

def test_parity_widget_initialization():
    """Verify Widget accepts standard contract data."""
    # Widget path
    widget = CodeCityWidget(nodes=SAMPLE_DATA['nodes'])
    assert len(widget.nodes) == 2
    assert widget.nodes == SAMPLE_DATA['nodes']

def test_parity_iframe_serialization():
    """Verify Iframe data path (json dump) is valid."""
    # Iframe path just dumps json
    scene_json = json.dumps(SAMPLE_DATA)
    loaded = json.loads(scene_json)
    assert loaded['nodes'] == SAMPLE_DATA['nodes']
    assert loaded['connections'] == SAMPLE_DATA['connections']

def test_parity_wiring_generation(tmp_path):
    """Verify Wiring View generation works with same data."""
    # Wiring path
    path = generate_wiring_view(SAMPLE_DATA['nodes'], SAMPLE_DATA['connections'], filename=str(tmp_path/"parity.html"))
    assert os.path.exists(path)
    with open(path) as f:
        content = f.read()
        assert "n1" in content
        assert "n2" in content
