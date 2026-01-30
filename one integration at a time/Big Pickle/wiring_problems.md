# Orchestr8 Wiring Problems Audit

## Directory: `IP/plugins/` (Audit Date: 2026-01-25)

This audit focuses on the plugin architecture used in `IP/orchestr8_app.py` (v3.0). It identifies disconnected UI elements, hollow integrations, and architectural fragility.

### 1. Architectural Fragility: `sys.path` Manipulation

**Pattern:** Using `sys.path.insert` to resolve imports for sibling or parent directories.

- **File:** `IP/plugins/04_connie_ui.py` (Line 97-98)
- **File:** `IP/plugins/08_director.py` (Line 208-209)
- **Integration Point:** Importing `connie.py` and `888/director/`.
- **Snippet:**

  ```python
  sys.path.insert(0, str(Path(__file__).parent.parent))
  from connie import ConversionEngine
  ```

- **Problem:** Brittle path resolution. If the app is run from a different CWD or if files are moved, these imports will fail. It circumvents standard Python package management.

### 2. Hollow Integration: `CarlContextualizer`

**Pattern:** Importing a core component but only using it for display-only JSON blobs.

- **File:** `IP/plugins/02_explorer.py` (Line 141-151)
- **Integration Point:** `carl_core.CarlContextualizer`
- **Snippet:**

  ```python
  try:
      from carl_core import CarlContextualizer
      carl = CarlContextualizer(root)
      context = carl.run_deep_scan()
      set_scan_result(context)
  except ImportError:
      pass
  ```

- **Problem:** `CarlContextualizer` is a major architectural piece, but here its output is just dumped into a preview panel. It doesn't influence the `Files` state or provide intelligent filtering/selection elsewhere in the app.

### 3. One-Way State: Generator Phase Locking

**Pattern:** Exporting state to a file but failing to initialize from that file.

- **File:** `IP/plugins/01_generator.py` (Line 44-53, 239-251)
- **Integration Point:** `BUILD_SPEC.json`
- **Problem:** The `export_spec` function includes `locked_phases` in the metadata. However, the `render` function initializes `get_locked` to `[]` every time. There is no logic to check if a `BUILD_SPEC.json` exists and restore the locked phases, making the "Lock Phase" feature transient.

### 4. Placeholder UI: Maestro "Coming Soon" Panels

**Pattern:** UI overlays exist but contain static "coming soon" text.

- **File:** `IP/plugins/06_maestro.py` (Line 691-757)
- **Integration Points:**
  - `Collabor8` (Agents Panel)
  - `JFDI` (Tasks Panel)
  - `Summon` (Global Search)
- **Snippet:**

  ```python
  if get_show_agents():
      agents_panel = mo.Html(f"""
      <div class="panel-overlay">
          <span class="panel-title">COLLABOR8 - Domain Agents</span>
          <div>Agent management interface coming soon.</div>
      </div>
      """)
  ```

- **Problem:** These are "Hollow Components" - the buttons toggle them, the CSS animates them, but they have no functional wiring to actual agents or task managers.

### 5. Dangling UI Actions: Maestro Control Surface

**Pattern:** Buttons with `on_change` lambdas that only log actions to the console.

- **File:** `IP/plugins/06_maestro.py` (Line 558, 811, 815, 819)
- **Integration Points:**
  - `Gener8` Button (Navigation)
  - `Apps` Button (Control Surface)
  - `Matrix` Button (Control Surface)
  - `Files` Button (Control Surface)
- **Snippet:**

  ```python
  mo.ui.button(label="Gener8", on_change=lambda _: log_action("Switch to Generator tab"))
  ```

- **Problem:** These buttons should trigger tab switches or open specific panels, but they are currently dead-ends that only provide log feedback.

### 6. Missing Re-Scan Logic: Gatekeeper Folder Management

**Pattern:** Adding data to configuration but lacking UI for removal or verified state refresh.

- **File:** `IP/plugins/03_gatekeeper.py` (Line 252)
- **Integration Point:** `LouisConfig`
- **Problem:** Users can add folders to protection, but the UI lacks a mechanism to remove them ("Note: Can't easily add remove buttons inline in MD"). Additionally, if files are locked/unlocked outside the app, the UI doesn't automatically detect the change unless a manual "Rescan Files" is clicked.

### 7. Fragile Fallback: Connie PDF/SQL Rendering

**Pattern:** Fallback logic that assumes secondary dependencies are present.

- **File:** `IP/plugins/04_connie_ui.py` (Line 147-158)
- **Integration Point:** `pandas` / `sqlite3`
- **Problem:** If `ConversionEngine` (from `connie.py`) fails to import, it falls back to raw `sqlite3` and `pandas`. However, if `pandas` itself is missing or if the table is extremely large, the `mo.md(preview_df.to_markdown())` call will likely crash or hang the cell.

### 8. Async Disconnect: Director Monitoring

**Pattern:** Background threads updating local state without a Marimo refresh trigger.

- **File:** `IP/plugins/08_director.py` (Line 239-247)
- **Integration Point:** `DirectorIntegration._monitor_loop`
- **Problem:** The monitor loop runs in a background thread and updates `self.generals`. However, Marimo's reactive state (`mo.state`) usually requires a setter call FROM A CELL to trigger a UI update. Updates inside a `threading.Thread` to a standard class attribute will not be reflected in the UI until the user interacts with another element or manually refreshes.

---
**Next Target:** `IP/` (Core logic and base classes)

## Directory: `IP/` (Audit Date: 2026-01-25)

This audit identifies problems in the core system modules that provide the logic for the plugins.

### 9. Incomplete Logic: Briefing Campaign History

**Pattern:** Placeholder comments in core logic that return empty results.

- **File:** `IP/briefing_generator.py` (Line 18-21)
- **Integration Point:** `BRIEFING.md` generation.
- **Snippet:**

  ```python
  # Parse markdown entries (simplified - would need proper parser)
  entries = []
  # ... parsing logic ...
  return entries[-limit:]
  ```

- **Problem:** The `load_campaign_log` function is a stub. It will always return an empty list, meaning the "Recent Campaign History" section in every generated briefing will be empty, losing valuable context for the LLM.

### 10. Platform & Tool Chain Assumptions

**Pattern:** Hardcoded commands or binaries that may not exist on the host system.

- **File:** `IP/terminal_spawner.py` (Line 73-87)
- **File:** `IP/briefing_generator.py` (Line 154)
- **Integration Points:** Terminal spawning and Health Check snippets.
- **Problem:** `terminal_spawner.py` prioritizes `gnome-terminal`, which is not universal on Linux. `briefing_generator.py` hardcodes `npm run typecheck` into the `BRIEFING.md` checklist, which is inappropriate for Python-only projects.

### 11. Un-Synchronized Mission State

**Pattern:** Multiple managers (Tickets, Combat, Briefings) operating on the same entity ("fiefdom") without a unified record.

- **File:** `IP/ticket_manager.py`
- **File:** `IP/combat_tracker.py`
- **File:** `IP/briefing_generator.py`
- **Problem:** A "Mission" involves a Ticket, a Briefing, and an active Combat deployment. However, these three systems are siloed. Creating a ticket does not trigger a briefing; spawning a terminal marks "Combat" but doesn't link back to the Ticket ID effectively in the tracker state.

### 12. Manual State Cleanup

**Pattern:** Reliance on manual triggers or external calls to clean up persistent state.

- **File:** `IP/combat_tracker.py` (Line 60-75)
- **Integration Point:** `.orchestr8/combat_state.json`
- **Problem:** `cleanup_stale_deployments` must be called explicitly. If the app crashes or is closed, "Combat" status (Purple) will persist indefinitely on files until a manual cleanup is triggered, leading to a "ghost in the machine" UI where files look active but aren't.

### 13. Brittle Alias Resolution

**Pattern:** Hardcoded path mappings for project-specific aliases.

- **File:** `IP/connection_verifier.py` (Line 356-359)
- **Integration Point:** JS/TS Import Resolution.
- **Snippet:**

  ```python
  if import_path.startswith('@/') or import_path.startswith('~/'):
      alias_path = import_path[2:]  # Remove @/ or ~/
      return self._try_resolve_js_file(self.project_root / 'src' / alias_path, source_file)
  ```

- **Problem:** Assumes `@/` always maps to `src/`. This will fail for projects using different alias configurations (e.g., `@core/`, `@ui/`) or different root directories.

### 14. Detection vs. Support Gap: Health Checkers

**Pattern:** Detecting a tool's presence but assuming its configuration is standard.

- **File:** `IP/health_checker.py` (Line 77-79)
- **Integration Point:** `npm run typecheck`
- **Problem:** The checker detects `package.json` and `npm` and assumes `typecheck` is a valid script. If the project uses a different script name (e.g., `npm run check`) or none at all, the health check will fail with a "script not found" error rather than reporting "not supported".

---
**Audit Status:** Methodist Crawl Complete for `IP/` and `IP/plugins/`.
