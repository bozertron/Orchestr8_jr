# A1 Canonical Replay Checklist

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE
Last Updated: 2026-02-15
Evidence Links: Observation #1464

## Purpose

Deterministic checklist for accepting/rejecting external lane packets into canonical Orchestr8_jr.

## Pre-Replay Requirements

- [ ] Packet ID recorded in STATUS.md
- [ ] Checkout message sent and acknowledged
- [ ] Source branch identified and accessible
- [ ] Target files listed explicitly

## Replay Steps

### Step 1: Environment Validation

| Check | Command | Expected |
|-------|---------|----------|
| Memory stack healthy | `curl -s http://127.0.0.1:37888/v1/memory/health` | `{"status":"ok"}` |
| Canonical tests pass | `pytest tests/reliability/test_reliability.py tests/city/test_binary_payload.py tests/city/test_wiring_view.py tests/city/test_parity.py -q` | `11 passed` |
| Widget verification | `bash scripts/verify_rehearsal.sh` | `WIDGET PASS`, `IFRAME PASS` |
| Git status clean | `git status --porcelain` | empty output |

### Step 2: Code Review

| Aspect | Criteria |
|--------|----------|
| Visual surfaces | No changes to frozen files without explicit unlock |
| Contracts | `contracts.py` changes documented and approved |
| Style | Follows existing patterns in codebase |
| Dependencies | No new runtime deps without approval |

### Step 3: Runtime Verification

- [ ] `marimo run orchestr8.py` starts without error
- [ ] UI renders with visual baseline alignment
- [ ] Controls respond to interaction
- [ ] No console errors in browser

### Step 4: Integration Testing

| Test | Command | Expected |
|------|---------|----------|
| Core reliability | `pytest tests/reliability/ -q` | all pass |
| City tests | `pytest tests/city/ -q` | all pass |
| Widget verification | `bash scripts/verify_rehearsal.sh` | both pass |

### Step 5: Documentation Completeness

- [ ] STATUS.md updated
- [ ] BLOCKERS.md updated (or marked none)
- [ ] Memory observation recorded
- [ ] Completion ping sent

## Decision Matrix

| Outcome | Condition | Action |
|---------|-----------|--------|
| ACCEPT | All steps pass | Promote, record in GUIDANCE.md |
| REWORK | 1-2 minor failures | Document issues, return to source lane |
| REJECT | 3+ failures or frozen file violation | Document rationale, require new packet |

## Frozen File Reference

Files requiring explicit unlock before modification:

```
IP/styles/*
IP/static/woven_maps_3d.js
IP/static/woven_maps_template.html
visual/layout sections in IP/plugins/06_maestro.py
```

Shared contract files (approval required):

```
orchestr8_next/city/contracts.py
orchestr8_next/shell/contracts.py
.planning/orchestr8_next/architecture/WIRING_DIAGRAMS.md
```

## Completion Record

| Packet ID | Outcome | Date | Evidence |
|-----------|---------|------|----------|
| - | - | - | - |
