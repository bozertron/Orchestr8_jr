# Task ID: 20

**Title:** Apply MaestroView Button Styles to Orchestr8

**Status:** pending

**Dependencies:** 19

**Priority:** high

**Description:** Apply extracted button style patterns to orchestr8.css, updating existing .orchestr8-btn and control button classes to match MaestroView visual treatment while preserving marimo button compatibility.

**Details:**

1. Update .orchestr8-btn in orchestr8.css to match .top-btn:
```css
.orchestr8-btn {
    padding: 5px 12px;
    background: var(--bg-elevated);
    border: 1px solid rgba(31, 189, 234, 0.3);
    border-radius: 4px;
    color: var(--blue-dominant);
    font-family: var(--font-headline);
    font-size: 10px;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 200ms ease-out;
}

.orchestr8-btn:hover,
.orchestr8-btn.active {
    background: rgba(212, 175, 55, 0.1);
    border-color: var(--gold-metallic);
    color: var(--gold-metallic);
}
```

2. Update marimo button overrides (lines 301-323):
   - Remove !important where possible
   - Use more specific selectors instead
   - Preserve on_click functionality

3. Add control button variants:
```css
.ctrl-btn-apps {
    background: rgba(31, 189, 234, 0.1);
    border-radius: 4px;
}

.ctrl-btn-send {
    background: rgba(212, 175, 55, 0.15);
    border-radius: 4px;
    color: var(--gold-metallic);
}

.ctrl-btn-send:hover {
    background: rgba(212, 175, 55, 0.25);
    color: var(--gold-saffron);
}
```

4. Ensure marimo mo.ui.button() elements receive correct styles:
   - Check if button classes apply
   - May need [data-marimo-element='button'] selector

**Test Strategy:**

1. Visual comparison with MaestroView reference
2. Click all buttons to verify on_click still fires
3. Check hover/active states in DevTools
4. Verify disabled button appearance
