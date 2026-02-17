import pytest
from orchestr8_next.city.power_grid import ProcessService, GridEntity

def test_process_service_topology():
    """Verify Power Grid (C2-02) topology builder."""
    service = ProcessService()
    
    # Mock Data
    processes = [
        {"pid": 1, "name": "init", "cpu": 0.1},
        {"pid": 100, "ppid": 1, "name": "browser", "cpu": 5.0},
        {"pid": 101, "ppid": 100, "name": "tab-1", "cpu": 2.0},
        {"pid": 200, "ppid": 9999, "name": "orphan", "cpu": 0.0} # Orphan
    ]
    
    roots = service.build_grid_topology(processes)
    
    # Verify Roots
    assert len(roots) == 2 # Init (1) and Orphan (200)
    
    # Verify Hierarchy
    init_node = next(n for n in roots if n.pid == 1)
    assert len(init_node.children) == 1 # Browser
    assert init_node.children[0].pid == 100
    assert init_node.children[0].children[0].pid == 101 # Tab-1
    
    # Verify Data Mapping
    orphan = next(n for n in roots if n.pid == 200)
    assert orphan.name == "orphan"
    assert orphan.cpu_usage == 0.0

def test_kill_process():
    """Verify kill switch logic."""
    service = ProcessService()
    
    # Populate mock state directly
    service._mock_processes[123] = GridEntity(id="123", pid=123, name="bad-proc", children=[])
    
    assert service.kill_process_entity(123) is True
    assert 123 not in service._mock_processes
    
    assert service.kill_process_entity(999) is False
