# Orchestr8 Current State Audit

**Audit Date:** 2026-02-13
**Authority Chain:** `.planning/phases/CONTEXT.md` > `.planning/VISION-ALIGNMENT.md`

---

## Canon Lock (2026-02-12 22:51:55 PST)

- [x] Top row canonical: `[orchestr8] [collabor8] [JFDI]`
- [x] `gener8` is excluded from the active UI canon
- [x] Combat cleanup is MANUAL ONLY (Founder decides)
- [x] Campaign log format is JSON in `.orchestr8/campaigns/`
- [x] Mermaid generator is KEPT — Carl deploys diagrams to agent briefings
- [x] Color system: Gold (#D4AF37) / Teal (#1fbdea) / Purple (#9D4EDD)
- [x] Building formulas: Height = `3 + (exports * 0.8)`, Footprint = `2 + (lines * 0.008)`
- [x] No breathing/pulsing animations — emergence only

---

## What's Wired and Working in 06_maestro.py

### Services Instantiated

| Service | Status | Notes |
|---------|--------|-------|
| CombatTracker | WIRED | Tracks Purple state, deploy/withdraw |
| BriefingGenerator | PARTIAL | generate() works, load_campaign_log() is STUB |
| TerminalSpawner | WIRED | Spawns terminals via Phreak> |
| TicketPanel | WIRED | JFDI button opens it |
| CalendarPanel | WIRED | Right-slide, mutual exclusion |
| CommsPanel | WIRED | Right-slide, mutual exclusion |
| FileExplorerPanel | WIRED | Right-slide, mutual exclusion |
| DeployPanel | WIRED | Modal overlay for broken nodes |
| CarlContextualizer | WIRED | Summon search + node click context |
| HealthWatcher | WIRED | File change detection → Code City |
| HealthChecker | WIRED | Via HealthWatcher callback + refresh_health() |

### Top Row: `[orchestr8] [collabor8] [JFDI]`

| Button | Handler | What It Does |
|--------|---------|--------------|
| orchestr8 | handle_home_click() | Resets all state to home view |
| collabor8 | toggle_collabor8() | Opens agent deployment panel (5 groups, 19 agents) |
| JFDI | handle_jfdi() | Opens TicketPanel (ticket-first workflow) |

### Panels That Work

| Panel | Trigger | Status |
|-------|---------|--------|
| Collabor8 (agents) | Top row button | WORKING — full agent group/picker/deploy UI |
| Settings | Bottom control + internal | WORKING — model picker + parameter display |
| Summon (search) | Search button | WORKING — Carl integration, context JSON display |
| Tickets | JFDI button | WORKING — full ticket CRUD |
| Calendar | Bottom left | WORKING — monthly grid, events |
| Comms | Bottom left | WORKING — contacts, messages, network tabs |
| Files | Bottom left | WORKING — breadcrumb nav, file listing |
| Deploy | Code City node click | WORKING — broken node → deploy agent modal |

### Code City (Woven Maps)

- Renders with three-color system (Gold/Teal/Purple)
- Health results merge into node status via status_merge_policy
- Combat files turn Purple
- Connection panel shows import edges with file names
- Click events bridge JS→Python via hidden input elements
- 71/71 contract tests passing

---

## Imports in 06_maestro.py

| Import | Status | Purpose |
|--------|--------|---------|
| mermaid_generator (Fiefdom, FiefdomStatus, generate_empire_mermaid) | INTENTIONAL | Carl deploys mermaid diagrams to agent briefings |
| HealthChecker | USED | Via HealthWatcher and refresh_health() |
| All other imports | USED | Wired to services and panels |

---

## Remaining Work

### 1. Campaign Log (JSON, not markdown)
- **Canon:** JSON files in `.orchestr8/campaigns/`
- **Current:** `load_campaign_log()` stub looks for CAMPAIGN_LOG.md (WRONG format)
- **Fix:** Rewrite to read JSON from `.orchestr8/campaigns/`

### 2. Mermaid → Carl Briefing Integration
- **Canon:** Carl deploys Mermaid diagrams to agents in briefing documents
- **Current:** Import exists, not yet wired to Carl's briefing pipeline
- **Fix:** Wire generate_empire_mermaid() into BriefingGenerator.generate()

### 3. SOT Document Accuracy
- **Previous state:** SOT docs contained contradictions with canon lock
- **Fixed:** 2026-02-13 — rewritten against authority chain

---

## Known Issues (From 14 Wiring Problems)

| # | Problem | Status |
|---|---------|--------|
| 1 | sys.path manipulation | Handled — project root detection works |
| 2 | CarlContextualizer hollow | RESOLVED — fully wired to Summon + node click |
| 3 | Generator phase locking | Not persisted (low priority) |
| 4 | Maestro "coming soon" panels | RESOLVED — all panels implemented |
| 5 | Dangling UI actions | MOSTLY RESOLVED — Apps/Matrix/Files work |
| 6 | Gatekeeper no rescan | Open (low priority) |
| 7 | Connie fragile fallback | Open (low priority) |
| 8 | Director async disconnect | Open (architecture limitation) |
| 9 | Campaign history stub | OPEN — needs JSON rewrite per canon |
| 10 | Platform assumptions | Handled — fallback chains exist |
| 11 | Unsynchronized mission state | Open (future work) |
| 12 | Manual state cleanup | BY DESIGN — canon says manual only |
| 13 | Brittle alias resolution | Open (low priority) |
| 14 | Health check assumptions | Handled — Python checkers available |
