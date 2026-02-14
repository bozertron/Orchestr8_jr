# Task ID: 19

**Title:** MaestroView Button Style Pattern Extraction

**Status:** pending

**Dependencies:** 11, 12

**Priority:** high

**Description:** Extract button styling patterns from MaestroView.vue including border treatments, hover states, active states, and color transitions. Document patterns for Orchestr8 application.

**Details:**

1. Extract .top-btn styles from MaestroView.vue (lines 735-753):
```css
.top-btn {
    padding: 5px 12px;
    border-radius: 4px;
    background: #121214;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: #1fbdea;
    font-family: var(--font-headline);
    font-size: 10px;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 200ms ease-out;
}

.top-btn:hover,
.top-btn.active {
    background: rgba(212, 175, 55, 0.1);
    border-color: #D4AF37;
    color: #D4AF37;
}
```

2. Extract .ctrl-btn styles (lines 1009-1037):
```css
.ctrl-btn {
    padding: 6px 12px;
    background: transparent;
    border: none;
    color: #1fbdea;
    font-family: var(--font-headline);
    font-size: 10px;
    letter-spacing: 0.08em;
    transition: all 150ms ease-out;
}

.ctrl-btn:hover { color: #D4AF37; }
.ctrl-btn.active { color: #D4AF37; }
.ctrl-btn:disabled { opacity: 0.3; cursor: not-allowed; }
```

3. Extract special button variants:
   - .apps-btn: Has background: rgba(31, 189, 234, 0.1)
   - .send-btn: Gold background accent
   - .maestro-center: Border with gold dark, larger padding

4. Create pattern documentation:
   - orchestr8_button_patterns.md
   - Include visual examples (ASCII/description)
   - Note transition timing (150ms vs 200ms)

**Test Strategy:**

1. Side-by-side visual comparison with MaestroView
2. Record hover/active state transitions
3. Verify disabled state appearance
4. Check keyboard focus states
