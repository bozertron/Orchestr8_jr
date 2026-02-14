# Task ID: 17

**Title:** Responsive Layout Pass - Desktop Viewport

**Status:** pending

**Dependencies:** 11, 15

**Priority:** high

**Description:** Ensure Orchestr8 layout renders correctly across desktop viewport sizes (1024px - 2560px width). Focus on top row, VOID center, bottom control surface, and right-side panels.

**Details:**

1. Define breakpoints:
   - Large desktop: 1920px+
   - Standard desktop: 1280px - 1919px
   - Small desktop: 1024px - 1279px

2. Test top row layout:
   - [orchestr8] [collabor8] [JFDI] buttons
   - Verify spacing and alignment at each breakpoint
   - Ensure no overflow/wrapping

3. Test VOID center:
   - Code City visualization sizing
   - Max-width constraints (700px for messages per MaestroView)
   - Padding adjustment for viewport

4. Test bottom control surface:
   - Full-width behavior maintained
   - Button groups stay on single row at desktop widths
   - Chat input scaling

5. Test right-side panels:
   - Ticket, Calendar, Comms, File Explorer panels
   - Fixed width (320px per MaestroView) or percentage?
   - Overlay vs push behavior

6. Add responsive CSS if needed:
```css
@media (min-width: 1920px) {
    .void-center { max-width: 900px; }
    .chat-input-container { max-width: 1100px; }
}

@media (max-width: 1279px) {
    .control-row { gap: 8px; }
    .ctrl-btn { padding: 4px 8px; }
}
```

**Test Strategy:**

1. Resize browser window through breakpoint ranges
2. Use DevTools device toolbar for exact widths
3. Verify no horizontal scrollbar at any tested width
4. Check button text truncation doesn't occur
