# contracts/status_merge_policy.py Integration Guide

- Source: `IP/contracts/status_merge_policy.py`
- Total lines: `43`
- SHA256: `64f01c4d86c17dcb367b16825077267c33ded69247533b1148e396cdf6e0f2a8`
- Role: **Canonical Status Precedence** — Three-state color system merge logic (combat > broken > working)

## Why This Is Painful

- Status precedence is a project-wide invariant: All status merges MUST use this function
- Color mapping must match CLAUDE.md spec exactly (Gold=#D4AF37, Teal=#1fbdea, Purple=#9D4EDD)
- Default to "working" is a design decision that affects all callers

## Anchor Lines

- `IP/contracts/status_merge_policy.py:3` — `StatusType = Literal["working", "broken", "combat"]` — Type alias
- `IP/contracts/status_merge_policy.py:6` — `STATUS_PRIORITY = {...}` — Precedence dict (combat=3, broken=2, working=1)
- `IP/contracts/status_merge_policy.py:12` — `def merge_status(*statuses)` — Main merge function
- `IP/contracts/status_merge_policy.py:36` — `def get_status_color(status)` — Hex color lookup
- `IP/contracts/status_merge_policy.py:38-40` — Color dict with exact hex values

## Integration Use

- `merge_status("working", "broken")` → `"broken"` — Broken overrides working
- `merge_status("combat", "working", "broken")` → `"combat"` — Combat wins all
- `merge_status()` → `"working"` — Empty input defaults to working
- `get_status_color("combat")` → `"#9D4EDD"` — Get canonical color

## Canonical Colors

| Status | Priority | Hex | Name |
|--------|----------|-----|------|
| working | 1 | #D4AF37 | Gold |
| broken | 2 | #1fbdea | Teal/Blue |
| combat | 3 | #9D4EDD | Purple |

## Resolved Gaps

- [x] merge_status() validates inputs and raises ValueError on unknown status
- [x] None values filtered before merge
- [x] get_status_color() provides canonical hex mapping
- [x] Imported and used in woven_maps.py:26
