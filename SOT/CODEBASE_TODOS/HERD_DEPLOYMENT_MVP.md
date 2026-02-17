# Herd Deployment Plan — MVP Sprint Packets

**Owner**: Antigravity (cross-lane synthesis)
**Date**: 2026-02-16
**Status**: FINAL — Ready for agent herd deployment
**Visual Contract**: All UI work complies with [VISUAL_TOKEN_LOCK.md](file:///home/bozertron/Orchestr8_jr/SOT/VISUAL_TOKEN_LOCK.md) v1

---

## Visual Token Lock Compliance Statement

The locked design tokens have been factored into every UI-touching sprint below. Here's how they map:

| Token Category | Locked Values | Applies To |
|---|---|---|
| **Primary Colors** | `#050505` bg-obsidian, `#C5A028` gold-dark, `#F4C430` gold-light, `#00E5E5` teal, `#CCC` text-grey | All panels, buttons, text in `06_maestro.py` and `orchestr8.css` |
| **State Colors** | `#D4AF37` working (gold), `#1fbdea` broken (blue), `#9D4EDD` combat (purple) | Code City buildings, health indicators, graph_builder.py |
| **Fonts** | Marcellus SC (headers), Poiret One (UI labels), VT323 (data/terminal) | All visible text surfaces |
| **Effects** | Gold glow hover `rgba(197,160,40,0.3)`, button shadows, scanlines | Interactive elements, emergence sequence |
| **Animation** | `0.2s` fast, `0.3s` normal, `0.5s` slow, `2s` emergence | Transitions, UI layer fade |

> [!IMPORTANT]
> **`or8_founder_console` has zero frontend files** — it is a pure Python/FastAPI backend (12 routers, JSON-only responses). Its UI surfaces are rendered by the marimo frontend in `Orchestr8_jr/IP/`. Therefore, visual token compliance for founder console features is enforced at the **rendering layer** (`06_maestro.py`, `shell.py`, `orchestr8.css`), not in the console's Python code. Any new founder-facing panel or view MUST use the locked tokens when rendered.

---

## Herd Structure (3 Herds, Overlapping Sprints)

### HERD 1: Visual Stack — *"Render it"*

- **Members**: `mingos_settlement_lab` + `antigravity`
- **Mission**: Code City visually correct and demo-ready
- **Token compliance**: State colors in buildings, font stack in HUD, gold glow on hover, obsidian background, emergence animation at 2s per phase

### HERD 2: Core Runtime — *"Wire it"*

- **Members**: `a_codex_plan` + `2ndFid_explorers`
- **Mission**: Marimo runtime functionally complete
- **Token compliance**: All new panels use `--bg-obsidian` background, `--gold-dark` borders, `--font-data` for terminal/data displays, `--teal` for interactive text

### HERD 3: Founder Tools — *"Control it"*

- **Members**: `or8_founder_console` (backend) + `Orchestr8_jr` canonical (rendering)
- **Mission**: Founder workflow operational end-to-end
- **Token compliance**: Backend serves JSON only; rendering in marimo uses locked tokens. Review queue, intent list, and approval UI must render with `--font-ui` labels, `--gold-light` approve buttons, `--state-broken` for items needing attention

---

## Sprint Schedule

```
Day 1-2   [HERD 1: Code City 3-state visual] [HERD 2: Settings + Health wiring]
Day 3-4   [HERD 1: Emergence + polish]        [HERD 2: Panels + Node Click]       [HERD 3: C2P scanner]
Day 5-6   [HERD 1: done ✓]                    [HERD 2: Carl + Connection]          [HERD 3: Review queue]
Day 7-8                                        [HERD 2: done ✓]                    [HERD 3: Dashboard]
Day 9-10                                                                            [HERD 3: done ✓ → MVP gate]
```

---

## Sprint Packets (Agent-Ready)

### Sprint 1 (Days 1-2): Foundation

#### Herd 1 — Visual Stack

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| Code City renders 3 health states | `graph_builder.py`, `woven_maps_3d.js` | `--state-working` #D4AF37, `--state-broken` #1fbdea, `--state-combat` #9D4EDD | 8-10 |
| Background renders obsidian | `orchestr8.css`, `woven_maps_template.html` | `--bg-obsidian` #050505 | 2 |
| Combat refresh trigger | `combat_tracker.py`, `06_maestro.py` | State colors on refresh | 4-6 |
| Fix marimo static asset 404s | marimo `_static/` investigation | N/A (infrastructure) | 2-3 |

#### Herd 2 — Core Runtime

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| SettingsService scaffold + persistence | `orchestr8_next/city/settings_service.py` | Settings drive visual tokens at render time | 8-10 |
| HealthWatcher wired into marimo state | `health_watcher.py`, `06_maestro.py` | Health status → state colors | 6-8 |

**Gate**: `11 passed` canonical + Code City renders gold/blue/purple buildings on obsidian background

---

### Sprint 2 (Days 3-4): Interaction

#### Herd 1 — Visual Polish

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| Emergence sequence (7 phases, 28s) | `woven_maps_3d.js` | `--transition-emergence` 2s, `--void-text` for labels | 6-8 |
| Camera + node hover | `woven_maps_3d.js` | `--glow-gold-hover` on hover | 4-6 |
| HUD overlays | `woven_maps_template.html` | `--font-header` Marcellus SC, `--tracking-normal` 2px | 3-4 |

#### Herd 2 — Panels

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| Panel system shows real data on click | `deploy_panel.py`, `shell.py` | `--bg-obsidian` panel bg, `--gold-dark` borders, `--font-data` VT323 | 8-10 |
| Working node info panel | `shell.py`, `code_city_context.py` | `--state-working` gold header, `--text-grey` #CCC body | 4-6 |
| Louis lock indicator in panels | `shell.py` | `--gold-light` lock icon, `--text-dim` when unlocked | 2-3 |

#### Herd 3 — C2P Foundation

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| Multi-repo intent scanner | `services/intent_scanner.py` | Backend only (JSON) | 6-8 |
| Intent queue API | `routers/intent_queue.py` | Backend only (JSON) | 4-6 |
| Intent rendering in marimo | `06_maestro.py` or new panel | `--font-ui` Poiret One labels, `--teal` intent text, `--gold-dark` borders | 4-6 |

**Gate**: Click a building → panel shows file info + health status + lock state, all in locked tokens

---

### Sprint 3 (Days 5-6): Connectivity

#### Herd 2 — Backend Integration

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| Carl context → Summon payload | `carl_core.py`, `06_maestro.py` | Context display uses `--font-data` VT323 | 6-8 |
| Connection Verifier contracts | `connection_verifier.py`, `patchbay.py` | Connection status uses state colors | 4-6 |
| Terminal spawner integration | `terminal_spawner.py` | Terminal text: `--font-data` VT323, `--bg-obsidian` bg | 4-6 |

#### Herd 3 — Review Flow

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| Review queue with approve/edit/dismiss | `routers/review.py` (backend) | Backend JSON only |  6-8 |
| Review UI rendering | Marimo panel in `06_maestro.py` | Approve btn: `--gold-light` + `--glow-gold-hover`; Dismiss: `--text-dim` | 4-6 |

**Gate**: Summon an agent → context payload includes Code City state; Founder sees review queue

---

### Sprint 4 (Days 7-8): Polish + Integration

#### Herd 3 — Founder Workflow

| Task | Files | Token Compliance | Hours |
|------|-------|------------------|-------|
| One-click packet launch | `routers/packets.py` (backend) + marimo render | Launch btn: `--btn-maestro-height` 36px, `--shadow-maestro`, Marcellus SC | 8-10 |
| Governance dashboard | New marimo panel | `--font-header` titles, `--font-data` metrics, state colors for lane health | 6-8 |

**Gate**: Founder can see Code City → click building → review intent → launch packet (all in locked visual tokens)

---

### Sprint 5 (Days 9-10): MVP Gate

All herds converge for **Friendly-Circle Test**:

- [ ] Code City renders with locked state colors on obsidian
- [ ] All text uses locked font stack (Marcellus SC / Poiret One / VT323)
- [ ] Click building → panel with real data in locked tokens
- [ ] Summon agent → context payload includes Code City state
- [ ] Founder console → review intents → approve/launch → all rendered in locked tokens
- [ ] Settings persist and drive visual behavior
- [ ] All canonical tests pass (`11+` base, `15+` integration)
- [ ] Desktop Linux fullscreen — no visual breaks

---

## Verification Plan

### Automated (after every sprint)

```bash
# Canonical gate
pytest tests/reliability/test_reliability.py tests/city/test_binary_payload.py \
  tests/city/test_wiring_view.py tests/city/test_parity.py -q  # 11 passed

# Integration gate
pytest tests/integration/ -q  # 15+ passed

# Founder console
cd /home/bozertron/or8_founder_console && python -m pytest tests/ -v  # 37+ passed
```

### Visual Token Compliance Check (manual per sprint gate)

1. Open `marimo run orchestr8.py` in browser
2. Verify background is `#050505` (not pure black)
3. Verify building colors match state tokens exactly
4. Verify button hover produces gold glow (`rgba(197,160,40,0.3)`)
5. Verify fonts: headers in Marcellus SC, labels in Poiret One, data in VT323
6. Screenshot and commit to `.planning/orchestr8_next/artifacts/`

---

## File Location

This plan is located at:

```
/home/bozertron/Orchestr8_jr/SOT/CODEBASE_TODOS/HERD_DEPLOYMENT_MVP.md
```

Ready for agent herd deployment. Each sprint packet above contains:

- Exact files to modify  
- Token compliance requirements per task  
- Hour estimates  
- Gate criteria
