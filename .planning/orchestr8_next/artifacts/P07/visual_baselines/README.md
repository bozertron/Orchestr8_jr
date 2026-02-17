# Visual Baselines Directory

Owner: Orchestr8_jr (Canonical Lane)
Status: ACTIVE - v1
Last Updated: 2026-02-15
Evidence Links: orchestr8_ui_reference.html, Observation #1464

## Purpose

Repository for visual baseline snapshots and comparison artifacts.

## Canonical Baseline

| Asset | Path | Description |
|-------|------|-------------|
| Reference HTML | `/home/bozertron/Downloads/orchestr8_ui_reference.html` | Primary visual contract |
| Screenshot | `baseline_desktop.png` | Desktop viewport capture (TODO) |

## Baseline Specifications

### Desktop Viewport

| Property | Value |
|----------|-------|
| Width | 1280px |
| Height | 800px |
| Device Pixel Ratio | 1x |

### Capture Conditions

- Clean browser profile (no extensions)
- Firefox or Chrome latest
- Post-emergence state (READY phase)
- No user interaction

## Snapshot Protocol

### Creating a Baseline

1. Launch `marimo run orchestr8.py`
2. Wait for READY phase (30s)
3. Capture full viewport
4. Save as `baseline_[viewport]_[date].png`
5. Document in this README

### Comparing Against Baseline

1. Capture new snapshot under same conditions
2. Use image diff tool (pixelmatch, etc.)
3. Document drift in FRONTEND_DEBT_QUEUE.md
4. Determine if drift is intentional or regression

## File Naming Convention

```
baseline_[viewport]_[date].png
drift_[packet_id]_[date].png
comparison_[baseline]_vs_[candidate].png
```

Examples:
- `baseline_desktop_2026-02-15.png`
- `drift_P07-C1_2026-02-16.png`
- `comparison_baseline_vs_P07B1.png`

## Acceptance Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Pixel diff | < 0.1% | Accept |
| Pixel diff | 0.1% - 1% | Review |
| Pixel diff | > 1% | Reject/Document |

## Current Baseline Status

| Baseline | Status | Last Captured |
|----------|--------|---------------|
| Desktop (1280x800) | CAPTURE_NEEDED | - |
| Mobile (375x667) | FUTURE | - |

## Baseline Inventory

| File | Date | Viewport | Status |
|------|------|----------|--------|
| (awaiting capture) | - | - | - |

## Change Log

| Date | Change | Authority |
|------|--------|-----------|
| 2026-02-15 | Initial directory setup | P07-A1 |
