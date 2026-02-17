# Task ID: 22

**Title:** Apply Lower-Fifth Symmetry Refinements

**Status:** pending

**Dependencies:** 21

**Priority:** medium

**Description:** Apply subtle spacing and alignment refinements to lower-fifth control surface to improve internal button rhythm while preserving full-width macro geometry.

**Details:**

1. Update control-surface CSS in orchestr8.css:
```css
.control-surface {
    width: 100%;
    background: var(--bg-elevated);
    border-top: 1px solid rgba(31, 189, 234, 0.2);
    padding: 12px 24px;
}

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
```

2. Apply consistent button sizing:
   - All .ctrl-btn: padding 6px 12px
   - .maestro-center: padding 10px 32px (larger prominence)

3. Update 06_maestro.py build_control_surface():
   - Regroup buttons following MaestroView pattern
   - Move Matrix to left group
   - Consider Search placement (currently with maestro)

4. Adjust gap values for visual balance:
```python
left_buttons = mo.hstack([...], gap='0.5rem')  # 8px
action_buttons = mo.hstack([...], gap='0.5rem')  # 8px
```

5. Ensure maestro center button stands out:
   - Larger padding maintained
   - Border treatment distinct from ctrl-btn

**Test Strategy:**

1. Visual comparison showing improved rhythm
2. Verify no layout shift on interaction
3. Check alignment at multiple viewport widths
4. Verify full-width behavior unchanged
