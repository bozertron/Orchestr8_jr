---
phase: P07-INTEGRATION
plan: 03
type: execute
wave: 1
depends_on: [P07-PHASE0-PLAN, P07-PHASE1-PLAN]
files_modified:
  - IP/plugins/06_maestro.py
  - IP/plugins/04_connie_ui.py
autonomous: true

must_haves:
  truths:
    - "06_maestro.py uses correct sys.path pointing to IP directory"
    - "04_connie_ui.py uses relative imports for connie module"
    - "08_director.py dynamic discovery unchanged"
    - "All imports resolve correctly"
  artifacts:
    - path: "IP/plugins/06_maestro.py"
      provides: "Path resolution fix"
      line: 53
    - path: "IP/plugins/04_connie_ui.py"
      provides: "Relative import conversion"
      lines: [97, 208, 281]
  key_links:
    - from: "06_maestro.py"
      to: "IP/"
      via: "sys.path.insert(0, str(_THIS_FILE.parent.parent))"
    - from: "04_connie_ui.py"
      to: "IP/connie.py"
      via: "from ..connie import ConversionEngine"
---

<objective>
Fix sys.path hacks across 3 files per FINAL_RESEARCH_SUMMARY.md Part XVIII §18.1 CORRECTION 2.

Purpose: Eliminate brittle absolute path manipulations and use proper relative imports for IP package modules.

Output: All 5 sys.path hack instances resolved (3 corrected, 1 verified, 1 kept as-is).
</objective>

<execution_context>
@/home/bozertron/.config/opencode/get-shit-done/workflows/execute-plan.md
@/home/bozertron/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
@IP/plugins/06_maestro.py (lines 47-53 for current path scope)
@IP/plugins/04_connie_ui.py (lines 97-98, 208-209, 281-282 for connie imports)
@IP/plugins/08_director.py (line 272 for dynamic discovery reference)

# Reference from research

@.planning/orchestr8_next/artifacts/P07/FINAL_RESEARCH_SUMMARY.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Fix sys.path scope in 06_maestro.py</name>
  <files>IP/plugins/06_maestro.py</files>
  <action>
    Fix line 53 to point to IP directory instead of project root:

    Current (line 49):
    ```python
    _PROJECT_ROOT = _THIS_FILE.parent.parent.parent
    ```

    Change to (point to IP directory):
    ```python
    _IP_DIR = _THIS_FILE.parent.parent  # IP/ directory (2 levels up from 06_maestro.py)
    ```

    Then update lines 51-53:
    ```python
    if str(_IP_DIR) not in sys.path:
        sys.path.insert(0, str(_IP_DIR))
    ```

    Also update the error message in lines 59-64 to reflect the change.
  </action>
  <verify>
    Run: python -c "import IP; print('IP package imported successfully')"
    Verify orchestr8.py loads without path errors
  </verify>
  <done>
    06_maestro.py line 53 now resolves to IP directory, not project root.
    sys.path.insert uses _IP_DIR variable.
  </done>
</task>

<task type="auto">
  <name>Task 2: Convert 3 imports in 04_connie_ui.py to relative imports</name>
  <files>IP/plugins/04_connie_ui.py</files>
  <action>
    Replace sys.path hacks with relative imports at 3 locations:

    LOCATION 1 (lines 96-98):
    Current:
    ```python
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from connie import ConversionEngine
    ```
    Replace with:
    ```python
    from ..connie import ConversionEngine
    ```

    LOCATION 2 (lines 207-209):
    Same replacement pattern.

    LOCATION 3 (lines 280-282):
    Same replacement pattern.

    Note: These are inside try/except blocks with fallback to direct sqlite3, so if relative import fails, it will fall back gracefully.
  </action>
  <verify>
    Run: python -c "import importlib; m = importlib.import_module('IP.plugins.04_connie_ui'); print('04_connie_ui imported OK')"
    Or test via: marimo run orchestr8.py - check Connie tab works
  </verify>
  <done>
    All 3 instances in 04_connie_ui.py use relative import: "from ..connie import ConversionEngine"
  </done>
</task>

<task type="auto">
  <name>Task 3: Verify 08_director.py unchanged (dynamic discovery)</name>
  <files>IP/plugins/08_director.py</files>
  <action>
    Verify line 272 remains as-is:

    ```python
    sys.path.insert(0, str(director_root))
    ```

    This is correct because it uses dynamic discovery via _resolve_director_root() to find the director adapter at runtime. This is intentional per CORRECTION 2.
  </action>
  <verify>
    Read line 272 and confirm it contains: sys.path.insert(0, str(director_root))
  </verify>
  <done>
    08_director.py line 272 preserved - dynamic discovery pattern intact.
  </done>
</task>

<task type="auto">
  <name>Task 4: Run verification tests</name>
  <files>IP/plugins/06_maestro.py, IP/plugins/04_connie_ui.py</files>
  <action>
    Execute comprehensive import verification:

    1. Test IP package import:
    ```bash
    python -c "import IP; print('IP package OK')"
    ```

    2. Test orchestr8.py loads:
    ```bash
    timeout 10 python -c "import orchestr8; print('orchestr8 OK')" || echo "Direct import may fail - test via marimo run"
    ```

    3. Test marimo runtime (preferred):
    ```bash
    marimo run orchestr8.py &
    sleep 5
    # Check for import errors in logs
    pkill -f "marimo run"
    ```

    4. Verify no sys.path hacks remain (should return empty for fixed files):
    ```bash
    grep -n "sys.path.insert" IP/plugins/06_maestro.py IP/plugins/04_connie_ui.py || echo "No sys.path hacks found - GOOD"
    ```
  </action>
  <verify>
    All import tests pass, no sys.path.insert in fixed files
  </verify>
  <done>
    All 5 instances verified: 3 fixed, 1 preserved, 1 untouched.
  </done>
</task>

</tasks>

<verification>
- [ ] 06_maestro.py uses _IP_DIR = _THIS_FILE.parent.parent
- [ ] 04_connie_ui.py has no sys.path.insert calls
- [ ] 04_connie_ui.py uses "from ..connie import" at 3 locations
- [ ] 08_director.py line 272 unchanged
- [ ] marimo run orchestr8.py starts without import errors
</verification>

<success_criteria>
All sys.path hacks resolved per CORRECTION 2:

- Fix #1: 06_maestro.py line 53 → uses IP dir (not project root) ✓
- Fix #2: 04_connie_ui.py lines 97, 208, 281 → relative imports ✓
- Fix #3: 08_director.py line 272 → kept as-is ✓
</success_criteria>

<output>
After completion, create `.planning/orchestr8_next/artifacts/P07/plans/P07-PHASE2-SUMMARY.md`
</output>
