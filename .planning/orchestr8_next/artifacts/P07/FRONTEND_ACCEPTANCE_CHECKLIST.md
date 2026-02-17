# FRONTEND ACCEPTANCE CHECKLIST

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, Observation #1464

## Purpose

Deterministic checklist for accepting frontend changes into canonical Orchestr8_jr.

## Pre-Acceptance Requirements

- [ ] Packet ID assigned and recorded
- [ ] Source lane identified (B: a_codex_plan or C: 2ndFid_explorers)
- [ ] Surface mapping documented in SURFACE_PLACEMENT_MAP.md
- [ ] Visual baseline comparison completed

## Visual Baseline Alignment

Reference: `/home/bozertron/Downloads/orchestr8_ui_reference.html`

### Structure Check

| Element | Expected | Actual | Pass |
|---------|----------|--------|------|
| Header height | 80px | - | [ ] |
| Top button height | 50px | - | [ ] |
| Void label opacity | 0.04 | - | [ ] |
| MAESTRO button height | 36px | - | [ ] |
| Mini button height | 22px | - | [ ] |

### Color Check

| Token | Expected | Actual | Pass |
|-------|----------|--------|------|
| --bg-obsidian | #050505 | - | [ ] |
| --gold-dark | #C5A028 | - | [ ] |
| --gold-light | #F4C430 | - | [ ] |
| --teal | #00E5E5 | - | [ ] |

### Typography Check

| Token | Expected | Actual | Pass |
|-------|----------|--------|------|
| --font-header | Marcellus SC | - | [ ] |
| --font-ui | Poiret One | - | [ ] |
| --font-data | VT323 | - | [ ] |

## Freeze Compliance

### Frozen File Check

| File | Modified | Authorized | Pass |
|------|----------|------------|------|
| IP/styles/orchestr8.css | [ ] | [ ] | [ ] |
| IP/static/woven_maps_3d.js | [ ] | [ ] | [ ] |
| IP/static/woven_maps_template.html | [ ] | [ ] | [ ] |
| 06_maestro.py (visual sections) | [ ] | [ ] | [ ] |

If any frozen file modified:
- [ ] Freeze unlock request submitted
- [ ] Approval documented in GUIDANCE.md

### Contract File Check

| File | Modified | Approved | Pass |
|------|----------|----------|------|
| orchestr8_next/city/contracts.py | [ ] | [ ] | [ ] |
| orchestr8_next/shell/contracts.py | [ ] | [ ] | [ ] |
| WIRING_DIAGRAMS.md | [ ] | [ ] | [ ] |

## Runtime Verification

### Startup Check

| Test | Command | Expected | Pass |
|------|---------|----------|------|
| App starts | `marimo run orchestr8.py` | No errors | [ ] |
| UI renders | Visual inspection | Baseline aligned | [ ] |

### Interaction Check

| Element | Action | Expected | Pass |
|---------|--------|----------|------|
| Top buttons | Hover | Gold glow | [ ] |
| MAESTRO button | Hover | Scale + glow | [ ] |
| Input bar | Focus | Teal border | [ ] |
| Mini buttons | Hover | White highlight | [ ] |

### Console Check

| Condition | Pass |
|-----------|------|
| No errors in browser console | [ ] |
| No CSS parser warnings | [ ] |
| No JavaScript errors | [ ] |

## Browser Compatibility

| Browser | Version | Render | Interact | Pass |
|---------|---------|--------|----------|------|
| Firefox | Latest | [ ] | [ ] | [ ] |
| Chrome | Latest | [ ] | [ ] | [ ] |

## Documentation Completeness

| Document | Updated | Pass |
|----------|---------|------|
| FRONTEND_SURFACE_REGISTRY.md | [ ] | [ ] |
| VISUAL_TOKEN_LOCK.md | [ ] | [ ] |
| SURFACE_PLACEMENT_MAP.md | [ ] | [ ] |
| FRONTEND_DEBT_QUEUE.md | [ ] | [ ] |

## Decision Matrix

| Condition | Action |
|-----------|--------|
| All checks pass | ACCEPT - promote to canonical |
| 1-2 minor failures | REWORK - return with notes |
| Freeze violation | REJECT - require new packet |
| Visual baseline drift | REWORK - alignment required |

## Acceptance Record

| Packet ID | Date | Outcome | Notes |
|-----------|------|---------|-------|
| - | - | - | - |

## Sign-Off

- [ ] All required checks completed
- [ ] Outcome recorded
- [ ] Memory observation created
- [ ] Completion ping sent

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial checklist | P07-A1 |
