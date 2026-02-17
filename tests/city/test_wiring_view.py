import pytest
import os
from orchestr8_next.city.wiring import generate_wiring_view
from unittest.mock import patch, MagicMock

def test_wiring_view_generates_file(tmp_path):
    """Test that generate_wiring_view creates an HTML file."""
    
    nodes = [{"id": "n1", "label": "Node 1"}]
    connections = []
    
    output_file = tmp_path / "wiring_test.html"
    
    path = generate_wiring_view(nodes, connections, filename=str(output_file))
    
    assert os.path.exists(path)
    assert path == str(output_file.absolute())
    
    with open(path, "r") as f:
        content = f.read()
        assert "Node 1" in content
        assert "n1" in content

def test_wiring_view_connections(tmp_path):
    """Test that connections are rendered."""
    nodes = [{"id": "n1"}, {"id": "n2"}]
    connections = [{"source_id": "n1", "target_id": "n2", "type": "imports"}]
    
    output_file = tmp_path / "wiring_conn.html"
    generate_wiring_view(nodes, connections, filename=str(output_file))
    
    with open(output_file, "r") as f:
        content = f.read()
        # Vis.js format puts edges in JSON inside the HTML
        assert "n1" in content
        assert "n2" in content
        # "imports" might be in the title attribute
        assert "imports" in content
