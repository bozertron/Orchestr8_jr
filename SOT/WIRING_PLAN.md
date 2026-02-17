# Orchestr8 Wiring Plan

**Created:** 2026-01-30
**Revised:** 2026-02-14
**Authority Chain:** `.planning/phases/CONTEXT.md` > `.planning/VISION-ALIGNMENT.md`
**Status:** COMPLETE (canon wiring checks closed)

---

## Canon Lock Reference (2026-02-12)

- Top row: `[orchestr8] [collabor8] [JFDI]` — three buttons only
- `gener8` EXCLUDED from active UI canon
- Combat cleanup: MANUAL ONLY
- Campaign log: JSON in `.orchestr8/campaigns/`
- Mermaid: KEPT — Carl deploys to agent briefings

---

## Completed Work

| Priority | Task | Status |
|----------|------|--------|
| P0 | Brand replacement (orchestr8) | DONE |
| P1.1 | JFDI → TicketPanel | DONE (handle_jfdi → toggle_tickets) |
| P2.1 | HealthChecker wired | DONE (HealthWatcher + refresh_health + Code City merge) |
| P5.1 | Collabor8 panel | DONE (5 agent groups, picker, deploy) |
| P5.2 | Summon panel | DONE (Carl search + context JSON) |
| P2.2 | Mermaid generator | DONE (wired into `BriefingGenerator.generate()`) |
| P3.1 | Campaign log JSON path | DONE (`.orchestr8/campaigns/*.json` loader active) |

---

## Remaining Work

No open canon wiring items remain in this plan.

Evidence:
- `IP/briefing_generator.py`: `load_campaign_log()` reads `.orchestr8/campaigns/*.json`.
- `IP/briefing_generator.py`: `build_fiefdom_diagram()` + Mermaid embed in `generate()`.

---

## Cancelled Items (Contradicted Canon)

| Item | Why Cancelled |
|------|---------------|
| P1.2: Add gener8 button | Canon: excluded from active UI |
| P1.3: Remove ~~~ waves button | Doesn't exist in current code |
| P6.2: Auto combat cleanup | Canon: manual only, Founder decides |
| P3: Parse CAMPAIGN_LOG.md | Canon: format is JSON, not markdown |

---

## Validation Checklist

- [x] Brand shows "orchestr8"
- [x] CSS classes are `.orchestr8-*`
- [x] Top row: `[orchestr8] [collabor8] [JFDI]`
- [x] JFDI button opens TicketPanel
- [x] Code City renders with three colors
- [x] HealthChecker is wired (via HealthWatcher)
- [x] Collabor8 has real agent panel
- [x] Summon has Carl search integration
- [x] Campaign log reads JSON from `.orchestr8/campaigns/`
- [x] Mermaid diagrams wired to Carl briefings
