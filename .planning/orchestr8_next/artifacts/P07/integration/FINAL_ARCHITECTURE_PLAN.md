# FINAL ARCHITECTURE PLAN
**Project:** orchestr8_next  
**Generated:** 2026-02-16  
**Status:** EXECUTION-READY  
**Canonical Source:** SOT/VISUAL_TOKEN_LOCK.md, ARCHITECTURE_BLUEPRINT.md

---

## EXECUTIVE SUMMARY

This document synthesizes findings from 5 parallel research agents and addresses gaps identified in ARCHITECTURE_SYNTHESIS_FEEDBACK.md to produce a single, actionable architecture plan ready for execution.

**Key Decision:** orchestr8_next adopts a **layered architecture** (L1-L5) with explicit boundaries, feature-flag-driven migration, and contract testing between layers.

**Critical Path:**
1. Establish Marimo-compliant module structure (R-1)
2. Integrate visual tokens as L1 presentation concern (R-2)
3. Formalize static asset handling (R-3)
4. Execute phased migration with rollback gates (R-4)
5. Validate all contracts with automated testing (R-5)

---

## 1. CANONICAL STRUCTURE

### 1.1 Physical Directory Layout

```
orchestr8_next/
├── orchestr8.py                    ← ENTRY POINT (CANNOT RELOCATE)
├── IP/
│   ├── plugins/
│   │   ├── 06_maestro.py          ← MAIN RENDER (CANNOT RELOCATE)
│   │   └── 07_settings.py
│   ├── styles/
│   │   ├── orchestr8.css          ← VISUAL TOKENS LIVE HERE
│   │   ├── font_profiles.py       ← FONT INJECTION
│   │   └── font_injection.py
│   ├── static/
│   │   ├── woven_maps_3d.js       ← THREE.JS RENDERER (CANNOT RELOCATE)
│   │   ├── woven_maps_template.html
│   │   └── shaders/
│   │       ├── barradeau.frag
│   │       └── barradeau.vert
│   ├── features/
│   │   ├── code_city/
│   │   │   ├── graph_builder.py
│   │   │   └── render.py
│   │   └── maestro/
│   │       └── views/
│   ├── contracts/
│   │   └── *.py                   ← LAYER CONTRACTS
│   └── [legacy modules]
├── Font/                           ← FONT ASSETS
│   ├── CalSans-SemiBold.woff
│   ├── mini_pixel-7.ttf
│   ├── HardCompn.fon
│   └── HardCompn.ttf
└── app/                            ← NEW MODULE STRUCTURE
    ├── __init__.py
    ├── app.py                      ← Marimo app entry
    ├── modules/
    │   ├── __init__.py
    │   ├── _state.py               ← All mo.state() definitions
    │   ├── _services.py            ← Service instantiation
    │   ├── _handlers.py            ← Event handlers
    │   ├── header.py
    │   ├── void.py
    │   └── footer.py
    └── lib/
        ├── __init__.py
        ├── health/
        ├── combat/
        ├── code_city/
        └── contracts/
```

### 1.2 Immutable Paths (CANNOT CHANGE)

| File | Reason |
|------|--------|
| `orchestr8.py` | Marimo entry point reference |
| `IP/plugins/06_maestro.py` | UI contract authority |
| `IP/woven_maps.py` | Data structure schema |
| `IP/static/woven_maps_3d.js` | Client API contract |
| `IP/contracts/*.py` | Cross-lane agreements |
| `IP/styles/orchestr8.css` | Visual token lock |

### 1.3 Mutable Paths

| File | Can Modify | Notes |
|------|------------|-------|
| `app/modules/_state.py` | YES | Centralize all mo.state() |
| `app/modules/_services.py` | YES | Service instantiation |
| `app/modules/_handlers.py` | YES | Event handlers |
| `Font/*` | YES | Add/remove fonts |

---

## 2. MARIMO-SPECIFIC PATTERNS (R-1)

### 2.1 Core Marimo Principles

| Principle | Implementation |
|-----------|----------------|
| **Reactive execution** | Run cell → marimo auto-runs dependent cells |
| **No hidden state** | Variables cleaned when cells deleted |
| **Execution order** | Determined by variable references, NOT file position |
| **UI globals** | All `mo.ui.*` elements MUST be global variables |

### 2.2 State Management Pattern

```python
# app/modules/_state.py - ALL state definitions must be here

import marimo as mo

# Global state definitions (module-level REQUIRED)
_root_state, _set_root = mo.state("/path/to/project")
_maestro_state, _set_maestro = mo.state("OFF")
_combat_state, _set_combat = mo.state([])

# Selector functions for derived state
def get_maestro_state() -> str:
    return _maestro_state()

def set_maestro_state(state: str) -> None:
    _set_maestro(state)
```

**CRITICAL:** State must be module-level. Function-scoped `mo.state()` will NOT persist.

### 2.3 UI Element Pattern

```python
# app/modules/header.py

import marimo as mo

# Global variable REQUIRED for tracking
toggle_orchestr8_btn = mo.ui.button(
    on_click=handle_toggle_orchestr8,
    label="orchestr8"
)

# NOT this (won't track):
# _toggle = mo.ui.button(...)  # Leading underscore = ignored
```

### 2.4 Handler Pattern

```python
# app/modules/_handlers.py

# Module-level function REQUIRED
def handle_toggle_orchestr8() -> None:
    current = get_maestro_state()
    states = ["ON", "OFF", "OBSERVE"]
    idx = states.index(current) if current in states else 0
    next_state = states[(idx + 1) % len(states)]
    set_maestro_state(next_state)

# Button uses on_click (NOT on_change)
toggle_btn = mo.ui.button(on_click=handle_toggle_orchestr8)
```

### 2.5 Cell Organization Pattern

```python
# orchestr8.py - Main entry

import marimo as mo

app = marimo.App(width="full")

# CELL 1: Imports (run once)
@app.cell
def import_modules():
    from app.modules import _state, _services, _handlers
    from app.modules import header, void, footer
    return

# CELL 2: State initialization (run once)
@app.cell
def init_state(import_modules):
    # State already initialized in _state.py
    return

# CELL 3: Services (run once)
@app.cell  
def init_services(init_state):
    from app.modules import _services
    return _services.get_services()

# CELL 4: UI output (reactive to state)
@app.cell
def render_header(init_services):
    from app.modules import header
    return header.render()
```

---

## 3. VISUAL TOKEN INTEGRATION (R-2)

### 3.1 Token Flow Architecture

```
SOT/VISUAL_TOKEN_LOCK.md (CANONICAL)
        ↓
    Parse tokens
        ↓
IP/styles/orchestr8.css ← CSS variables
IP/styles/font_profiles.py ← Font injection
        ↓
IP/static/woven_maps_3d.js ← Three.js colors
        ↓
    Runtime rendering
```

### 3.2 Color Token Definitions

| Token | Hex | Location | Usage |
|-------|-----|----------|-------|
| `--bg-obsidian` | #050505 | orchestr8.css:9 | Background base |
| `--gold-dark` | #C5A028 | orchestr8.css:10 | Primary accent |
| `--gold-light` | #F4C430 | orchestr8.css:11 | Highlight |
| `--teal` | #00E5E5 | orchestr8.css:12 | Secondary accent |
| `--text-grey` | #CCC | orchestr8.css:13 | Standard text |
| `--state-working` | #D4AF37 | orchestr8.css:27 | Gold - operational |
| `--state-broken` | #1fbdea | orchestr8.css:28 | Blue - needs attention |
| `--state-combat` | #9D4EDD | orchestr8.css:29 | Purple - agents active |

### 3.3 Typography Token Definitions

| Token | Value | Location |
|-------|-------|----------|
| `--font-header` | 'Marcellus SC', serif | orchestr8.css:62 |
| `--font-ui` | 'Poiret One', cursive | orchestr8.css:63 |
| `--font-data` | 'VT323', monospace | orchestr8.css:64 |

### 3.4 Dimension Token Definitions

| Token | Value | Location |
|-------|-------|----------|
| `--header-height` | 80px | orchestr8.css:1689 |
| `--top-btn-height` | 50px | orchestr8.css:1690 |
| `--top-btn-min-width` | 160px | orchestr8.css:1691 |
| `--btn-mini-height` | 22px | orchestr8.css:1692 |
| `--btn-mini-min-width` | 60px | orchestr8.css:1693 |
| `--btn-maestro-height` | 36px | orchestr8.css:1694 |

### 3.5 Three.js Color Mapping

The `woven_maps_3d.js` must map JavaScript colors to CSS tokens:

```javascript
// IP/static/woven_maps_3d.js - Required color mappings

const TOKEN_COLORS = {
    // Map CSS tokens to Three.js colors
    'state-working': 0xD4AF37,  // Gold
    'state-broken': 0x1FBD3A,   // Blue  
    'state-combat': 0x9D4EDD,   // Purple
    'bg-obsidian': 0x050505,    // Background
    'gold-accent': 0xC5A028,    // Borders
    'teal-accent': 0x00E5E0     // Highlights
};
```

### 3.6 Token Verification Gate

```python
# tests/visual/test_tokens.py

def test_css_tokens_match_lock():
    """Verify orchestr8.css tokens match VISUAL_TOKEN_LOCK.md"""
    lock = load_visual_token_lock()  # Parse SOT/VISUAL_TOKEN_LOCK.md
    css = load_css_variables("IP/styles/orchestr8.css")
    
    for token, expected_hex in lock.color_tokens.items():
        actual_hex = css.get(token)
        assert actual_hex == expected_hex, f"Token {token} drift: {actual_hex} != {expected_hex}"
```

---

## 4. STATIC ASSET HANDLING (R-3)

### 4.1 Current Asset Locations

| Asset Type | Current Location | Status |
|------------|------------------|--------|
| CSS | `IP/styles/orchestr8.css` | ✅ Active |
| JavaScript | `IP/static/woven_maps_3d.js` | ✅ Active |
| HTML Template | `IP/static/woven_maps_template.html` | ✅ Active |
| Shaders | `IP/static/shaders/*.frag/*.vert` | ✅ Active |
| Fonts | `Font/*.ttf/*.woff` | ✅ Active |

### 4.2 Recommended Asset Structure

```
IP/static/
├── woven_maps_3d.js           ← Main Three.js renderer
├── woven_maps_template.html   ← Iframe template
├── shaders/
│   ├── barradeau.frag        ← Fragment shader
│   └── barradeau.vert        ← Vertex shader
└── [future: additional renderers]

Font/
├── CalSans-SemiBold.woff      ← UI font
├── HardCompn.ttf              ← Display font
└── mini_pixel-7.ttf           ← Data font
```

### 4.3 Asset Loading Pattern

```python
# IP/plugins/06_maestro.py

def load_static_assets():
    """Load CSS and JS assets in correct order."""
    
    # 1. Load CSS (visual tokens first)
    css = Path("IP/styles/orchestr8.css")
    assert css.exists(), "orchestr8.css missing"
    
    # 2. Load font profiles
    font_profile = get_settings().get("ui.general.font_profile", "hard_comp")
    font_css = inject_font_profile(font_profile)  # From font_profiles.py
    
    # 3. Load Three.js renderer
    js_path = Path("IP/static/woven_maps_3d.js")
    assert js_path.exists(), "woven_maps_3d.js missing"
    
    return css, font_css, js_path
```

### 4.4 Font Injection Pattern

```python
# IP/styles/font_profiles.py

FONT_PROFILES = {
    "hard_comp": {
        "display": "HardCompn, serif",
        "ui": "CalSans-SemiBold, sans-serif", 
        "data": "mini_pixel-7, monospace"
    },
    # Additional profiles...
}

def inject_font_profile(profile_name: str) -> str:
    """Generate CSS for font profile."""
    profile = FONT_PROFILES.get(profile_name, FONT_PROFILES["hard_comp"])
    return f"""
        :root {{
            --font-display: {profile['display']};
            --font-ui: {profile['ui']};
            --font-data: {profile['data']};
        }}
    """
```

---

## 5. MIGRATION STRATEGY WITH ROLLBACK (R-4)

### 5.1 Migration Phases

```
PHASE 1: Foundation
├── Create app/ module structure
├── Centralize mo.state() in _state.py
└── Verify Marimo patterns compile

PHASE 2: Visual Integration  
├── Verify CSS tokens match LOCK
├── Test font injection
└── Verify Three.js color mappings

PHASE 3: Service Migration
├── Extract services to app/modules/_services.py
├── Extract handlers to app/modules/_handlers.py
└── Verify service instantiation once

PHASE 4: Component Migration
├── Migrate panel components
├── Migrate Code City integration
└── Verify end-to-end flow

PHASE 5: Cutover
├── Run full test suite
├── Enable feature flag
├── Monitor for 24h
└── Complete or rollback
```

### 5.2 Feature Flag Configuration

```python
# orchestr8_next/config.py

import os

class FeatureFlags:
    """Feature flags for migration control."""
    
    # Core flags
    USE_NEW_STRUCTURE = os.getenv('ORCHESTR8_USE_NEW', 'false').lower() == 'true'
    USE_NEW_STATE = os.getenv('ORCHESTR8_USE_NEW_STATE', 'false').lower() == 'true'
    USE_NEW_SERVICES = os.getenv('ORCHESTR8_USE_NEW_SERVICES', 'false').lower() == 'true'
    
    # Feature flags for gradual rollout
    ENABLE_CONNECTION_ACTIONS = os.getenv('ORCHESTR8_ENABLE_CONNECTION_ACTIONS', 'false').lower() == 'true'
    ENABLE_COMBAT_TRACKER = os.getenv('ORCHESTR8_ENABLE_COMBAT_TRACKER', 'false').lower() == 'true'
    
    @classmethod
    def is_enabled(cls, flag: str) -> bool:
        return getattr(cls, flag, False)
```

### 5.3 Proxy Pattern for Backward Compatibility

```python
# orchestr8_next/compat.py
"""
Proxy pattern for gradual migration.
Routes to old or new implementation based on feature flags.
"""

from orchestr8_next.config import FeatureFlags

class HealthCheckerProxy:
    """Proxy that routes to old or new implementation."""
    
    def __init__(self):
        if FeatureFlags.USE_NEW_SERVICES:
            from app.modules._services import HealthChecker as NewHealthChecker
            self._impl = NewHealthChecker()
        else:
            from IP.health_checker import HealthChecker as LegacyHealthChecker
            self._impl = LegacyHealthChecker()
    
    def check(self, path: str):
        return self._impl.check(path)
    
    def get_status(self, path: str):
        return self._impl.get_status(path)
```

### 5.4 Rollback Strategy

| Phase | Rollback Criteria | Rollback Action |
|-------|-------------------|-----------------|
| P1: Foundation | Module import fails | Revert to single-file structure |
| P2: Visual | Token mismatch > 1px/1hex | Revert CSS to last known good |
| P3: Services | Service instantiation errors | Revert to inline instantiation |
| P4: Components | Panel rendering broken | Disable flag, use old components |
| P5: Cutover | Error rate > 1% | Disable feature flag, use old system |

### 5.5 Rollback Execution

```bash
# Emergency rollback command
export ORCHESTR8_USE_NEW=false
export ORCHESTR8_USE_NEW_STATE=false  
export ORCHESTR8_USE_NEW_SERVICES=false

# Restart marimo
marimo run orchestr8.py
```

---

## 6. CONTRACT TESTING APPROACH (R-5)

### 6.1 Layer Contract Tests

```python
# tests/contracts/test_l1_l2.py

def test_l1_does_not_import_l3():
    """
    L1 (presentation) should not import L3 (services) directly.
    Enforce layer boundaries.
    """
    l1_files = list(Path("app/modules/").glob("*.py"))
    
    for file in l1_files:
        content = file.read_text()
        # Check for forbidden imports
        forbidden = ["IP/services/", "IP/adapters/", "IP/llm/"]
        
        for pattern in forbidden:
            assert pattern not in content, f"{file} imports L3: {pattern}"

def test_state_initialized_at_module_level():
    """All mo.state() calls must be module-level."""
    state_file = Path("app/modules/_state.py")
    content = state_file.read_text()
    
    # Find function definitions
    in_function = False
    for line in content.split('\n'):
        if line.strip().startswith('def '):
            in_function = True
        if 'mo.state' in line and in_function:
            raise AssertionError("mo.state() found inside function - must be module-level")
```

### 6.2 Visual Token Verification Tests

```python
# tests/visual/test_tokens.py

def test_css_tokens_match_lock():
    """Verify orchestr8.css tokens match VISUAL_TOKEN_LOCK.md"""
    lock = parse_visual_token_lock("SOT/VISUAL_TOKEN_LOCK.md")
    css = parse_css_variables("IP/styles/orchestr8.css")
    
    # Color tokens
    for token, expected in lock['colors'].items():
        actual = css.get(f"--{token}")
        assert actual == expected, f"Color token drift: {token}"
    
    # Typography tokens
    for token, expected in lock['typography'].items():
        actual = css.get(f"--{token}")
        assert actual == expected, f"Typography token drift: {token}"
    
    # Dimension tokens
    for token, expected in lock['dimensions'].items():
        actual = css.get(f"--{token}")
        assert actual == expected, f"Dimension token drift: {token}"

def test_threejs_colors_match_tokens():
    """Verify JavaScript colors match CSS tokens."""
    js = Path("IP/static/woven_maps_3d.js").read_text()
    
    # Extract color definitions
    import re
    color_pattern = r"'state-(\w+)':\s*(0x[0-9A-Fa-f]+)"
    colors = dict(re.findall(color_pattern, js))
    
    lock = parse_visual_token_lock("SOT/VISUAL_TOKEN_LOCK.md")
    
    for state, hex_val in colors.items():
        expected = lock['colors'][f'state-{state}']
        assert hex_val == expected, f"Three.js color mismatch: {state}"
```

### 6.3 Import Audit

```bash
# scripts/audit_imports.py

#!/usr/bin/env python3
"""Audit import patterns across codebase."""

import ast
from pathlib import Path

FORBIDDEN_IMPORTS = {
    "app/modules/_state.py": ["IP/", "app/lib/"],
    "app/modules/_handlers.py": ["IP/services/", "IP/adapters/"],
    "IP/plugins/06_maestro.py": ["app/lib/services/"],
}

def audit_imports():
    """Check for layer boundary violations."""
    violations = []
    
    for file_path, forbidden in FORBIDDEN_IMPORTS.items():
        content = Path(file_path).read_text()
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for pattern in forbidden:
                        if pattern in alias.name:
                            violations.append(f"{file_path}: imports {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for pattern in forbidden:
                        if pattern in node.module:
                            violations.append(f"{file_path}: from {node.module} ...")
    
    if violations:
        print("IMPORT VIOLATIONS FOUND:")
        for v in violations:
            print(f"  - {v}")
        raise SystemExit(1)
    else:
        print("✅ All import contracts satisfied")
```

---

## 7. PHASE IMPLEMENTATION ORDER

### Phase 1: Foundation (Week 1)

| Task | Owner | Deliverable |
|------|-------|-------------|
| Create app/ directory structure | Agent | Module files |
| Centralize mo.state() in _state.py | Agent | Single state file |
| Extract services to _services.py | Agent | Service module |
| Extract handlers to _handlers.py | Agent | Handler module |

**Gate:** `marimo run app/app.py` starts without errors

### Phase 2: Visual Integration (Week 1-2)

| Task | Owner | Deliverable |
|------|-------|-------------|
| Verify CSS tokens match LOCK | Agent | Test pass |
| Test font injection | Agent | Fonts render |
| Verify Three.js color mappings | Agent | Colors match |

**Gate:** Visual token tests pass

### Phase 3: Service Migration (Week 2)

| Task | Owner | Deliverable |
|------|-------|-------------|
| Migrate Health Checker | Agent | Works in new structure |
| Migrate Combat Tracker | Agent | Works in new structure |
| Migrate Connection Verifier | Agent | Works in new structure |

**Gate:** All services instantiate correctly

### Phase 4: Component Migration (Week 2-3)

| Task | Owner | Deliverable |
|------|-------|-------------|
| Migrate Panel System | Agent | Panels render |
| Migrate Code City integration | Agent | 3D renders |
| Migrate Control Surface | Agent | Controls work |

**Gate:** End-to-end flow functional

### Phase 5: Cutover (Week 3)

| Task | Owner | Deliverable |
|------|-------|-------------|
| Run full test suite | CI | 11 tests pass |
| Enable feature flag | Ops | New system active |
| Monitor for 24h | Ops | Error rate < 1% |

**Gate:** Production ready or rollback

---

## 8. ACCEPTANCE GATES

| Gate | Criteria | Verification |
|------|----------|--------------|
| P00 | Layer boundaries documented | Architecture review |
| P01 | All controls dispatch typed actions | Integration test |
| P02 | Service adapters hot-swappable | Feature flag test |
| P03 | IDE integrations work as modules | Manual test |
| P04 | Code City reconnects | Visual verification |
| P05 | Contract tests pass | CI pipeline |
| P06 | End-to-end reliability | 24h monitor |

---

## 9. RISK MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Token drift | Medium | High | Automated CSS token tests |
| Layer violation | Medium | High | Import audit in CI |
| Migration breaks | High | High | Feature flags + proxy pattern |
| Three.js color mismatch | Low | Medium | Visual token verification |
| Performance regression | Low | High | Load testing in P05 |

---

## 10. REFERENCES

| Document | Location | Purpose |
|----------|----------|---------|
| VISUAL_TOKEN_LOCK.md | SOT/ | Canonical visual tokens |
| ARCHITECTURE_BLUEPRINT.md | .planning/orchestr8_next/architecture/ | Layer architecture |
| MARIMO_STRUCTURE_CLEANUP_SPEC.md | .planning/orchestr8_next/artifacts/P07/integration/ | Marimo patterns |
| CANONICAL_VISUAL_INTEGRATION_SPEC.md | .planning/orchestr8_next/artifacts/P07/integration/ | Visual spec |
| INTEGRATION_EXECUTION_STRATEGY.md | .planning/orchestr8_next/artifacts/P07/integration/ | Migration waves |

---

## DECISION REQUIRED

Before execution, confirm:

1. ✅ **Canonical source of truth** - VISUAL_TOKEN_LOCK.md confirmed
2. ✅ **Entry point** - orchestr8.py confirmed (no path change)
3. ✅ **Main render** - IP/plugins/06_maestro.py confirmed (no path change)
4. ✅ **Layer architecture** - L1-L5 boundaries confirmed
5. ✅ **Migration approach** - Feature flags + proxy pattern confirmed
6. ✅ **Testing strategy** - Contract tests + visual token verification confirmed

---

**STATUS: READY FOR EXECUTION**

This plan is ready for Task Master to generate implementation tasks.
