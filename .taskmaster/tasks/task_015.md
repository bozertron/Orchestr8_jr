# Task ID: 15

**Title:** CSS Browser Compatibility Audit and Source-Level Fixes

**Status:** pending

**Dependencies:** 11, 12

**Priority:** high

**Description:** Perform comprehensive CSS syntax audit across orchestr8.css and any inline styles for browser-incompatible features. Apply source-level fixes for unsupported syntax, not just runtime suppression.

**Details:**

1. Audit for known problematic patterns (from CLAUDE.md ledger):
   - @source directive (Tailwind-specific)
   - @container style(...) queries
   - Nested child selectors without proper syntax
   - ::-webkit-scrollbar-thumb:hover vendor prefixes without fallback
   - text-wrap property (limited support)
   - -moz-osx-font-smoothing (Firefox-only)
   - -webkit-text-size-adjust (Safari-only)
   - break-after, orphans, widows (print-focused)

2. Check orchestr8.css for:
   - Invalid at-rules
   - Unsupported pseudo-elements
   - Malformed selectors

3. Apply fixes:
```css
/* BEFORE (problematic) */
.container {
    text-wrap: balance;  /* Limited support */
}

/* AFTER (compatible) */
.container {
    /* text-wrap: balance; -- Not widely supported */
    overflow-wrap: break-word;
}
```

4. For vendor prefixes, use progressive enhancement:
```css
.element {
    font-smoothing: antialiased;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
```

5. Document all changes in CSS_COMPATIBILITY_FIXES.md

6. Test across Firefox, Chrome, Safari (if available)

**Test Strategy:**

1. Run CSS validator on orchestr8.css
2. Open browser DevTools Console and check for CSS parsing warnings
3. Test in Firefox (primary per CLAUDE.md context)
4. Verify no console warnings from project-owned styles
