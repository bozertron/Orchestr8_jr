---
phase: P07-INTEGRATION
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - IP/plugins/06_maestro.py
  - IP/mermaid_theme.py
  - IP/features/maestro/config.py
  - IP/woven_maps.py
  - IP/plugins/components/ticket_panel.py
  - IP/plugins/components/file_explorer_panel.py
  - IP/plugins/components/comms_panel.py
  - IP/plugins/components/calendar_panel.py
  - IP/city/settings_service.py
autonomous: true

must_haves:
  truths:
    - "All hardcoded #B8860B replaced with #C5A028 in Orchestr8_jr"
    - "woven_maps.py uses SettingsService for runtime color tokens"
    - "No legacy #B8860B remains in IP/ Python files"
  artifacts:
    - path: "IP/plugins/06_maestro.py"
      contains: "#C5A028"
      no: "#B8860B"
    - path: "IP/mermaid_theme.py"
      contains: "#C5A028"
      no: "#B8860B"
    - path: "IP/features/maestro/config.py"
      contains: "#C5A028"
      no: "#B8860B"
    - path: "IP/woven_maps.py"
      contains: "SettingsService"
      no: "#B8860B"
    - path: "IP/plugins/components/ticket_panel.py"
      contains: "#C5A028"
      no: "#B8860B"
    - path: "IP/plugins/components/file_explorer_panel.py"
      contains: "#C5A028"
      no: "#B8860B"
    - path: "IP/plugins/components/comms_panel.py"
      contains: "#C5A028"
      no: "#B8860B"
    - path: "IP/plugins/components/calendar_panel.py"
      contains: "#C5A028"
      no: "#B8860B"
  key_links:
    - from: "IP/woven_maps.py"
      to: "IP/city/settings_service.py"
      via: "import and COLOR_TOKENS dict"
---

<objective>
Fix color token drift (#B8860B → #C5A028) across Orchestr8_jr and wire woven_maps.py to SettingsService for runtime tokens.

Purpose: Establish visual token compliance with VISUAL_TOKEN_LOCK.md and prevent future drift by consuming tokens from SettingsService at runtime.

Output: All 8 files fixed, SettingsService integration complete.
</objective>

<execution_context>
@/home/bozertron/.config/opencode/get-shit-done/workflows/execute-plan.md
@/home/bozertron/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
@SOT/VISUAL_TOKEN_LOCK.md
# VISUAL_TOKEN_LOCK.md defines locked color tokens:
# --gold-dark: #C5A028 (locked value - replaces legacy #B8860B)
# --gold-light: #F4C430
# --teal: #00E5E5
# --state-working: #D4AF37
# --state-broken: #1fbdea
# --state-combat: #9D4EDD

@.planning/orchestr8_next/artifacts/P07/integration/FINAL_RESEARCH_SUMMARY.md

# Section 6.2 documents the #B8860B drift (8 files, 11 instances)

# Section 20.1 mentions Bootstrap violations in orchestr8_next (predictive - files don't exist yet)

@IP/city/settings_service.py

# CitySettingsService provides COLOR_TOKENS dict with locked values

# Includes: --gold-dark: #C5A028, --state-working: #D4AF37, etc

</context>

<tasks>

<task type="auto">
  <name>Task 1: Fix #B8860B drift in IP/plugins/06_maestro.py</name>
  <files>IP/plugins/06_maestro.py</files>
  <action>
    Replace all instances of #B8860B with #C5A028 in IP/plugins/06_maestro.py.
    Line 20 contains: `--gold-dark: #B8860B (Maestro default)` - change to `#C5A028`.
    Use: sed -i 's/#B8860B/#C5A028/g' IP/plugins/06_maestro.py
  </action>
  <verify>grep -n "#B8860B" IP/plugins/06_maestro.py returns no matches; grep -n "#C5A028" IP/plugins/06_maestro.py returns matches</verify>
  <done>IP/plugins/06_maestro.py contains #C5A028 and no #B8860B</done>
</task>

<task type="auto">
  <name>Task 2: Fix #B8860B drift in IP/mermaid_theme.py</name>
  <files>IP/mermaid_theme.py</files>
  <action>
    Replace all instances of #B8860B with #C5A028 in IP/mermaid_theme.py.
    Lines 4, 7, 8, 11 contain hardcoded #B8860B for stroke colors.
    Use: sed -i 's/#B8860B/#C5A028/g' IP/mermaid_theme.py
  </action>
  <verify>grep -n "#B8860B" IP/mermaid_theme.py returns no matches; grep -n "#C5A028" IP/mermaid_theme.py returns matches</verify>
  <done>IP/mermaid_theme.py contains #C5A028 and no #B8860B</done>
</task>

<task type="auto">
  <name>Task 3: Fix #B8860B drift in IP/features/maestro/config.py</name>
  <files>IP/features/maestro/config.py</files>
  <action>
    Replace #B8860B with #C5A028 in IP/features/maestro/config.py.
    Line 17 contains the legacy color value.
    Use: sed -i 's/#B8860B/#C5A028/g' IP/features/maestro/config.py
  </action>
  <verify>grep -n "#B8860B" IP/features/maestro/config.py returns no matches</verify>
  <done>IP/features/maestro/config.py contains #C5A028 and no #B8860B</done>
</task>

<task type="auto">
  <name>Task 4: Fix #B8860B drift + wire to SettingsService in IP/woven_maps.py</name>
  <files>IP/woven_maps.py</files>
  <action>
    1. Replace hardcoded #B8860B with #C5A028 on line 62 in COLORS dict.
    2. Import CitySettingsService to use runtime tokens:
       - Add import: from IP.city.settings_service import COLOR_TOKENS
       - Modify COLORS dict to reference COLOR_TOKENS instead of hardcoded values
       - Example: "gold_dark": COLOR_TOKENS.get("--gold-dark", "#C5A028")

    The COLORS dict (lines 56-64) should use SettingsService tokens:
    ```python
    from IP.city.settings_service import COLOR_TOKENS
    
    COLORS = {
        "gold_metallic": COLOR_TOKENS.get("--state-working", "#D4AF37"),
        "blue_dominant": COLOR_TOKENS.get("--state-broken", "#1fbdea"),
        "purple_combat": COLOR_TOKENS.get("--state-combat", "#9D4EDD"),
        "bg_primary": COLOR_TOKENS.get("--bg-obsidian", "#050505"),
        "bg_elevated": "#121214",  # Keep - not in VTL
        "gold_dark": COLOR_TOKENS.get("--gold-dark", "#C5A028"),
        "gold_saffron": COLOR_TOKENS.get("--gold-light", "#F4C430"),
    }
    ```
  </action>
  <verify>
    - grep -n "#B8860B" IP/woven_maps.py returns no matches
    - grep -n "from IP.city.settings_service import" IP/woven_maps.py returns match
    - grep -n "COLOR_TOKENS" IP/woven_maps.py returns matches
  </verify>
  <done>IP/woven_maps.py uses SettingsService COLOR_TOKENS, no #B8860B remains</done>
</task>

<task type="auto">
  <name>Task 5: Fix #B8860B drift in IP/plugins/components/ticket_panel.py</name>
  <files>IP/plugins/components/ticket_panel.py</files>
  <action>
    Replace #B8860B with #C5A028 in IP/plugins/components/ticket_panel.py.
    Line 11 contains the legacy value.
    Use: sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/ticket_panel.py
  </action>
  <verify>grep -n "#B8860B" IP/plugins/components/ticket_panel.py returns no matches</verify>
  <done>ticket_panel.py contains #C5A028</done>
</task>

<task type="auto">
  <name>Task 6: Fix #B8860B drift in IP/plugins/components/file_explorer_panel.py</name>
  <files>IP/plugins/components/file_explorer_panel.py</files>
  <action>
    Replace #B8860B with #C5A028 in IP/plugins/components/file_explorer_panel.py.
    Line 15 contains the legacy value.
    Use: sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/file_explorer_panel.py
  </action>
  <verify>grep -n "#B8860B" IP/plugins/components/file_explorer_panel.py returns no matches</verify>
  <done>file_explorer_panel.py contains #C5A028</done>
</task>

<task type="auto">
  <name>Task 7: Fix #B8860B drift in IP/plugins/components/comms_panel.py</name>
  <files>IP/plugins/components/comms_panel.py</files>
  <action>
    Replace #B8860B with #C5A028 in IP/plugins/components/comms_panel.py.
    Line 27 contains the legacy value.
    Use: sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/comms_panel.py
  </action>
  <verify>grep -n "#B8860B" IP/plugins/components/comms_panel.py returns no matches</verify>
  <done>comms_panel.py contains #C5A028</done>
</task>

<task type="auto">
  <name>Task 8: Fix #B8860B drift in IP/plugins/components/calendar_panel.py</name>
  <files>IP/plugins/components/calendar_panel.py</files>
  <action>
    Replace #B8860B with #C5A028 in IP/plugins/components/calendar_panel.py.
    Line 28 contains the legacy value.
    Use: sed -i 's/#B8860B/#C5A028/g' IP/plugins/components/calendar_panel.py
  </action>
  <verify>grep -n "#B8860B" IP/plugins/components/calendar_panel.py returns no matches</verify>
  <done>calendar_panel.py contains #C5A028</done>
</task>

<task type="auto">
  <name>Task 9: Verify no #B8860B remains in IP/</name>
  <files>IP/</files>
  <action>
    Run comprehensive grep to confirm no #B8860B remains in any Python file:
    grep -r "#B8860B" --include="*.py" IP/

    This should return no matches after all fixes are applied.
  </action>
  <verify>grep -r "#B8860B" --include="*.py" IP/ returns empty (no matches)</verify>
  <done>Zero #B8860B instances remain in IP/ directory</done>
</task>

<task type="auto">
  <name>Task 10: Fix 27 VTL violations in a_codex_plan (2ndFid audit - Part XX)</name>
  <files>/home/bozertron/a_codex_plan/</files>
  <action>
    The 2ndFid audit (Part XX §20.1) found 27 additional VTL violations in a_codex_plan.
    These are Bootstrap colors that violate VISUAL_TOKEN_LOCK.md.

    1. Find all violations:
    ```bash
    cd /home/bozertron/a_codex_plan
    grep -rn "#B8860B\|#007bff\|#28a745\|#dc3545\|#ffc107\|#17a2b8\|#6c757d" \
      --include="*.py" --include="*.css" --include="*.html" \
      orchestr8_next/ tests/ lib/ scripts/
    ```

    2. Replace Bootstrap colors with VTL equivalents:
    - #007bff (Bootstrap blue) → #1fbdea (--state-broken / teal family)
    - #28a745 (Bootstrap green) → #D4AF37 (--state-working)
    - #dc3545 (Bootstrap red) → #9D4EDD (--state-combat) or remove
    - #ffc107 (Bootstrap yellow) → #F4C430 (--gold-light)
    - #17a2b8 (Bootstrap cyan) → #00E5E5 (--teal)
    - #6c757d (Bootstrap gray) → #CCC (--text-grey)
    - #B8860B → #C5A028 (same fix as Orchestr8_jr)

    3. Apply fixes per file using sed or manual edit.

    Target: 12 files, 38 instances total across a_codex_plan.
  </action>
  <verify>
    grep -rn "#B8860B\|#007bff\|#28a745\|#dc3545\|#ffc107\|#17a2b8\|#6c757d" \
      --include="*.py" --include="*.css" --include="*.html" \
      /home/bozertron/a_codex_plan/orchestr8_next/ /home/bozertron/a_codex_plan/tests/ \
      returns empty (no matches)
  </verify>
  <done>All 38 VTL violations in a_codex_plan fixed. Zero Bootstrap colors remain.</done>
</task>

</tasks>

<verification>
1. All 8 Orchestr8_jr files modified with #C5A028
2. IP/woven_maps.py imports and uses SettingsService COLOR_TOKENS
3. grep -r "#B8860B" --include="*.py" IP/ returns zero matches
4. All 12 a_codex_plan files fixed (38 Bootstrap/VTL violations)
5. All changes match VISUAL_TOKEN_LOCK.md exactly
</verification>

<success_criteria>

- All 8 Orchestr8_jr files with #B8860B drift fixed (11 instances)
- All 12 a_codex_plan files with Bootstrap color drift fixed (27 instances)
- IP/woven_maps.py wired to SettingsService for runtime color tokens
- No hardcoded #B8860B or Bootstrap colors remain in either codebase
- Color tokens match VISUAL_TOKEN_LOCK.md: --gold-dark: #C5A028
- Total: 38 violations fixed across both codebases
</success_criteria>

<output>
After completion, create `.planning/orchestr8_next/artifacts/P07/plans/P07-PHASE0-PLAN-01-SUMMARY.md`
</output>
