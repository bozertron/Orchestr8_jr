# Task ID: 12

**Title:** Typography CSS Variable Definition and Font Stack Audit

**Status:** pending

**Dependencies:** 11

**Priority:** high

**Description:** Define and normalize typography CSS variables following MaestroView.vue font-family patterns. Establish --font-headline, --font-body, and --font-mono variables in orchestr8.css with appropriate fallback stacks.

**Details:**

1. Extract font-family patterns from MaestroView.vue:
   - var(--font-headline) - used for buttons, titles
   - var(--font-body) - used for chat input, message content
   - var(--font-mono) - used for timestamps, code

2. Update IP/styles/orchestr8.css :root block:
```css
:root {
    /* Typography - Orchestr8 Font System */
    --font-headline: 'Cal Sans', 'JetBrains Mono', 'IBM Plex Mono', monospace;
    --font-body: 'IBM Plex Sans', 'Inter', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', 'IBM Plex Mono', 'Fira Code', monospace;
    
    /* Override existing --font-ui */
    --font-ui: var(--font-mono);
}
```

3. Audit current typography usage:
   - .orchestr8-brand uses font-family: monospace
   - .orchestr8-btn uses font-family: monospace
   - Replace direct 'monospace' with var(--font-mono)

4. Update button and control element font declarations:
   - .top-btn -> var(--font-headline)
   - .ctrl-btn -> var(--font-headline)
   - .chat-input -> var(--font-body)
   - .message-content -> var(--font-body)
   - .message-time -> var(--font-mono)

5. Ensure letter-spacing values match MaestroView.vue:
   - Headlines: 0.08em - 0.1em
   - Body: normal
   - Mono/times: inherit

**Test Strategy:**

1. Inspect rendered fonts in browser DevTools
2. Verify font-family inheritance chain works
3. Check fallback fonts render correctly when primary unavailable
4. Visual comparison of button text against MaestroView reference
