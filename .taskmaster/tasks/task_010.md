# Task ID: 10

**Title:** Run canonical constraint acceptance tests

**Status:** done

**Dependencies:** 7 ✓, 8 ✓, 9 ✓

**Priority:** high

**Description:** Verify all canonical constraints remain intact after integration

**Details:**

Manual acceptance testing to verify no canon drift occurred during implementation.

Acceptance checklist:

1. **Naming/UI constraints:**
   - [ ] Top row shows: [orchestr8] [collabor8] [JFDI]
   - [ ] No 'gener8' appears in active canonical frame
   - [ ] App title remains 'Orchestr8 v3.0: The Fortress Factory'

2. **Color constraints:**
   - [ ] Working nodes render in gold (#D4AF37)
   - [ ] Broken nodes render in blue/teal (#1fbdea)
   - [ ] Combat nodes render in purple (#9D4EDD)
   - [ ] Background remains The Void (#0A0A0B)

3. **Motion constraints:**
   - [ ] Code City buildings EMERGE (particles coalesce)
   - [ ] NO breathing/pulsing animations
   - [ ] NO animate-in effects on UI panels
   - [ ] Transitions are instant or emergence-only

4. **State precedence:**
   - [ ] Combat status overrides broken and working
   - [ ] Broken status overrides working
   - [ ] merge_status() is used consistently

5. **Behavioral constraints:**
   - [ ] Clicking broken node opens deploy panel
   - [ ] Clicking working node does NOT open deploy panel
   - [ ] Clicking combat node shows combat status message
   - [ ] All existing plugins still render
   - [ ] No console errors in browser

6. **State wiring:**
   - [ ] STATE_MANAGERS contains health/health_status keys
   - [ ] Root state initialization succeeds
   - [ ] handle_node_click() is invoked on valid clicks

Document any deviations in tests/acceptance_report.md with screenshots if needed.

**Test Strategy:**

Complete all checklist items. Take screenshots of: (1) Top navigation bar, (2) Code City with nodes in all three states, (3) Deploy panel triggered by broken node click, (4) Browser console showing no errors. Accept only if ALL items pass.
