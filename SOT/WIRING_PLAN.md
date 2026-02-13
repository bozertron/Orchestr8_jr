# Orchestr8 Wiring Plan

**Created:** 2026-01-30
**Revised:** 2026-02-13
**Authority Chain:** `.planning/phases/CONTEXT.md` > `.planning/VISION-ALIGNMENT.md`
**Status:** MOSTLY COMPLETE

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
| P2.2 | Mermaid generator | INTENTIONAL — awaiting Carl briefing integration |

---

## Remaining Work

### 1. Campaign Log: JSON Implementation

**Canon says:** JSON files in `.orchestr8/campaigns/`
**Current:** `load_campaign_log()` stub looks for markdown CAMPAIGN_LOG.md

**Fix:** Rewrite `load_campaign_log()` to:
- Read JSON files from `.orchestr8/campaigns/`
- Return structured entries for agent historical context
- Schema flexible per canon (exact structure agent-discretion)

### 2. Mermaid → Carl Briefing Pipeline

**Canon says:** Carl deploys Mermaid diagrams to agents in briefing documents
**Current:** Fiefdom, FiefdomStatus, generate_empire_mermaid imported but not wired

**Fix:** Wire mermaid output into BriefingGenerator.generate():
- Carl calls generate_empire_mermaid() for fiefdom structure
- Include diagram in briefing markdown
- Agents receive visual context alongside textual context

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
- [ ] Campaign log reads JSON from `.orchestr8/campaigns/`
- [ ] Mermaid diagrams wired to Carl briefings
