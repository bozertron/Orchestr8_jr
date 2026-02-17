# CODE CITY UI CONTRACT

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, IP/woven_maps.py, Observation #1464

## Purpose

Contract specification for Code City 3D visualization integration.

## Integration Points

### Primary Files

| File | Responsibility | Freeze Status |
|------|----------------|---------------|
| `IP/woven_maps.py` | Python backend, data preparation | UNLOCKED |
| `IP/static/woven_maps_3d.js` | WebGL/Three.js rendering | FROZEN |
| `IP/static/woven_maps_template.html` | iframe template | FROZEN |

### Render Path

```
orchestr8.py
  -> IP/plugins/06_maestro.py
    -> IP/woven_maps.py (build_code_city)
      -> IP/static/woven_maps_template.html
        -> IP/static/woven_maps_3d.js (client-side)
```

## Visual Contract

### Viewport

| Property | Value |
|----------|-------|
| Position | Main section (The Void) |
| Z-index | 100 (canvas layer) |
| Background | Transparent to --bg-obsidian |

### Building Representation

| Element | Visual | Semantic |
|---------|--------|----------|
| Height | Building elevation | Export count / complexity |
| Footprint | Base area | Lines of code |
| Color (Gold) | #D4AF37 | Working state |
| Color (Teal) | #00E5E5 | Needs attention |
| Color (Purple) | #9D4EDD | Agents active |

### Particle System

| Property | Value |
|----------|-------|
| Count | 12,000 particles |
| Size | 0.12 (attenuated) |
| Opacity | 0.8 |
| Initial Color | rgba(0, 0.8, 0.8, 1) |

### Emergence Sequence

| Phase | Duration | Behavior |
|-------|----------|----------|
| VOID | 0-1s | Dark, silent |
| AWAKENING | 1-10s | Particles stir, lights fade in |
| TUNING | 10-16s | Particle organization begins |
| COALESCING | 16-22s | Particles converge to building positions |
| EMERGENCE | 22-26s | Full city formation |
| TRANSITION | 26-28s | Color shift to gold |
| READY | 28-30s | UI layer appears |

## Data Contract

### Input Schema

```python
{
    "nodes": [
        {
            "id": str,           # File/module identifier
            "path": str,         # File path
            "exports": int,      # Export count -> height
            "loc": int,          # Lines of code -> footprint
            "state": str,        # "working" | "needs_attention" | "agents_active"
            "fiefdom": str       # Subsystem assignment
        }
    ],
    "edges": [
        {
            "source": str,       # Source node id
            "target": str,       # Target node id
            "type": str          # "import" | "export" | "internal"
        }
    ]
}
```

### Output Contract

The visualization must render without blocking the main thread:
- Stream budget: 5,000,000 bytes/sec (configurable)
- Max payload: 9,000,000 bytes before fallback
- Fallback: Compact warning panel

## Payload Guard

### Size Check

```python
MAX_PAYLOAD_BYTES = int(os.environ.get('ORCHESTR8_CODE_CITY_MAX_BYTES', 9_000_000))

payload_bytes = len(json.dumps(graph_data).encode('utf-8'))
if payload_bytes > MAX_PAYLOAD_BYTES:
    # Fallback to IP/ as root
    # If still oversized, render compact warning
```

### Streaming Mode

```python
STREAM_BPS = int(os.environ.get('ORCHESTR8_CODE_CITY_STREAM_BPS', 5_000_000))
INLINE_BUILDING_DATA = os.environ.get('ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA', '0') == '1'
```

## Event Contract

### Outbound Events (to marimo)

| Event | Payload | Consumer |
|-------|---------|----------|
| `city:node:selected` | `{node_id, path}` | Plugin handlers |
| `city:edge:hovered` | `{source, target}` | Tooltip display |
| `city:ready` | `{node_count, edge_count}` | Status updates |

### Inbound Events (from marimo)

| Event | Payload | Handler |
|-------|---------|---------|
| `city:filter:fiefdom` | `{fiefdom_id}` | Filter visibility |
| `city:highlight:state` | `{state}` | Highlight by state |
| `city:reset` | `{}` | Reset view |

## Performance Contract

| Metric | Threshold |
|--------|-----------|
| Initial render | < 2s |
| Frame rate | > 30fps |
| Memory (client) | < 500MB |
| Payload size | < 9MB |

## Fallback Behavior

| Condition | Fallback |
|-----------|----------|
| WebGPU unavailable | CPU canvas fallback |
| Payload oversized | Repo root -> IP/ -> Compact warning |
| WebGL error | Static placeholder |

## Change Protocol

Changes to this contract require:
1. Packet proposal with impact analysis
2. Visual regression test plan
3. Codex + Orchestr8_jr approval

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial contract | P07-A1 |
