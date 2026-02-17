# A1 Freeze Matrix Report

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE
Last Updated: 2026-02-15
Evidence Links: Observation #1464, P07_OPERATING_MODEL.md

## Purpose

Authoritative registry of frozen files and change controls for P07.

## Freeze Categories

| Category | Definition | Unlock Authority |
|----------|------------|------------------|
| CANONICAL_FROZEN | Visual/identity critical, no changes without Founder approval | Founder |
| CONTRACT_LOCKED | Shared interfaces, requires packet-level approval | Orchestr8_jr + Codex |
| UNLOCKED | General codebase, normal packet workflow applies | Packet checkout |

## Canonical Frozen Files

Visual surfaces locked to Orchestr8_jr lane:

| File | Freeze Level | Reason | Last Modified |
|------|--------------|--------|---------------|
| `IP/styles/orchestr8.css` | CANONICAL_FROZEN | Primary stylesheet, visual contract | 2026-02-13 |
| `IP/styles/font_profiles.py` | CANONICAL_FROZEN | Font injection logic | 2026-02-13 |
| `IP/static/woven_maps_3d.js` | CANONICAL_FROZEN | 3D rendering engine | 2026-02-13 |
| `IP/static/woven_maps_template.html` | CANONICAL_FROZEN | Code City template | 2026-02-13 |
| `IP/plugins/06_maestro.py` (visual sections) | CANONICAL_FROZEN | Flagship layout | 2026-02-13 |

Visual sections in 06_maestro.py include:
- Header rendering
- Void/main area layout
- Footer control surface
- CSS injection calls
- Font profile loading

## Contract Locked Files

Shared interfaces requiring approval:

| File | Contract Type | Consumers | Unlock Requirement |
|------|---------------|-----------|-------------------|
| `orchestr8_next/city/contracts.py` | Data contracts | City module, adapters | Packet approval + integration test |
| `orchestr8_next/shell/contracts.py` | Shell contracts | Shell module, CLI | Packet approval + integration test |
| `.planning/orchestr8_next/architecture/WIRING_DIAGRAMS.md` | Event namespace | All modules | Architecture review |

## Identity Lock

| Item | Lock Status | Reason |
|------|-------------|--------|
| `maestro` identifier | PERMANENT | Flagship agent identity |
| `orchestr8` identifier | PERMANENT | Project namespace |

## Placement-Agnostic Integration Model

Non-canonical lanes (B: a_codex_plan, C: 2ndFid_explorers) follow this model:

| Lane Responsibility | Deliverable | Canonical Role |
|--------------------|-------------|----------------|
| Expose stable contracts | Function signatures, data streams | Review, approve |
| Produce packets | Code with provenance | Replay, validate |
| Document integration points | Interface specs | Map to surfaces |
| Decide final UI placement | N/A | Orchestr8_jr ONLY |

## Unlock Request Template

To request freeze unlock:

```markdown
## Freeze Unlock Request

- Packet ID: [P07-XX]
- File: [path]
- Category: [CANONICAL_FROZEN / CONTRACT_LOCKED]
- Justification: [reason]
- Proposed Changes: [summary]
- Risk Assessment: [analysis]
- Test Coverage: [plan]
```

Submit via comms to codex with `requires_ack=true`.

## Change Log

| Date | File | Change | Authority | Packet |
|------|------|--------|-----------|--------|
| 2026-02-15 | Matrix established | Initial freeze configuration | Orchestr8_jr | P07-A1 |
