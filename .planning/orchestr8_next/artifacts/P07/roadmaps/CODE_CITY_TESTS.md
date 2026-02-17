# Code City Test Suite Catalog

This document provides a comprehensive catalog of the Code City test suite, documenting all test files, patterns, and coverage areas for validation purposes.

## Overview

The Code City test suite is organized into three primary directories:

- `tests/city/` - Unit tests for core Code City components
- `tests/integration/` - Integration tests for service interoperability
- `tests/reliability/` - Reliability and stability tests for core systems

## Test Directory Structure

```
tests/
├── city/                          # Unit tests for Code City core
│   ├── test_binary_payload.py    # Binary payload chunking tests
│   ├── test_parity.py            # Widget initialization parity tests
│   └── test_wiring_view.py       # Wiring view generation tests
├── integration/                  # Integration tests
│   ├── test_command_surface.py  # CommandSurface + TemporalState integration
│   ├── test_temporal_state.py    # TemporalStateService comprehensive tests
│   ├── test_city_automation.py   # Automation queue and undo/redo tests
│   ├── test_agent_conversation.py # AgentConversationService tests
│   ├── test_city_tour_service.py # TourService lifecycle tests
│   ├── test_city_power_grid.py   # Power grid topology tests
│   ├── test_graphs.py            # Topology builder and heatmap tests
│   └── test_temporal_state.py    # Additional temporal state tests
└── reliability/                   # Reliability tests
    └── test_reliability.py       # Core state and bridge tests
```

## Test Files Analysis

### tests/city/ - Unit Tests

#### test_binary_payload.py

Tests the `CodeCityWidget` binary payload chunking mechanism for handling large payloads exceeding the 4MB limit.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_send_small_payload` | Verifies single-chunk transmission for payloads under 4MB |
| `test_send_large_payload_chunking` | Verifies multi-chunk transmission and reassembly for payloads > 4MB |
| `test_malformed_chunk_handling` | Validates metadata consistency for chunked data |

**Key Testing Aspects:**
- Chunk metadata validation (payload_id, chunk_index, chunk_total)
- Binary data encoding/decoding (UTF-8)
- Chunk reassembly verification
- Payload ID consistency across chunks

**Dependencies:**
- `orchestr8_next.city.widget.CodeCityWidget`
- `traitlets`
- `json`
- `uuid`

#### test_parity.py

Tests the parity between widget initialization and wiring view generation to ensure consistent data handling.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_parity_widget_initialization` | Verifies widget accepts standard contract data |
| `test_parity_iframe_serialization` | Validates iframe JSON dump/load path |
| `test_parity_wiring_generation` | Verifies wiring view generates correctly with same data |

**Key Testing Aspects:**
- Widget nodes and connections initialization
- JSON serialization/deserialization round-trip
- HTML file generation for wiring views
- Content parity between widget and wiring representations

**Dependencies:**
- `orchestr8_next.city.widget.CodeCityWidget`
- `orchestr8_next.city.wiring.generate_wiring_view`
- `json`
- `os`

#### test_wiring_view.py

Tests the `generate_wiring_view` function for creating HTML-based wiring visualizations.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_wiring_view_generates_file` | Verifies HTML file creation |
| `test_wiring_view_connections` | Validates connection rendering in output |

**Key Testing Aspects:**
- File existence validation
- Node label inclusion in output
- Connection type rendering (vis.js format)
- Edge data serialization

**Dependencies:**
- `orchestr8_next.city.wiring.generate_wiring_view`
- `unittest.mock`

### tests/integration/ - Integration Tests

#### test_command_surface.py

Tests the integration between `CommandSurface` and `TemporalStateService`.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_command_surface_temporal_integration` | Verifies CommandSurface can query temporal state and use time_machine |

**Key Testing Aspects:**
- Command registration with temporal service
- Query history command execution
- Snapshot/time_machine retrieval
- Service interoperability

**Dependencies:**
- `orchestr8_next.city.temporal_state.TemporalStateService`
- `orchestr8_next.city.command_surface.CommandSurface`

#### test_temporal_state.py

Comprehensive tests for the `TemporalStateService` - the central state management system for Code City.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_epoch_lifecycle` | Verifies Epoch management (MSL-MOD-03) |
| `test_quantum_stream` | Validates quantum event recording |
| `test_snapshot_creation` | Tests snapshot creation and retrieval logic |
| `test_persistence` | Verifies save/load to disk |
| `test_tour_integration` | Validates TourService quantum event recording |
| `test_conversation_integration` | Validates AgentConversationService quantum event recording |
| `test_quantum_increment` | Verifies MSL-04 3.1 atomic increment |
| `test_historical_snapshot_retrieval` | Verifies MSL-04 3.2 immutable access |
| `test_full_city_cycle` | Verifies MSL-04 4 sync loop - service interoperability |
| `test_bucketed_activity` | Verifies MSL-04 3.1 / P07-C5-01 activity bucketization |
| `test_search_history` | Verifies P07-C5-02 history search/filtering |

**Key Testing Aspects:**
- Epoch start/end lifecycle
- Quantum event recording and retrieval
- Snapshot creation with artifact references
- Persistence export/import
- Service integration (Tour, Conversation)
- Atomic quantum increment
- Historical snapshot retrieval by quantum ID
- Full city cycle - multi-service interoperability
- Activity bucketing for time windows
- History search with type and query filters

**Dependencies:**
- `orchestr8_next.city.temporal_state.TemporalStateService`
- `orchestr8_next.city.temporal_state.Epoch`
- `orchestr8_next.city.temporal_state.Snapshot`
- `orchestr8_next.city.tour_service.TourService`
- `orchestr8_next.city.agent_conversation.AgentConversationService`
- `time`

#### test_city_automation.py

Tests automation services for task queuing and undo/redo functionality.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_automation_queue_flow` | Verifies QueueService (C2-01) logic |
| `test_undo_redo_service` | Verifies UndoRedoService (C2-01) logic |

**Key Testing Aspects:**
- Task enqueuing with ID generation
- Task processing workflow
- Pending task count management
- Empty queue handling
- State capture for undo
- Undo/redo pointer navigation
- Boundary conditions (undo at start, redo at end)

**Dependencies:**
- `orchestr8_next.city.automation.QueueService`
- `orchestr8_next.city.automation.UndoRedoService`
- `orchestr8_next.city.automation.AutomationTask`

#### test_agent_conversation.py

Tests the `AgentConversationService` for agent-to-user messaging and tool execution tracking.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_streaming_message_lifecycle` | Verifies C3-02 conversation logic |
| `test_empty_state` | Validates empty service state |

**Key Testing Aspects:**
- User message posting
- Agent response posting
- Tool execution (thinking) lifecycle
- Tool log accumulation
- Active thinking task tracking
- Completion status management
- Message history retrieval

**Dependencies:**
- `orchestr8_next.city.agent_conversation.AgentConversationService`
- `orchestr8_next.city.agent_conversation.MessageType`

#### test_city_tour_service.py

Tests the `TourService` for guided user tours through the Code City interface.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_tour_lifecycle` | Verifies TourService (C3-01) complete flow |
| `test_tour_navigation` | Validates prev/next navigation logic |

**Key Testing Aspects:**
- Tour step loading
- Tour start/finish state management
- Next step progression
- Previous step navigation
- Boundary handling (no previous at start, no next at end)
- Active/inactive state transitions

**Dependencies:**
- `orchestr8_next.city.tour_service.TourService`
- `orchestr8_next.city.tour_service.TourStep`

#### test_city_power_grid.py

Tests the `ProcessService` and `GridEntity` for system process topology visualization.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_process_service_topology` | Verifies Power Grid (C2-02) topology builder |
| `test_kill_process` | Validates kill switch logic |

**Key Testing Aspects:**
- Process hierarchy building from parent-child relationships
- Root process identification
- Nested child traversal
- Orphan process handling
- CPU usage mapping
- Process termination
- Non-existent process handling

**Dependencies:**
- `orchestr8_next.city.power_grid.ProcessService`
- `orchestr8_next.city.power_grid.GridEntity`

#### test_graphs.py

Tests topology building and heatmap time bucketing services.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_c1_01_topology_builder` | Verifies clean room topology generation |
| `test_c1_02_heatmap_bucketing` | Verifies clean room time bucketing logic |

**Key Testing Aspects:**
- Filesystem scanning and node generation
- Connection building from directory structure
- Event time bucketing by interval
- Bucket count verification
- Heatmap intensity normalization
- Peak/normal intensity calculation

**Dependencies:**
- `orchestr8_next.city.topology.CityTopologyBuilder`
- `orchestr8_next.city.heatmap.TimeService`
- `os`
- `time`

### tests/reliability/ - Reliability Tests

#### test_reliability.py

Tests core system reliability including state management and event bridge failure isolation.

**Test Functions:**

| Function | Purpose |
|----------|---------|
| `test_system_startup_reliability` | Verifies clean initialization of core state components |
| `test_core_control_integrity` | Verifies basic action dispatch doesn't destabilize store |
| `test_adapter_failure_isolation_bridge` | Verifies CityBridge isolates handler failures |

**Key Testing Aspects:**
- State.initial() factory method
- Store creation with reducer
- State consistency verification
- Action dispatch and state mutation
- Bridge handler failure isolation
- Event dispatch without caller exceptions

**Dependencies:**
- `orchestr8_next.shell.store.Store`
- `orchestr8_next.shell.contracts.State`
- `orchestr8_next.shell.contracts.ActionType`
- `orchestr8_next.shell.reducer.root_reducer`
- `orchestr8_next.shell.actions.UIAction`
- `orchestr8_next.city.bridge.CityBridge`
- `orchestr8_next.city.contracts.NodeClickedEvent`
- `unittest.mock.MagicMock`

## Test Patterns Used

### Framework and Fixtures

The test suite uses **pytest** as the primary testing framework with the following common patterns:

- **tmp_path fixture**: Used for creating temporary files and directories for tests that involve file I/O
- **unittest.mock**: Used for mocking dependencies and simulating edge cases
- **Traitlets observation**: Used in `test_binary_payload.py` to capture trait change events

### Testing Approaches

1. **Unit Testing**: Individual component testing with mock dependencies
2. **Integration Testing**: Service interoperability testing with real service instances
3. **State-Based Testing**: Testing state transitions and lifecycle methods
4. **File-Based Testing**: Testing file generation and content validation
5. **Contract Testing**: Validating data structures match expected schemas

### Common Test Patterns

```python
# State initialization pattern
service = ServiceClass()
result = service.method(input)
assert expected_condition

# File generation pattern
output_file = tmp_path / "filename.html"
result = generate_function(data, filename=str(output_file))
assert os.path.exists(result)
with open(result) as f:
    content = f.read()
    assert "expected_content" in content

# Lifecycle pattern
service.start()
assert service.is_active()
service.stop()
assert not service.is_active()

# Integration pattern
service_a = ServiceA()
service_b = ServiceB()
service_a.register_dependency(service_b)
```

## Coverage Areas

### Core Components Covered

| Component | Coverage |
|-----------|----------|
| CodeCityWidget | Binary payload chunking, traitlets integration |
| Wiring View | HTML generation, connection rendering |
| TemporalStateService | Epochs, quantum events, snapshots, persistence |
| CommandSurface | Command registration, temporal query integration |
| QueueService | Task enqueuing, processing workflow |
| UndoRedoService | State capture, undo/redo navigation |
| AgentConversationService | Message lifecycle, tool execution tracking |
| TourService | Step navigation, state management |
| ProcessService | Topology building, process hierarchy |
| CityTopologyBuilder | Filesystem scanning, node generation |
| TimeService | Event bucketing, intensity calculation |
| Store | State management, action dispatch |
| CityBridge | Event handling, failure isolation |

### MSL Requirements Coverage

| MSL Requirement | Test Coverage |
|-----------------|---------------|
| MSL-MOD-03 | Epoch lifecycle (test_epoch_lifecycle) |
| MSL-04 3.1 | Quantum atomic increment (test_quantum_increment) |
| MSL-04 3.2 | Immutable snapshot access (test_historical_snapshot_retrieval) |
| MSL-04 4 | Sync loop / service interoperability (test_full_city_cycle) |
| P07-C5-01 | Activity bucketization (test_bucketed_activity) |
| P07-C5-02 | History search/filtering (test_search_history) |
| C2-01 | Queue and Undo/Redo (test_automation_queue_flow, test_undo_redo_service) |
| C2-02 | Power grid topology (test_process_service_topology) |
| C3-01 | Tour service (test_tour_lifecycle, test_tour_navigation) |
| C3-02 | Conversation service (test_streaming_message_lifecycle) |

### Gap Analysis

**Areas with Test Coverage:**
- Binary payload handling for large data
- Wiring view generation
- Temporal state management
- Automation services
- Agent conversation tracking
- Tour navigation
- Process topology
- Topology building
- Heatmap bucketing
- Core state management
- Event bridge reliability

**Potential Areas for Additional Testing:**
- Frontend JavaScript rendering tests
- End-to-end user workflow tests
- Performance/load testing for large codebases
- Browser compatibility testing
- WebSocket communication testing
- Multi-user concurrent session testing
- Error recovery and fallback scenarios

## Running the Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Directory

```bash
pytest tests/city/ -v
pytest tests/integration/ -v
pytest tests/reliability/ -v
```

### Run Specific Test File

```bash
pytest tests/city/test_binary_payload.py -v
```

### Run Tests Matching Pattern

```bash
pytest tests/ -k "temporal" -v
```

## Test Execution Requirements

### Python Dependencies

- pytest
- traitlets
- anywidget
- json (standard library)
- os (standard library)
- time (standard library)
- unittest.mock (standard library)

### Module Dependencies

The tests require the following orchestr8_next modules:

- `orchestr8_next.city.widget`
- `orchestr8_next.city.wiring`
- `orchestr8_next.city.temporal_state`
- `orchestr8_next.city.command_surface`
- `orchestr8_next.city.automation`
- `orchestr8_next.city.agent_conversation`
- `orchestr8_next.city.tour_service`
- `orchestr8_next.city.power_grid`
- `orchestr8_next.city.topology`
- `orchestr8_next.city.heatmap`
- `orchestr8_next.city.bridge`
- `orchestr8_next.city.contracts`
- `orchestr8_next.shell.store`
- `orchestr8_next.shell.reducer`
- `orchestr8_next.shell.contracts`
- `orchestr8_next.shell.actions`

## Summary

The Code City test suite provides comprehensive validation across multiple layers:

- **3 unit tests** in `tests/city/` covering core widget and wiring functionality
- **8 integration tests** in `tests/integration/` covering service interoperability
- **1 reliability test** in `tests/reliability/` covering core system stability

Total: **12 test files** with **30+ test functions** providing broad coverage of Code City functionality with specific focus on temporal state management, automation services, and system reliability.
