# Code City Payload Guardrail System

## Overview

The payload guardrail system protects Orchestr8 from runtime failures when rendering Code City visualizations for oversized repositories. Without guardrails, large payloads cause marimo output serialization failures, WebSocket errors, and UI instability.

## Architecture

### Location
- **Primary Guardrail**: `IP/plugins/06_maestro.py` (lines 1134-1212)
- **Streaming Control**: `IP/features/code_city/render.py` (lines 59-80)

### Core Flow

```
build_code_city() entry
    |
    v
1. Read ORCHESTR8_CODE_CITY_MAX_BYTES env (default: 9,000,000)
    |
    v
2. Render Code City at root
    |
    v
3. Measure payload size (_payload_size_bytes)
    |
    v
4. IF payload > max_bytes:
    |
    +-- YES --> Try IP/ subroot fallback
    |               |
    |               v
    |           Measure again
    |               |
    |               v
    |           IF still too large --> Show warning panel
    |               |
    |               v
    |           ELSE --> Render with IP/ subroot
    |
    v
5. Render output (or fallback panel)
```

## Size Measurement Logic

### Implementation (`06_maestro.py` lines 1155-1160)

```python
def _payload_size_bytes(city_result: Any) -> int:
    """Measure marimo Html payload size when available."""
    text = getattr(city_result, "text", None)
    if not isinstance(text, str):
        return 0
    return len(text.encode("utf-8"))
```

**Key Points**:
- Extracts `.text` attribute from marimo `Html` object
- Returns 0 if not string (safe default)
- Measures UTF-8 encoded bytes, not string length

### Why This Matters

Marimo serializes all output to JSON for WebSocket transmission. The payload includes:
- Full HTML content (iframe srcdoc)
- JavaScript dependencies
- Graph data (nodes/edges)
- Building data (if inline mode)

Large repositories generate payloads exceeding WebSocket frame limits and browser DOM constraints.

## Fallback Strategies

### Strategy 1: IP/ Subroot (Primary)

**Trigger**: Payload exceeds `max_payload_bytes` at repository root

**Logic**:
```python
ip_root = Path(root) / "IP"
if ip_root.is_dir() and str(ip_root) != str(root):
    result = create_code_city(str(ip_root), ...)
```

**Conditions**:
1. `IP/` subdirectory must exist
2. `IP/` path must differ from root (avoid infinite recursion)
3. Falls back to warning panel if still oversized

**Use Case**: Orchestr8 project itself is large, but `IP/` submodule is manageable.

### Strategy 2: Warning Panel (Final Fallback)

**Trigger**: Payload still exceeds limit after subroot attempt

**Output**: Styled void-center div with:
- Payload size (formatted with commas)
- Limit size
- Instructions to increase limits
- Environment variable commands

```html
<div class="void-center">
    <div class="void-placeholder" style="max-width: 760px; line-height: 1.6;">
        Code City payload exceeded safe render size
        (<code>{payload_size:,}</code> bytes; limit <code>{max_payload_bytes:,}</code>).
        <br><br>
        Set a narrower project root, or increase limits:
        <br>
        <code>export ORCHESTR8_CODE_CITY_MAX_BYTES={max_payload_bytes * 2}</code>
        <br>
        <code>export MARIMO_OUTPUT_MAX_BYTES={max_payload_bytes * 2}</code>
    </div>
</div>
```

### Strategy 3: Streaming (3D Buildings)

**Location**: `IP/features/code_city/render.py`

**Environment Variable**: `ORCHESTR8_CODE_CITY_STREAM_BPS`
- **Default**: 5,000,000 bytes/sec
- **Minimum**: 100,000 bytes/sec
- **Purpose**: Progressive client-side building generation

**Logic**:
```python
stream_bps_raw = os.getenv("ORCHESTR8_CODE_CITY_STREAM_BPS", "5000000").strip()
try:
    stream_bps = max(100_000, int(stream_bps_raw))
except ValueError:
    stream_bps = 5_000_000
```

When `ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA` is NOT set:
- 3D building data set to `"null"`
- Buildings generated client-side from graph nodes
- Streaming budget controls progressive loading

## Environment Variables

| Variable | Default | Min | Purpose |
|----------|---------|-----|---------|
| `ORCHESTR8_CODE_CITY_MAX_BYTES` | 9,000,000 | 1,000,000 | Max payload size before fallback |
| `ORCHESTR8_CODE_CITY_STREAM_BPS` | 5,000,000 | 100,000 | 3D building stream rate |
| `ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA` | false | - | Legacy full-inline mode |

### Configuration Safety

```python
max_payload_raw = os.getenv("ORCHESTR8_CODE_CITY_MAX_BYTES", "9000000").strip()
try:
    max_payload_bytes = max(1_000_000, int(max_payload_raw))
except ValueError:
    max_payload_bytes = 9_000_000
```

- Enforces 1MB minimum (prevents accidental zero/negative values)
- Falls back to 9MB on parse errors
- Logs all threshold breaches for observability

## Error Handling

### Layer 1: Payload Size Guard

```python
payload_size = _payload_size_bytes(result)
if payload_size > max_payload_bytes:
    # Attempt subroot fallback
```

### Layer 2: Subroot Retry

```python
payload_size = _payload_size_bytes(result)
if payload_size > max_payload_bytes:
    # Final fallback: warning panel
    return mo.Html(f"""...""")
```

### Layer 3: Exception Catching

```python
except Exception as e:
    log_action(f"Code City error: {str(e)}")
    return mo.Html(f"""
    <div class="void-center">
        <div class="void-placeholder" style="color: {BLUE_DOMINANT};">
            Error rendering Code City: {str(e)}
        </div>
    </div>
    """)
```

**Error Display**:
- Uses `BLUE_DOMINANT` color (#1fbdea) for error state
- Graceful degradation to placeholder message
- Errors logged via `log_action()` for diagnostics

### Layer 4: Health Watcher Protection

```python
try:
    health_watcher.start_watching()
except Exception as e:
    log_action(f"Health watcher start error: {e}")
```

- Health watcher failures don't crash Code City render
- Errors logged but render continues

## Observability

### Logging Points

1. **Subroot Attempt**:
   ```
   "Code City payload too large at root; retrying with IP/ subroot "
   f"({payload_size} bytes > {max_payload_bytes} bytes)."
   ```

2. **Final Threshold Breach**:
   ```
   "Code City payload exceeded guardrail "
   f"({payload_size} bytes > {max_payload_bytes} bytes)."
   ```

3. **Successful Render**:
   ```
   f"Code City rendered with {len(health_data)} health result(s)"
   ```

4. **Errors**:
   ```
   "Code City error: {str(e)}"
   "Health watcher start error: {e}"
   "Initial health check error: {he}"
   ```

## Tuning Recommendations

### For Large Monorepos

```bash
# Increase payload limit
export ORCHESTR8_CODE_CITY_MAX_BYTES=18000000

# Increase marimo output limit
export MARIMO_OUTPUT_MAX_BYTES=18000000
```

### For Slow Networks

```bash
# Reduce streaming rate for progressive loading
export ORCHESTR8_CODE_CITY_STREAM_BPS=1000000
```

### For Development/Debugging

```bash
# Enable legacy inline building data mode
export ORCHESTR8_CODE_CITY_INLINE_BUILDING_DATA=1
```

## Failure Modes

| Mode | Symptom | Guardrail Response |
|------|---------|-------------------|
| Oversized root payload | Blank Code City | Retry with IP/ subroot |
| Oversized subroot payload | Warning panel | Show size + tuning instructions |
| Invalid env value | Falls back to defaults | Continues with safe limits |
| Health watcher failure | No live updates | Logs error, render continues |
| Render exception | Error placeholder | Blue error message |

## Integration Notes

- Guardrail is invoked at render time, not build time
- Payload measurement happens AFTER `create_code_city()` completes
- The system is defensive: it catches failures and degrades gracefully
- No manual intervention required for typical oversized repo scenarios
