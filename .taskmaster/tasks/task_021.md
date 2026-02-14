# Task ID: 21

**Title:** Lower-Fifth Control Surface Rhythm Analysis

**Status:** pending

**Dependencies:** 19

**Priority:** medium

**Description:** Analyze the lower-fifth control surface button layout rhythm from MaestroView.vue. Document spacing, grouping, and visual balance patterns without changing macro geometry.

**Details:**

1. Analyze MaestroView control-surface layout (lines 611-660):
   - Single row layout: Left Group | Center (maestro) | Right Group
   - Left Group: Apps, Matrix, Calendar, Comms, Files
   - Center: maestro button (summon action)
   - Right Group: Search, Record, Playback, Phreak>, Send, Attach

2. Document spacing metrics:
   - .control-row gap: 16px
   - .control-group gap: 8px
   - .maestro-center margin: 0 16px
   - Button padding: 6px 12px

3. Document visual rhythm:
   - Left group: 5 buttons (navigation/utility)
   - Center: 1 prominent maestro button
   - Right group: 6 buttons (actions)
   - Symmetry assessment: Left=5, Right=6 (slight right-heavy)

4. Compare to current Orchestr8 implementation:
   - Current left_buttons: Apps, Calendar*, Comms*, Files (4)
   - Current center: maestro + @maestro state + Search (3 elements)
   - Current action_buttons: Record, Playback, Phreak>, Send, Attach, Settings (6)

5. Identify rhythm improvements:
   - Move Settings out of action_buttons?
   - Balance left/right counts?
   - Maintain current surface width

6. Document in lower_fifth_rhythm_analysis.md

**Test Strategy:**

1. Screenshot comparison of current vs MaestroView layout
2. Measure pixel spacing in DevTools
3. Verify full-width behavior preserved
4. Check wrapping behavior at narrow widths
