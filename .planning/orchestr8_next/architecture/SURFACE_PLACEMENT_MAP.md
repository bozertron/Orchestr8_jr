# SURFACE PLACEMENT MAP

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, FRONTEND_SURFACE_REGISTRY.md

## Purpose

Authoritative mapping of data streams from non-canonical lanes to frontend surfaces.

## Placement Rule

> Non-canonical lanes (B: a_codex_plan, C: 2ndFid_explorers) expose stable contracts and streams.
> **Canonical lane (Orchestr8_jr) maps those streams to final visual surfaces.**

## Lane Responsibility Matrix

| Lane | Produces | Does Not Decide |
|------|----------|-----------------|
| B: a_codex_plan | Data adapters, middleware, contracts | UI placement, visual tokens |
| C: 2ndFid_explorers | Extraction packets, conversion specs | UI placement, visual tokens |
| A: Orchestr8_jr | Surface mapping, visual contract | N/A |

## Stream-to-Surface Mapping

### Code City Streams

| Stream Source | Lane | Target Surface | Adapter |
|---------------|------|----------------|---------|
| `city:nodes` | B | CANVAS_3D | woven_maps.py |
| `city:edges` | B | CANVAS_3D | woven_maps.py |
| `city:state` | B | CODE_CITY_UI | woven_maps.py |

### Header Streams

| Stream Source | Lane | Target Surface | Status |
|---------------|------|----------------|--------|
| `header:nav` | A | HEADER_CONTAINER | Active |
| `header:actions` | A | BTN_ORCHESTR8, BTN_COLLABOR8, BTN_JFDI | Active |

### Lower Fifth Streams

| Stream Source | Lane | Target Surface | Status |
|---------------|------|----------------|--------|
| `input:command` | A | INPUT_MAESTRO | Active |
| `controls:actions` | A | BTN_GRP_LEFT, BTN_GRP_RIGHT | Active |
| `maestro:invoke` | A | BTN_MAESTRO | Active |

### Status Streams

| Stream Source | Lane | Target Surface | Status |
|---------------|------|----------------|--------|
| `system:phase` | A | STATUS_TEXT | Active |
| `system:telemetry` | B | TBD | Future |

## Integration Protocol

### Step 1: Stream Declaration (Non-Canonical Lane)

```markdown
## Stream Declaration

- Stream ID: [unique identifier]
- Lane: [B or C]
- Data Type: [schema description]
- Update Frequency: [real-time | periodic | on-demand]
- Consumer Contract: [what the consumer must provide]
```

### Step 2: Surface Mapping Proposal (Canonical Lane)

```markdown
## Surface Mapping Proposal

- Stream ID: [from Step 1]
- Target Surface: [from FRONTEND_SURFACE_REGISTRY]
- Adapter Module: [file path]
- Visual Token Impact: [none | list affected tokens]
- Freeze Impact: [none | list affected frozen files]
```

### Step 3: Approval

| Approver | Condition |
|----------|-----------|
| Orchestr8_jr | All mappings |
| Codex | Contract changes |
| Founder | Freeze unlocks |

## Current Mappings

| Stream | Surface | Adapter | Approved |
|--------|---------|---------|----------|
| city:nodes | CANVAS_3D | IP/woven_maps.py | YES |
| city:edges | CANVAS_3D | IP/woven_maps.py | YES |
| header:nav | HEADER_CONTAINER | 06_maestro.py | YES |
| input:command | INPUT_MAESTRO | 06_maestro.py | YES |
| maestro:invoke | BTN_MAESTRO | 06_maestro.py | YES |

## Pending Mappings

| Stream | Proposed Surface | Status | Blocker |
|--------|------------------|--------|---------|
| - | - | - | - |

## Placement Constraints

1. No surface may receive more than one primary stream
2. Stream adapters must not modify visual tokens
3. Surface placement changes require freeze unlock if frozen
4. All mappings must be documented in this file

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial placement map | P07-A1 |
