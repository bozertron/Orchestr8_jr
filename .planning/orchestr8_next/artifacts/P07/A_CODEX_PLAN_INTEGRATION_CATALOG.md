# A_CODEX_PLAN Integration Catalog

**Target:** `/home/bozertron/a_codex_plan`
**Generated:** 2026-02-16
**Purpose:** Comprehensive catalog of Orchestr8 plugins and P2P systems for a_codex_plan integration

---

## PART 1: MARIMO PLUGIN SYSTEM

### Architecture Overview

```
orchestr8.py (entry point)
    └── IP/plugins/__init__.py (plugin loader)
            ├── 00_welcome.py
            ├── 01_generator.py
            ├── 02_explorer.py
            ├── 03_gatekeeper.py
            ├── 04_connie_ui.py
            ├── 05_universal_bridge.py
            ├── 06_maestro.py (THE VOID)
            ├── 07_settings.py
            └── 08_director.py
```

### Plugin Contract (MANDATORY)

Every plugin MUST export:

```python
PLUGIN_NAME: str = "Display Name"
PLUGIN_ORDER: int = N  # Lower = first tab

def render(STATE_MANAGERS: dict) -> mo.UIElement:
    # STATE_MANAGERS keys: "root", "files", "selected", "logs", "health"
    get_root, set_root = STATE_MANAGERS["root"]
    # ... implementation
    return mo.vstack([...])
```

### State Management Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `mo.state(initial)` | Historical state, sync across elements | `get_phase, set_phase = mo.state(1)` |
| `STATE_MANAGERS` | Shared state across plugins | `get_root, set_root = STATE_MANAGERS["root"]` |
| Derived from UI | Compute from element value | `value = my_button.value` |

**CRITICAL: Do NOT store UIElement in mo.state - causes unpredictable behavior**

---

## PART 2: PLUGIN CATALOG

### 00_welcome.py - Welcome Tab
- **Purpose:** Getting started guide
- **Complexity:** Simple
- **State:** ACCESSES root, logs
- **Dependencies:** marimo
- **Integration:** None

### 01_generator.py - 7-Phase Project Wizard
- **Purpose:** BUILD_SPEC.json generation
- **Complexity:** Medium
- **State:** `phase`, `spec`, `locked` (mo.state)
- **UI:** text, text_area, dropdown, button, md, vstack, hstack
- **Integration:** None

### 02_explorer.py - File Explorer
- **Purpose:** Project file browsing + Carl deep scan
- **Complexity:** Medium
- **State:** `scan_result`, `is_scanning` (mo.state)
- **Integration:** CarlContextualizer.run_deep_scan()

### 03_gatekeeper.py - Louis File Protection
- **Purpose:** File lock/unlock UI
- **Complexity:** Medium
- **State:** `new_path`, `refresh_trigger`, `selected_files` (mo.state)
- **Integration:** LouisWarden, LouisConfig

### 04_connie_ui.py - Database Conversion
- **Purpose:** SQLite export tools
- **Complexity:** Medium
- **State:** 6 mo.state variables for DB/table/format selection
- **Integration:** ConversionEngine, pandas

### 05_universal_bridge.py - Tool Registry
- **Purpose:** Dynamic TypeScript tool execution
- **Complexity:** High
- **State:** `tool_states`, `scan_errors`, `is_scanning`, `selected_target`
- **Integration:** Dynamic registry scanning, output_renderer

### 06_maestro.py - THE VOID (MOST COMPLEX)
- **Purpose:** Central command, Code City, chat
- **Complexity:** VERY HIGH (29 mo.state variables!)
- **Key Features:**
  - Code City 3D via iframe
  - JS->Python bridge (node_click, connection_action, camera_nav)
  - Contract validation (CodeCityNodeEvent)
  - HealthWatcher, CombatTracker, TerminalSpawner
  - CSS injection, font profile injection
- **Integration:** ALL THE THINGS

### 07_settings.py - Configuration Panel
- **Purpose:** TOML config management
- **Complexity:** Medium
- **State:** `active_tab`, `modified`
- **Integration:** SettingsManager, pyproject_orchestr8_settings.toml

### 08_director.py - LLM Monitoring
- **Purpose:** Director agent integration
- **Complexity:** High
- **State:** `monitoring`, `show_alerts`
- **Integration:** 888/director.adapter (PyO3), background thread

---

## PART 3: MARIMO INTEGRATION PATTERNS

### JavaScript Bridge Pattern (CRITICAL)

Used in 06_maestro.py for iframe communication:

```python
# Python side
get_payload, set_payload = mo.state("")
bridge = mo.ui.text(value=get_payload(), on_change=on_change_handler)

# JavaScript (in mo.Html)
<script>
window.parent.postMessage({node: clickedData}, '*');
// Or write to hidden input
document.getElementById('bridge-element-id').value = JSON.stringify(data);
document.getElementById('bridge-element-id').dispatchEvent(new Event('input'));
</script>

# Hidden wrapper
mo.Html(f"<div style='display:none'>{bridge}</div>")
```

### Path Resolution Pattern

06_maestro.py lines 44-64:

```python
import sys
from pathlib import Path

_THIS_FILE = Path(__file__).resolve()
_PROJECT_ROOT = _THIS_FILE.parent.parent.parent

if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import IP  # Fails loudly if not found
```

### CSS Injection Pattern

```python
from IP.features.maestro import load_orchestr8_css

def render(STATE_MANAGERS):
    css = mo.Html(f"<style>{load_orchestr8_css()}</style>")
    return mo.vstack([css, ...])
```

### Button Callback Pattern (MANDATORY)

```python
# CORRECT - use on_click
mo.ui.button(label="Submit", on_click=lambda _: handle_submit())

# WRONG - on_change can fail in some marimo versions
mo.ui.button(label="Submit", on_change=lambda _,: handle_submit())
```

---

## PART 4: P2P SYSTEMS CATALOG

### Rust P2P (one integration at a time/p2p/)

**Architecture:**
```
P2PNetwork (main orchestrator)
├── PeerManager (connections)
├── Discovery (mDNS + Kademlia DHT)
├── P2PTransport (TCP/WebSocket + Noise + Yamux)
├── WebRtcService (video/audio)
├── MessageService (encrypted messaging)
└── P2PService (lifecycle coordinator)
```

**Key Types:**
- `PeerId` - Unique peer identifier
- `Multiaddr` - Network addresses (`/ip4/.../tcp/.../p2p/...`)
- `Keypair` - Ed25519 identity
- `NetworkConfig` - All configuration

**Discovery:**
- mDNS: Local network peer discovery
- Kademlia: DHT-based distributed discovery

**Message Pipeline:**
```
sign (Ed25519) -> encrypt (ChaCha20-Poly1305) -> route -> persist
```

### Python P2P Adapter (one integration at a time/888/comms/adapter.py)

**Public API:**
```python
# Session management
create_session(peer_id?, storage_path?) -> {success, session_id, peer_id}
get_network_stats(session_id) -> {connected_peers, bytes_sent, ...}

# Contacts
list_contacts(session_id) -> {contacts: [...]}
add_contact(session_id, name, peer_id, email?, notes?) -> {contact_id}
remove_contact(session_id, contact_id) -> {success}

# Messaging
send_message(session_id, recipient_peer_id, content, type?, attachments?) -> {message_id}
get_messages(session_id, limit?, offset?) -> {messages: [...]}
get_conversation(session_id, peer_id, limit?) -> {messages: [...]}

# WebRTC
start_webrtc_call(session_id, peer_id, video?, audio?) -> {call_id}
end_webrtc_call(session_id, call_id) -> {duration_seconds}
get_active_calls(session_id) -> {calls: [...]}
```

**Global State:**
- `_p2p_sessions`: Active sessions
- `_contacts`: Contact list
- `_messages`: Messages by conversation
- `_active_calls`: Active WebRTC calls

---

## PART 5: ALIGNMENT PATTERNS FOR A_CODEX_PLAN

### Integration Checklist

| Item | Priority | Pattern |
|------|----------|---------|
| IP package path resolution | MANDATORY | Use 06_maestro.py lines 44-64 pattern |
| Plugin exports | MANDATORY | PLUGIN_NAME, PLUGIN_ORDER, render() |
| State management | MANDATORY | mo.state for local, STATE_MANAGERS for shared |
| Button callbacks | MANDATORY | Use on_click, NOT on_change |
| JS bridges | CRITICAL | Hidden input + postMessage pattern |
| CSS injection | REQUIRED | load_orchestr8_css() or mo.Html |
| Error handling | REQUIRED | All P2P calls return {success, ...} format |
| Timestamps | REQUIRED | Unix milliseconds: int(time.time() * 1000) |

### Common Pitfalls (AVOID THESE)

1. **Duplicate variable names across cells** - Marimo namespace is global
2. **IP import failure** - Ensure sys.path manipulation at module top
3. **UIElement in mo.state** - Causes unpredictable behavior
4. **on_change on buttons** - Use on_click instead
5. **Missing payload guards** - Large outputs crash marimo (see ORCHESTR8_CODE_CITY_MAX_BYTES)
6. **WebSocket errors** - Usually secondary to compile violations

### libp2p Version Requirement

```
libp2p 0.52+ required
Features: tcp, websocket, noise, yamux, kademlia, mdns
```

---

## PART 6: CATALOG FILE LOCATIONS

| Catalog | Path |
|---------|------|
| Marimo Plugins | `.planning/orchestr8_next/artifacts/P07/PLUGIN_CATALOG.json` |
| Rust P2P | `.planning/orchestr8_next/artifacts/P07/RUST_P2P_CATALOG.json` |
| Python P2P Adapter | `.planning/orchestr8_next/artifacts/P07/PYTHON_P2P_CATALOG.json` |
| **This Document** | `.planning/orchestr8_next/artifacts/P07/A_CODEX_PLAN_INTEGRATION_CATALOG.md` |

---

## STRATEGIC NOTES FOR A_CODEX_PLAN

1. **Plugin hierarchy is SENSITIVE** - Follow the exact contract in PART 1
2. **06_maestro.py is the reference implementation** - Study it for all patterns
3. **P2P adapter uses Python primitives** - Rust bindings not yet compiled (PyO3 pending)
4. **Start with simple plugins** - 00_welcome then 01_generator before attempting Maestro
5. **Test JS bridges in isolation** - Use the hidden input pattern demonstrated in 06_maestro
