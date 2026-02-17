# FRONTEND DEBT QUEUE

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, Observation #1464

## Purpose

Track frontend visual debt, drift from baseline, and remediation priority.

## Debt Categories

| Category | Definition | Priority |
|----------|------------|----------|
| VISUAL_DRIFT | Deviation from baseline appearance | Medium |
| INTERACTION_GAP | Missing or broken interactions | High |
| TOKEN_VIOLATION | Unauthorized token modifications | Critical |
| ACCESSIBILITY | A11y compliance gaps | Medium |
| PERFORMANCE | Render/interaction latency | Medium |
| COMPATIBILITY | Browser-specific issues | Low |

## Active Debt Items

### Queue Status

| ID | Category | Severity | Status | Owner | Created |
|----|----------|----------|--------|-------|---------|
| (none pending) | - | - | - | - | - |

## Debt Entry Template

```markdown
### DEBT-XXX: [Title]

- **Category**: [VISUAL_DRIFT | INTERACTION_GAP | TOKEN_VIOLATION | ACCESSIBILITY | PERFORMANCE | COMPATIBILITY]
- **Severity**: [Critical | High | Medium | Low]
- **Status**: [Open | In Progress | Blocked | Resolved]
- **Owner**: [Agent/Person]
- **Created**: [Date]
- **Source Packet**: [Packet ID or "Baseline"]

#### Description
[What is the debt item]

#### Evidence
- [Screenshot link or description]
- [Baseline comparison if applicable]

#### Impact
[User/developer impact]

#### Remediation Plan
[Proposed fix]

#### Blockers
[Any dependencies or blockers]

#### Resolution
[How it was resolved, if applicable]
```

## Resolved Debt Items

| ID | Category | Resolution Date | Resolution Summary |
|----|----------|-----------------|-------------------|
| (none yet) | - | - | - |

## Drift Log

Record visual drift detections here:

| Date | Packet | Drift % | Action | Notes |
|------|--------|---------|--------|-------|
| - | - | - | - | - |

## Known Gaps (Future Features)

These are intentional gaps, not debt:

| Gap | Description | Target Phase |
|-----|-------------|--------------|
| Apps button | Application launcher | Post-P07 |
| Calendar* button | Calendar integration | Post-P07 |
| Comms* button | Communications panel | Post-P07 |
| Files button | File browser | Post-P07 |
| Search button | Search function | Post-P07 |
| Record button | Recording toggle | Post-P07 |
| Play button | Playback control | Post-P07 |
| Phreak> button | Special action | Post-P07 |
| Send button | Send action | Post-P07 |
| Attach button | Attachment function | Post-P07 |

## Technical Debt (Non-Visual)

| ID | Description | Impact | Priority |
|----|-------------|--------|----------|
| TD-001 | HardCompn.ttf duplicate detection workaround | Font display | Medium |

## Remediation Priority Matrix

| Severity | Visual Drift | Interaction Gap | Token Violation |
|----------|--------------|-----------------|-----------------|
| Critical | Immediate | Immediate | Block packet |
| High | Next sprint | This sprint | Immediate |
| Medium | Backlog | Next sprint | This sprint |
| Low | Monitor | Backlog | Next sprint |

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Open debt items | 0 | 0 |
| Critical items | 0 | 0 |
| Avg resolution time | N/A | < 3 days |
| Baseline drift % | N/A | < 0.1% |

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial debt queue | P07-A1 |
