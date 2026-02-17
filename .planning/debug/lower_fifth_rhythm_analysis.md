# Lower-Fifth Control Surface Rhythm Analysis

**Task:** Task 21 - Analyze button layout rhythm from MaestroView.vue
**Date:** 2026-02-13

---

## 1. Reference Implementation (MaestroView.vue)

### Button Distribution (Lines 611-660)

| Section | Buttons | Count |
|---------|---------|-------|
| **Left Group** | Apps, Matrix, Calendar, Comms, Files | 5 |
| **Center** | maestro | 1 |
| **Right Group** | Search, Record, Playback, Phreak>, Send, Attach | 6 |

**Total:** 12 buttons (5 left + 1 center + 6 right)

### Spacing Metrics (Vue Reference)

| Property | Value | Location |
|----------|-------|----------|
| `.control-surface` padding | `12px 24px` | Line 981 |
| `.control-row` gap | `16px` | Line 989 |
| `.control-group` gap | `8px` | Line 997 |
| Button padding | `6px 12px` | Line 1011 |

### Visual Structure

```
[Apps][Matrix][Calendar][Comms][Files]  [maestro]  [Search][Record][Playback][Phreak>][Send][Attach]
        LEFT (5)                             CENTER (1)                         RIGHT (6)
```

---

## 2. Current Orchestr8 Implementation

### Button Distribution (06_maestro.py)

| Section | Buttons | Count |
|---------|---------|-------|
| **Left Group** | Apps, Calendar*, Comms*, Files | 4 |
| **Center** | maestro, Search | 2 |
| **Row 2 (Right)** | Record, Playback, Phreak>, Send, Attach, Settings | 6 |

**Total:** 12 buttons (but laid out in 3 rows, not 1 row with groups)

### Spacing Metrics (Python/marimo)

| Property | Value | Location |
|----------|-------|----------|
| Button hstack gap | `0.25` (rem units) | Lines 1997, 2035 |
| Center group gap | `0.35` | Line 2045 |
| Top controls gap | `0.5` | Line 2054 |
| Container padding | `0.5rem 0 0` | Line 2065 |

---

## 3. Rhythm Assessment

### Issues Identified

| Issue | Severity | Description |
|-------|----------|-------------|
| **Asymmetric button count** | High | Vue: 5 left / 6 right. Orchestr8: 4 left / 8 right (includes Settings) |
| **Missing Matrix button** | Medium | Vue has "Matrix" but Orchestr8 doesn't include it |
| **Layout structure differs** | High | Vue uses single row with left/center/right groups. Orchestr8 uses 2-3 separate rows |
| **Gap inconsistency** | Low | Vue uses 16px/8px, Orchestr8 uses 0.25rem/0.35rem/0.5rem (mix) |
| **Missing center Search placement** | Medium | Vue has Search in right group; Orchestr8 puts Search in center |

### Visual Imbalance

- **Vue Reference:** Clean 3-column layout with `justify-content: space-between`
- **Orchestr8:** Vertical stack of hstacks - loses the horizontal rhythm

---

## 4. Recommendations for Task 22

### Priority 1: Replicate Vue Layout Structure

1. **Single control row** with left group, center maestro, right group
2. **Add Matrix button** to left group (between Apps and Calendar)
3. **Move Search** to right group (per Vue reference)
4. **Remove Settings** from control surface (it has its own portal corner button)

### Priority 2: Fix Spacing

| Current | Recommended |
|---------|-------------|
| `gap=0.25` | `gap=0.5` (8px equivalent) |
| `gap=0.35` | `gap=0.75` (12px - more breathing room for center) |
| No row gap | Add `gap=1.0` between chat input and control row |

### Priority 3: Visual Balance

- **Left group:** 5 buttons (Apps, Matrix, Calendar, Comms, Files)
- **Center:** 1 button (maestro)
- **Right group:** 6 buttons (Search, Record, Playback, Phreak>, Send, Attach)

This achieves the 5/1/6 rhythm matching the Vue reference.

---

## 5. Implementation Notes

### CSS Requirements

```css
.control-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.control-group {
    display: flex;
    align-items: center;
    gap: 8px;
}

.control-left { justify-content: flex-start; }
.control-right { justify-content: flex-end; }
```

### Marimo Implementation

Need to restructure `build_control_surface()` to return a single `mo.hstack` containing three elements:
1. `left_buttons` (hstack of 5)
2. `center_btn` (solo)
3. `right_buttons` (hstack of 6)

Then wrap in outer hstack with `justify="space-between"`.

---

## Summary

| Metric | Vue Reference | Current Orchestr8 | Target |
|--------|---------------|-------------------|--------|
| Left buttons | 5 | 4 | 5 |
| Center buttons | 1 | 2 | 1 |
| Right buttons | 6 | 6 | 6 |
| Layout rows | 1 | 2-3 | 1 |
| Row gap | 16px | ~4px | 16px |
| Group gap | 8px | 4px | 8px |

**Rhythm Goal:** Achieve the 5-1-6 horizontal distribution with proper spacing to match the Vue "Overton window" control surface aesthetic.
