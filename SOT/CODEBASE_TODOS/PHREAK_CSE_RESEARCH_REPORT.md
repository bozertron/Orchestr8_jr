# Research Report: Phreak Mode & Comprehensive Settings Environment (CSE)

**Researched:** 2026-02-16  
**Confidence:** HIGH  
**Author:** Claude (Agent)

---

## Executive Summary

This report synthesizes the new UI decisions formalized by the Founder:

1. **Aesthetic Renamed:** "Nexus" → "Phreak"
2. **Typography Locked:** Marcellus SC (headers), Poiret One (UI), VT323 (data/console)
3. **Spacing Invariant:** Polished spacing from reference HTML
4. **CSE Architecture:** Single-pass wiring + SettingsService Python service

---

## 1. Phreak Mode Specification (CORRECTED)

### 1.1 Source Documents
- `/home/bozertron/Orchestr8_jr/IP/features/maestro/config.py` - **CANONICAL COLORS**
- `/home/bozertron/mingos_settlement_lab/Human Dashboard Aesthetic Reference/orchestr8_ui_reference.html` - Typography
- `/home/bozertron/mingos_settlement_lab/transfer/MSL_06_PHREAK_TOKEN_SPEC.md` - **DEPRECATED** (different spec)

### 1.2 Phreak Color Tokens (LOCKED - FROM 06_maestro.py)

| Token | Hex | Name | State |
|-------|-----|------|-------|
| `BLUE_DOMINANT` | `#1fbdea` | Teal | Default / Working / Broken |
| `GOLD_METALLIC` | `#D4AF37` | Gold | Highlight / Working |
| `PURPLE_COMBAT` | `#9D4EDD` | Purple | Combat / Agents Active |
| `BG_PRIMARY` | `#0A0A0B` | Void Black | Background |

### 1.3 Additional Colors (from orchestr8_ui_reference.html)

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-obsidian` | `#050505` | Background base |
| `--gold-dark` | `#C5A028` | Primary accent, borders |
| `--gold-light` | `#F4C430` | Highlight accent, hover |
| `--teal` | `#00E5E5` | Secondary accent |

---

## 2. Typography System (LOCKED)

### 2.1 Font Stack

| Role | Font | Usage |
|------|------|-------|
| `--font-header` | 'Marcellus SC', serif | Major headers, top buttons |
| `--font-ui` | 'Poiret One', cursive | UI labels, mini buttons |
| `--font-data` | 'VT323', monospace | Data, status, terminal |

### 2.2 Source: orchestr8_ui_reference.html
```html
<link href="https://fonts.googleapis.com/css2?family=Marcellus+SC&family=Poiret+One&family=VT323&display=swap" rel="stylesheet">
```

### 2.3 Current Implementation Status
- VISUAL_TOKEN_LOCK.md (line 48-50) confirms these as LOCKED
- orchestr8.css needs migration from previous HardCompn/CalSans/Mini Pixel

---

## 3. Spacing System (LOCKED)

### 3.1 Source: orchestr8_ui_reference.html

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 8px | Internal button padding |
| `--space-sm` | 12px | Mini button horizontal |
| `--space-md` | 15-25px | Button deck margins |
| `--space-lg` | 30-40px | Header/footer padding |
| `--gap-btn-group` | 8px | Button group gap |
| `--gap-deck-row` | 20px | Deck row gap |

### 3.2 Header Dimensions
- Header height: 80px
- Top button height: 50px
- Top button min-width: 160px

### 3.3 Footer Dimensions (Lower Fifth)
- Input padding: 8px 0
- Mini button height: 22px
- Mini button min-width: 60px
- Maestro button height: 36px

---

## 4. Comprehensive Settings Environment (CSE)

### 4.1 Architecture: Single-Pass Wiring

**Concept:** Instead of separate steps for logic + persistence + UI, implement all three simultaneously.

| Component | Responsibility |
|-----------|----------------|
| **SettingsService** | Python service - typesafe source of truth for TOML |
| **pyproject_orchestr8_settings.toml** | Persistent storage |
| **Phreak Settings Panel** | UI representation |

### 4.2 SettingsService Design

**Target Implementation:**
- `/home/bozertron/a_codex_plan/orchestr8_next/settings/service.py` (in progress)

**Responsibilities:**
1. Typesafe access to pyproject_orchestr8_settings.toml
2. Backend logic consumption
3. Frontend UI data binding
4. Validation on load/save
5. Change events for real-time sync

### 4.3 CSE Control Surfaces

| Surface | Requirement |
|---------|-------------|
| **Registry** | Virtualized HistoryPanel for settings |
| **Toggle State** | Teal=Enabled, Greyscale=Disabled |
| **Value Change** | "Quantum Commit" pulse feedback |
| **Phreak Token Vault** | Console-style input with ToolCallCard audit |
| **Validation** | Real-time Glitch color feedback |

### 4.4 Behavioral Requirements

- **Sync Latency:** UI reflects SettingsService change within <50ms
- **Persistence Proof:** Reload restores all states from temporal_state ledger
- **Auditability:** Every setting change triggers Action Inspector event + Quantum Tick

---

## 5. Integration Status

### 5.1 Current State

| Component | Status | Location |
|-----------|--------|----------|
| **VOID Design** | ✅ Active | orchestr8.css + 06_maestro.py |
| **Typography (Phreak)** | ⚠️ Partial | orchestr8_css needs migration to Poiret One/VT323 |
| **SettingsService** | 🔄 In Progress | a_codex_plan lane |
| **CSE UI** | 🔄 In Progress | P07-B7 packet |

### 5.2 Gap Analysis

| Gap | Severity | Action |
|-----|----------|--------|
| **OLD DEPRECATED SPEC** | NOTE | MSL_06_PHREAK_TOKEN_SPEC.md (magenta/orange/lime) is NOT used |
| Typography migration incomplete | HIGH | Replace current fonts → Poiret One/VT323/Marcellus SC |
| SettingsService not in orchestr8_jr | MEDIUM | Wait for B7 to merge |
| CSE UI constraints not implemented | MEDIUM | Future phase |

---

## 6. Recommendations

### 6.1 Immediate Actions

1. **Confirm current orchestr8.css has correct Void colors:**
```css
:root {
    --blue-dominant: #1fbdea;
    --gold-metallic: #D4AF37;
    --purple-combat: #9D4EDD;
    --bg-primary: #0A0A0B;
}
```

2. **Migrate typography in orchestr8.css to Phreak fonts:**
```css
--font-header: 'Marcellus SC', serif;
--font-ui: 'Poiret One', cursive;
--font-data: 'VT323', monospace;
```

3. **Add Phreak button styling (using existing Void colors):**
```css
.btn-phreak {
    font-family: var(--font-data);
    font-style: italic;
    color: var(--gold-metallic);
    border: 1px solid var(--gold-dark);
}
```

### 6.2 Future Actions

1. Complete SettingsService implementation (P07-B7)
2. Wire settings read-path into core city services
3. Implement CSE UI constraints
4. Add quantum commit pulse animation

---

## 7. Sources

### Primary (HIGH confidence)
- `IP/features/maestro/config.py` - **CANONICAL** color definitions (BLUE_DOMINANT, GOLD_METALLIC, PURPLE_COMBAT)
- `orchestr8_ui_reference.html` - **CANONICAL** typography (Marcellus SC, Poiret One, VT323)
- `VISUAL_TOKEN_LOCK.md` - Locked tokens
- `MSL_06_CSE_UI_CONSTRAINTS.md` - CSE requirements

### Secondary (MEDIUM confidence)
- `MSL_06_PHREAK_TOKEN_SPEC.md` - **DEPRECATED** - different/older spec, not currently used
- `07_settings.py` - Current settings implementation
- `orchestr8.css` - Current CSS
- P07-B7 packet scope - SettingsService work

---

## 8. Conclusion

The Phreak aesthetic and CSE architecture represent a significant evolution of the Orchestr8 visual system. The key components are:

1. **Visual Design** comes from **06_maestro.py / VOID Design** (teal/gold/purple)
2. **Typography** comes from **orchestr8_ui_reference.html** (Marcellus SC, Poiret One, VT323)
3. **Single-pass wiring** eliminates the logic/persistence/UI drift problem
4. **SettingsService** provides typesafe access from both backend and frontend

**Note:** The MSL_06_PHREAK_TOKEN_SPEC.md file (magenta/orange/lime) is a DEPRECATED/ALTERNATE spec and is NOT the one currently in use.

**Risk:** The typography migration from current fonts to Phreak fonts requires careful CSS update to avoid visual regression.

**Next Step:** Execute P07-B7 packet (SettingsService + Phreak token wiring) in a_codex_plan lane.
