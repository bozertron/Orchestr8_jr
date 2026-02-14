# Task ID: 18

**Title:** Responsive Layout Pass - Mobile/Narrow Viewport

**Status:** pending

**Dependencies:** 17

**Priority:** medium

**Description:** Ensure Orchestr8 layout degrades gracefully on narrow viewports (320px - 1023px). Not full mobile redesign, but functional and non-broken display.

**Details:**

1. Define narrow breakpoints:
   - Tablet: 768px - 1023px
   - Large phone: 480px - 767px
   - Phone: 320px - 479px

2. Handle top row at narrow widths:
```css
@media (max-width: 767px) {
    .orchestr8-top-row {
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
    }
}
```

3. Handle control surface wrapping:
```css
@media (max-width: 767px) {
    .control-row {
        flex-direction: column;
        align-items: center;
    }
    .control-group {
        justify-content: center;
    }
    .maestro-center {
        margin: 12px 0;
    }
}
```

4. Handle Code City at narrow widths:
   - Consider hiding 3D view below 480px
   - Show simplified list view or placeholder
   - Maintain touch-friendly tap targets (44px minimum)

5. Handle panels on narrow:
   - Full-width overlays instead of side panels
   - Stack instead of slide behavior

6. Ensure no critical functionality lost:
   - All buttons accessible
   - Chat input usable
   - Error states visible

**Test Strategy:**

1. Use DevTools mobile device presets (iPhone, Galaxy)
2. Physical device testing if available
3. Verify touch targets meet 44px minimum
4. Check no text overflow or clipping
