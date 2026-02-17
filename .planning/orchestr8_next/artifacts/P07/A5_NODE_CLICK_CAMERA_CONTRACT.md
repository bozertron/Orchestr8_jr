# Code City Event Contract: Node Click + Camera State Handoff

**Contract Status:** LOCKED
**Date:** 2026-02-16
**Location:** `orchestr8_next/city/contracts.py`, `IP/plugins/06_maestro.py`

---

## Event Contract Schema

### Node Click Event (JS → Python)

```python
class NodeClickedEvent(BaseCityEvent):
    type: Literal["node_clicked"] = "node_clicked"
    node_id: str
    button: int = 0
```

### Camera Moved Event (JS → Python)

```python
class CameraMovedEvent(BaseCityEvent):
    type: Literal["camera_moved"] = "camera_moved"
    position: Coordinate
    rotation: Rotation
```

### Connection Request Event (JS → Python)

```python
class ConnectionRequestedEvent(BaseCityEvent):
    type: Literal["connect_request"] = "connect_request"
    source_id: str
    target_id: str
```

---

## Bridge Implementation

| Component | Location | Status |
|-----------|----------|--------|
| Node click handler | `IP/plugins/06_maestro.py:364` (`process_node_click`) | ✅ IMPLEMENTED |
| Schema validation | `orchestr8_next/city/contracts.py:66` (`NodeClickedEvent`) | ✅ LOCKED |
| Camera nav bridge | `IP/plugins/06_maestro.py:1011` (`on_node_click_bridge_change`) | ✅ IMPLEMENTED |
| Hidden bridge element | `IP/plugins/06_maestro.py:1082` (`node_click_bridge`) | ✅ IMPLEMENTED |

---

## Behavior Contract by Node Status

| Status | Action | Implementation |
|--------|--------|----------------|
| `broken` | Auto-generate ticket payload, show deploy panel | `IP/plugins/06_maestro.py:412` |
| `combat` | Show "Agent active" status message | `IP/plugins/06_maestro.py:407` |
| `working` | Show building info panel (read-only) | `IP/plugins/06_maestro.py:408` |

---

## Camera State Contract

| Field | Type | Description |
|-------|------|-------------|
| `position.x` | float | X coordinate |
| `position.y` | float | Y coordinate |
| `position.z` | float | Z coordinate |
| `rotation.x` | float | X rotation (radians) |
| `rotation.y` | float | Y rotation (radians) |
| `rotation.z` | float | Z rotation (radians) |

---

## Integration Targets

1. **Broken Node → Deploy Panel**: `06_maestro.py:412` triggers deploy panel with Carl context
2. **Node Click → Context Payload**: `IP/features/maestro/code_city_context.py` assembles handoff
3. **Camera → Navigation History**: Return stack maintained for dive/return navigation

---

## Contract Enforcement

Any changes to this contract must:
1. Update `orchestr8_next/city/contracts.py` schema
2. Update `IP/plugins/06_maestro.py` bridge handlers
3. Run acceptance test: click each node type and verify behavior
