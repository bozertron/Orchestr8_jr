# Wave 2 Reference Document - Phreak + CSE Integration

**Created:** 2026-02-16  
**Maintained by:** [ASSIGNED AGENT]  
**Status:** READY FOR WAVE 2

---

## Wave 1 Completion Summary

| Plan | Status | Commits |
|------|--------|---------|
| 08-01 Void-styled settings UI | ✅ COMPLETE | 1655ea4, 60cc8a4 |
| 08-02 Pydantic validation + preview | ✅ COMPLETE | f27135e, 094fd72 |
| 08-03 Summon interface refinement | ✅ COMPLETE | 71fbc13, 31b4e61 |

---

## Wave 2 Completion Summary

| Plan | Status | Commits |
|------|--------|---------|
| 08-04 Phreak Typography Migration | ✅ COMPLETE | f6ec6b8, 4ceddf4 |
| 08-05 CSE Single-Pass Wiring + SettingsService | ✅ COMPLETE | 1c11f3c, a6f7ae9 |

---

## Phase 8 Complete: 5/5 Plans ✅

### Files Modified
- `IP/plugins/07_settings.py` - Refactored to use orchestr8.css + Pydantic
- `IP/styles/orchestr8.css` - Added settings + summon CSS classes
- `IP/features/maestro/views/basic.py` - Summon interface updates

### Key Implementations
1. **Void Design CSS** - 50+ new classes, exact color tokens
2. **Pydantic Models** - Nested validation with Field validators
3. **Real-time Preview** - Font changes apply immediately
4. **Emergence Animations** - No breathing, rise animation only
5. **Diamond Dismiss** - ◇ instead of ✕

---

## Wave 2 Pending Plans

### 08-04: Phreak Typography Migration
**Objective:** Migrate to Phreak fonts (Marcellus SC, Poiret One, VT323)

**Status:** ✅ COMPLETE

**Completed Tasks:**
1. ✅ Updated font_profiles.py with phreak_nexus profile
2. ✅ Added Google Fonts CDN import for Marcellus SC, Poiret One, VT323
3. ✅ Updated orchestr8.css CSS variables (--font-header, --font-ui, --font-data)
4. ✅ Added Phreak-specific component styles (.btn-phreak, .input-phreak)
5. ✅ Updated pyproject_orchestr8_settings.toml with phreak_nexus default

**Target Files Modified:**
- `IP/styles/font_profiles.py` - Added phreak_nexus profile with Google Fonts
- `IP/styles/orchestr8.css` - Added Phreak typography variables and component styles
- `pyproject_orchestr8_settings.toml` - Set font_profile = "phreak_nexus"

### 08-05: CSE Single-Pass Wiring + SettingsService
**Objective:** Implement SettingsService with single-pass wiring

**Tasks:**
1. Create SettingsService class for typesafe TOML access
2. Wire settings read-path into core city services
3. Implement quantum commit pulse feedback

**Dependencies:**
- Requires 08-02 (Pydantic validation)
- Requires 08-04 (font profile)

**Target Files:**
- `IP/plugins/08_settings.py` (new)
- `pyproject_orchestr8_settings.toml`

---

## Canonical Color Tokens (LOCKED)

From `IP/features/maestro/config.py`:

| Token | Hex | Usage |
|-------|-----|-------|
| BLUE_DOMINANT | #1fbdea | Default / Working |
| GOLD_METALLIC | #D4AF37 | Highlight |
| PURPLE_COMBAT | #9D4EDD | Combat / Agents |
| BG_PRIMARY | #0A0A0B | The Void |

---

## Canonical Typography (LOCKED)

From `orchestr8_ui_reference.html`:

| Role | Font | CSS Variable |
|------|------|--------------|
| Headers | Marcellus SC | --font-header |
| UI | Poiret One | --font-ui |
| Data/Console | VT323 | --font-data |

---

## CSE Architecture Requirements

1. **Single-Pass Wiring:** Logic + TOML + UI implemented simultaneously
2. **SettingsService:** Typesafe source of truth for all settings
3. **Real-time Sync:** <50ms UI reflection
4. **Audit Trail:** Every change triggers Action Inspector event
5. **Persistence:** Reload restores all states from temporal_state ledger

---

## Gap Analysis - ALL COMPLETE

| Gap | Severity | Plan | Status |
|-----|----------|------|--------|
| Typography not Phreak | HIGH | 08-04 | ✅ COMPLETE |
| SettingsService not integrated | HIGH | 08-05 | ✅ COMPLETE |
| Single-pass wiring not implemented | MEDIUM | 08-05 | ✅ COMPLETE |
| Quantum commit pulse not added | LOW | 08-05 | ✅ COMPLETE |

---

## Notes for Wave 2 Agents

1. **DO NOT** use magenta/orange/lime colors - those are from deprecated spec
2. **USE** #1fbdea, #D4AF37, #9D4EDD, #0A0A0B
3. **USE** emergence animations, NOT breathing
4. **USE** diamond dismiss (◇), NOT ✕
5. **ENSURE** all changes persist to pyproject_orchestr8_settings.toml

---

## Maintainer Notes

- [UPDATE AFTER EACH WAVE 2 TASK COMPLETE]
- Document any deviations from canonical colors/typography
- Note any new dependencies discovered
- Track integration test results
