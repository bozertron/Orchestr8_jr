---
phase: P07-INTEGRATION
plan: 05
type: execute
wave: 1
depends_on: [P07-PHASE3-PLAN]
files_modified:
  - orchestr8_next/ARCHITECTURE.md
  - orchestr8_next/settings/schema.py
  - orchestr8_next/settings/validators.py
  - FC/FounderConsole_files_for_merge.txt
autonomous: true
user_setup: []

must_haves:
  truths:
    - "ARCHITECTURE.md exists and maps directories to L1-L5 layers"
    - "C7 validator spec delivered with new constraint fields (regex, depends_on, conflicts_with, conditional, deprecated, locked)"
    - "ValidationError dataclass implemented with key, value, constraint, message, severity fields"
    - "19 FC files merged with SettingsService integration"
    - "Tests pass: 68+ tests passing"
  artifacts:
    - path: "orchestr8_next/ARCHITECTURE.md"
      provides: "Directory-to-layer mapping documentation"
      min_lines: 50
    - path: "orchestr8_next/settings/schema.py"
      provides: "SettingConstraint with new fields"
      contains: "regex|depends_on|conflicts_with|conditional|deprecated|locked"
    - path: "orchestr8_next/settings/validators.py"
      provides: "ValidationError dataclass"
      contains: "ValidationError"
    - path: "FC_merged/"
      provides: "19 FC files with SettingsService integration"
  key_links:
    - from: "ARCHITECTURE.md"
      to: "orchestr8_next/shell/"
      via: "documentation mapping shell/ = L2 bus layer"
    - from: "ARCHITECTURE.md"
      to: "orchestr8_next/comms/"
      via: "documentation mapping comms/ = L5 bridge layer"
    - from: "settings/schema.py"
      to: "settings/validators.py"
      via: "ValidationError import"
    - from: "FC files"
      to: "orchestr8_next/settings/service.py"
      via: "SettingsService integration"
---

<objective>
Combined Phase 4-5 execution:
1. Write ARCHITECTURE.md documenting directory-to-layer mapping (Phase 4 - Documentation only, 0.5 hr)
2. Deliver C7 validator spec (BLOCKING per FINAL_RESEARCH_SUMMARY.md Part XX §20.3)
3. Merge 19 FC files with SettingsService integration (Phase 5)

Purpose: Complete remaining integration work per FINAL_RESEARCH_SUMMARY.md roadmap.

Output: ARCHITECTURE.md, updated schema.py with C7 validator spec, 19 FC files merged.
</objective>

<execution_context>
@/home/bozertron/.config/opencode/get-shit-done/workflows/execute-plan.md
@/home/bozertron/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
# From FINAL_RESEARCH_SUMMARY.md Part XVIII:
# - Phase 4: Documentation only (write ARCHITECTURE.md mapping dirs to layers)
# - Phase 5: FC merge - 19 files with SettingsService integration
#
# From Part XX §20.3:
# - C7 validator spec is BLOCKING - deliver this first
#
# CORRECTION: Keep shell/ and comms/ as-is. Document that shell/ = L2 bus layer and comms/ = L5 bridge layer.
# DO NOT rename directories - would break 37+ test imports.
#
# Current SettingConstraint in orchestr8_next/settings/schema.py (L24-45, 78 settings) is missing constraint types:
# - regex: Optional[str] - URL/path format validation
# - depends_on: Optional[str] - Conditional activation
# - conflicts_with: Optional[List[str]] - Mutual exclusion
# - conditional: Optional[Dict] - Conditional constraints
# - deprecated: bool - Sunset marking
# - locked: bool - Immutable VTL-derived tokens

@.planning/orchestr8_next/artifacts/P07/integration/FINAL_RESEARCH_SUMMARY.md
@.planning/orchestr8_next/artifacts/P07/plans/P07-PHASE3-PLAN.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Write ARCHITECTURE.md documenting directory-to-layer mapping</name>
  <files>orchestr8_next/ARCHITECTURE.md</files>
  <action>
    Create orchestr8_next/ARCHITECTURE.md with the following structure:

    ```markdown
    # Orchestr8 Architecture

    ## Five-Layer Architecture (L1-L5)

    | Layer | Name | Directory | Purpose |
    |-------|------|----------|---------|
    | L1 | Presentation Shell | `IP/plugins/` | Marimo UI contracts, renders canonical layout, emits typed actions only |
    | L2 | Action Bus + Store | `orchestr8_next/shell/` | Single source of truth for state transitions, deterministic command routing |
    | L3 | Service Adapter Layer | `orchestr8_next/services/`, `orchestr8_next/adapters/` | Normalizes external systems behind stable interfaces |
    | L4 | Visualization Layer | `orchestr8_next/visualization/` | 3D Code City rendering, node and connection interactions |
    | L5 | Bridge Layer | `orchestr8_next/comms/` | Capability slices, external orchestration integration |

    ## Directory Mapping

    ### IP/ (L1 - Presentation Shell)
    - `IP/plugins/` - Marimo plugin files (06_maestro.py, 07_settings.py, etc.)
    - `IP/styles/` - CSS and visual tokens
    - `IP/static/` - Static assets (JavaScript, fonts)
    - `IP/contracts/` - Validation contracts

    ### orchestr8_next/shell/ (L2 - Action Bus + Store)
    - `shell/facades/` - L2 facade modules wrapping L3 services
    - `shell/store.py` - Redux-style state store
    - `shell/reducer.py` - State reducers

    ### orchestr8_next/city/ (L3 - Domain Services)
    - `city/health/` - Health checking services
    - `city/combat/` - Combat tracking services
    - `city/terminal/` - Terminal spawning services
    - `city/context/` - Contextualization services
    - `city/viz/` - Visualization services

    ### orchestr8_next/visualization/ (L4 - Visualization)
    - 3D Code City rendering
    - Node and connection interactions

    ### orchestr8_next/comms/ (L5 - Bridge Layer)
    - External orchestration integration
    - Capability slices

    ## Layer Contracts

    ### L1 → L2: Facade Pattern
    Plugins (L1) MUST import from `shell/facades/` (L2), NOT directly from L3 services.

    ### L2 → L3: Facade Wrapper Pattern
    Facades wrap L3 services, providing lazy initialization and unified interfaces.

    ### L3 → L4/L5: Service Consumption
    Domain services consume visualization and bridge capabilities through typed contracts.

    ## Important Notes

    - DO NOT rename `shell/` to `bus/` - would break 37+ test imports
    - DO NOT rename `comms/` to `bridge/` - would break 37+ test imports
    - Use this ARCHITECTURE.md to document layer boundaries instead of directory renames
    ```

    IMPORTANT: Do NOT include directory renames. Per §18.3 CORRECTION 3, renames would break all existing imports.
  </action>
  <verify>
    wc -l orchestr8_next/ARCHITECTURE.md
    grep -c "L1\|L2\|L3\|L4\|L5" orchestr8_next/ARCHITECTURE.md
  </verify>
  <done>
    ARCHITECTURE.md exists with 50+ lines, documents all 5 layers and directory mappings.
  </done>
</task>

<task type="auto">
  <name>Task 2: Deliver C7 validator spec - extend SettingConstraint</name>
  <files>
    orchestr8_next/settings/schema.py
    orchestr8_next/settings/validators.py
  </files>
  <action>
    Update orchestr8_next/settings/schema.py to add new constraint fields to SettingConstraint:

    1. Add new fields to SettingConstraint dataclass (around line 24-45):
    ```python
    @dataclass
    class SettingConstraint:
        key: str
        setting_type: SettingType
        default: Any
        description: str
        required: bool = False
        min_value: Optional[float] = None
        max_value: Optional[float] = None
        options: Optional[List[Any]] = None
        # NEW C7 FIELDS:
        regex: Optional[str] = None  # URL/path format validation (e.g. "^bolt://.*:\d+")
        depends_on: Optional[str] = None  # Conditional activation (e.g. "senses.enabled")
        conflicts_with: Optional[List[str]] = None  # Mutual exclusion (encrypt ↔ log_messages)
        conditional: Optional[Dict] = None  # Conditional constraints ({"when": "batch_processing", "is": True})
        deprecated: bool = False  # Sunset marking
        locked: bool = False  # Immutable VTL-derived tokens
    ```

    2. Create orchestr8_next/settings/validators.py with ValidationError dataclass:
    ```python
    """Validators for settings constraints."""
    
    from dataclasses import dataclass
    from typing import Any, List, Optional, Dict
    
    
    @dataclass
    class ValidationError:
        """Validation error with full context."""
        key: str  # Setting that failed
        value: Any  # Value attempted
        constraint: str  # Which constraint failed
        message: str  # Human-readable error
        severity: str  # "error" | "warning" | "info"
    
    
    def validate_regex(value: str, pattern: str) -> bool:
        """Validate value against regex pattern."""
        import re
        return bool(re.match(pattern, value))
    
    
    def validate_depends_on(value: Any, dependency_key: str, settings: Dict) -> bool:
        """Check if dependency is satisfied."""
        # Implementation checks if dependency_key is truthy in settings
        return bool(settings.get(dependency_key))
    
    
    def validate_conflicts(value: Any, conflict_keys: List[str], settings: Dict) -> bool:
        """Check for conflicts with other settings."""
        for key in conflict_keys:
            if settings.get(key) is not None:
                return False
        return True
    
    
    def validate_conditional(value: Any, condition: Dict, settings: Dict) -> bool:
        """Validate conditional constraint."""
        when_key = condition.get("when")
        expected = condition.get("is")
        actual = settings.get(when_key)
        return actual == expected
    ```

    This implements the BLOCKING C7 validator spec from §20.3.
  </action>
  <verify>
    python -c "
    from orchestr8_next.settings.schema import SettingConstraint
    from orchestr8_next.settings.validators import ValidationError

    # Check new fields exist
    import inspect
    fields = [f.name for f in SettingConstraint.__dataclass_fields__.values()]
    required = ['regex', 'depends_on', 'conflicts_with', 'conditional', 'deprecated', 'locked']
    for r in required:
        assert r in fields, f'Missing field: {r}'
    
    print('C7 validator spec: All new fields present')
    print(f'VealidationError: {ValidationError.__dataclass_fields__.keys()}')
    "
  </verify>
  <done>
    SettingConstraint has all 6 new fields (regex, depends_on, conflicts_with, conditional, deprecated, locked).
    ValidationError dataclass implemented with key, value, constraint, message, severity.
  </done>
</task>

<task type="auto">
  <name>Task 3: Discover and audit FC files for merge manifest</name>
  <files>FC manifest</files>
  <action>
    BEFORE merging any FC files, we need to know EXACTLY what exists.

    1. Find the Founder Console source:
    ```bash
    find /home/bozertron -maxdepth 2 -type d -iname "*founder*" -o -iname "*FC*" -o -iname "or8_founder*" 2>/dev/null
    ls -la /home/bozertron/or8_founder_console/ 2>/dev/null || echo "NOT FOUND"
    ```

    2. List all Python files:
    ```bash
    find /home/bozertron/or8_founder_console/ -name "*.py" -type f 2>/dev/null | sort
    ```

    3. Find hardcoded config values in each file:
    ```bash
    grep -rn "hardcoded\|API_KEY\|localhost\|127.0.0.1\|/home/\|\.env" \
      --include="*.py" /home/bozertron/or8_founder_console/ 2>/dev/null
    ```

    4. Create extraction manifest at:
    `.planning/orchestr8_next/artifacts/P07/plans/FC_EXTRACTION_MANIFEST.md`

    The manifest MUST contain for each file:
    | Source Path | Target Path in a_codex_plan | Layer (L1-L5) | Settings Keys Needed | Hardcoded Values to Replace |

    This manifest must be REVIEWED before Task 4 executes.
  </action>
  <verify>
    cat .planning/orchestr8_next/artifacts/P07/plans/FC_EXTRACTION_MANIFEST.md | head -20
    # Should show table with file paths, target layers, and settings keys
  </verify>
  <done>FC_EXTRACTION_MANIFEST.md created with complete file-by-file migration plan.</done>
</task>

<task type="gated">
  <name>Task 4: GATE — Review FC extraction manifest before proceeding</name>
  <files>FC_EXTRACTION_MANIFEST.md</files>
  <action>
    STOP HERE. Review FC_EXTRACTION_MANIFEST.md before continuing.

    Verify:
    - All 19 files are listed with source + target paths
    - Each file has its layer assignment (L1-L5)
    - All hardcoded values that need SettingsService are identified
    - No files conflict with existing a_codex_plan modules

    Only proceed to Task 5 after manifest is verified.
  </action>
  <verify>Manifest reviewed and approved</verify>
  <done>FC extraction manifest approved. Ready to execute merge.</done>
</task>

<task type="auto">
  <name>Task 5: Execute FC merge per manifest</name>
  <files>Per FC_EXTRACTION_MANIFEST.md</files>
  <action>
    For each file in FC_EXTRACTION_MANIFEST.md:

    1. Copy file to target path in a_codex_plan
    2. Replace hardcoded values with SettingsService calls:
       ```python
       # Pattern for each replacement:
       from orchestr8_next.settings.service import SettingsService
       _settings = SettingsService()
       VALUE = _settings.get_setting("section.key", fallback="original_hardcoded_value")
       ```
    3. Update imports to use a_codex_plan package structure
    4. Add any new settings keys to orchestr8_next/settings/schema.py

    After ALL files are merged:
    ```bash
    cd /home/bozertron/a_codex_plan
    python -m pytest tests/ -q 2>&1 | tail -10
    ```
  </action>
  <verify>
    - All files from manifest exist at target paths
    - grep -rn "hardcoded" merged files returns no matches
    - python -m pytest tests/ -q passes (37+ existing + new tests)
  </verify>
  <done>19 FC files merged with SettingsService integration. All tests pass.</done>
</task>

<task type="auto">
  <name>Task 4: Verify all tests pass (68+ target)</name>
  <files>tests/</files>
  <action>
    Run the test suite to verify all phases are complete:

    ```bash
    cd /home/bozertron/Orchestr8_jr
    python -m pytest tests/ -v --tb=short 2>&1 | tail -30
    ```

    Target: 68+ tests passing

    If tests fail:
    1. Check which phase introduced the failure
    2. Fix the issue in the relevant file
    3. Re-run tests

    Key areas to verify:
    - orchestr8_next/shell/facades/ - All 10 facades import correctly
    - orchestr8_next/settings/ - Schema and validators work
    - FC_merged/ - Files integrate correctly
  </action>
  <verify>
    python -m pytest tests/ -q 2>&1 | tail -10
  </verify>
  <done>
    68+ tests passing. All phases complete.
  </done>
</task>

</tasks>

<verification>
- [ ] ARCHITECTURE.md exists with 50+ lines
- [ ] ARCHITECTURE.md maps shell/ to L2, comms/ to L5
- [ ] SettingConstraint has all 6 new C7 fields
- [ ] ValidationError dataclass implemented
- [ ] FC_EXTRACTION_MANIFEST.md exists with 19 files listed
- [ ] FC extraction manifest reviewed and approved (GATE)
- [ ] 19 FC files merged with SettingsService at target paths
- [ ] 68+ tests passing
</verification>

<success_criteria>
Combined Phase 4-5 complete:

1. ARCHITECTURE.md documentation written (per §18.3 CORRECTION 3 - no renames)
2. C7 validator spec delivered (per §20.3 - BLOCKING dependency)
3. FC_EXTRACTION_MANIFEST.md created and reviewed (GATED)
4. 19 FC files merged with SettingsService integration per manifest
5. 68+ tests passing

Total execution time estimate: 3-4 hours (includes discovery + gate review)
</success_criteria>

<output>
After completion, create `.planning/orchestr8_next/artifacts/P07/plans/P07-PHASE45-SUMMARY.md`
</output>
