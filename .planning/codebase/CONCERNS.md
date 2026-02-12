# Codebase Concerns

**Analysis Date:** 2026-01-30

## Tech Debt

**Bare Exception Handling:**
- Issue: Many try-except blocks catch generic `Exception` or use bare `except:` with `pass`, swallowing errors silently and making debugging difficult
- Files: `IP/louis_core.py`, `IP/connection_verifier.py`, `IP/plugins/02_explorer.py`, `IP/plugins/components/calendar_panel.py`, `IP/plugins/components/comms_panel.py`, and many others
- Impact: Silent failures, no logging of actual errors, difficult root cause analysis when systems malfunction
- Fix approach: Replace bare exceptions with specific exception types and proper logging. Replace `except: pass` with explicit error capture and at minimum a log statement

**Loose Dependency on Anthropic SDK:**
- Issue: Chat functionality in `IP/plugins/06_maestro.py` (lines 88-92) gracefully degrades if anthropic not installed, but core functionality depends on environment variable `ANTHROPIC_API_KEY` without validation
- Files: `IP/plugins/06_maestro.py` (handle_send function, lines 753-844)
- Impact: User won't know API key is invalid until they try to send a message; errors appear only in the chat, not as initialization warnings
- Fix approach: Add initialization-time validation of `ANTHROPIC_API_KEY` in `orchestr8.py` entry point; log clear warning if missing before any chat attempt

**Configuration with Placeholder Values:**
- Issue: `pyproject_orchestr8_settings.toml` contains many placeholder values like `[local_doc_model]`, `[path_to_image_model]`, `[neo4j_password]` that are never validated
- Files: `pyproject_orchestr8_settings.toml` (lines 47, 121, 130, 149, 162, 237, etc.)
- Impact: System may silently fail to initialize external services without clear feedback about which configuration values are invalid
- Fix approach: Create config validation module that checks all required paths/credentials exist at startup and reports missing/invalid values

## Known Bugs

**Code City Rendering Failures Not Handled Gracefully:**
- Symptoms: If `build_code_city()` throws exception in `06_maestro.py`, error appears inline in UI but doesn't prevent rest of interface from loading
- Files: `IP/plugins/06_maestro.py` (build_code_city function, lines 917-944)
- Trigger: Invalid project root, permission issues, or corrupted file scan data
- Workaround: Set project root to a valid directory; check `.orchestr8/` subdirectory isn't corrupted

**Panel Mutual Exclusion Logic Inconsistent:**
- Symptoms: Right-side panels (Calendar, Comms, File Explorer) claim mutual exclusion, but toggling between them can leave multiple panels visible
- Files: `IP/plugins/06_maestro.py` (toggle_calendar, toggle_comms, toggle_file_explorer functions, lines 441-485)
- Trigger: Rapid clicking between panel toggle buttons
- Workaround: Click "Home" button to reset all panels to closed state

**Terminal Spawning Assumes OS Tools Exist:**
- Symptoms: Terminal spawner silently fails on systems without gnome-terminal, xterm, or expected file managers
- Files: `IP/terminal_spawner.py` (spawn function, lines 71-95), `IP/plugins/06_maestro.py` (handle_apps, handle_matrix, handle_files functions, lines 657-720)
- Trigger: Running on minimal Linux systems, macOS without expected tools, or CI/CD environments
- Workaround: Install gnome-terminal, or modify subprocess calls to use alternative terminal emulators

## Security Considerations

**API Key Exposure Risk:**
- Risk: ANTHROPIC_API_KEY read from environment variable without protection; if app is exposed to untrusted network, API calls could leak key in logs or error messages
- Files: `IP/plugins/06_maestro.py` (anthropic client initialization, lines 754-785)
- Current mitigation: Error messages redact partial key information ("AuthenticationError" message)
- Recommendations: (1) Add rate limiting on API calls, (2) Never log full API responses, (3) Consider proxy pattern for API calls, (4) Document that this application should not be exposed to untrusted networks

**File Protection (Louis) Using chmod 444:**
- Risk: chmod 444 (read-only) protects against accidental modification but doesn't prevent:
  - Deletion by owner on Linux
  - Replacement via git operations if .git/hooks not enforced
  - Access if file is copied elsewhere
- Files: `IP/louis_core.py` (is_locked, chmod-based checks, lines 62-64)
- Current mitigation: Protected files list checked at git pre-commit via integration
- Recommendations: (1) Document that Louis is "accidental modification" protection, not "malicious attack" protection, (2) Add full path blocking in .gitignore for sensitive files, (3) Consider vault-style encryption for truly critical files

**Subprocess Spawning in `handle_apps`, `handle_matrix`, `handle_files`:**
- Risk: Spawning editor and file manager processes without input validation; if project_root contains shell metacharacters, could lead to injection
- Files: `IP/plugins/06_maestro.py` (lines 659-720)
- Current mitigation: Path is from project state, not user input
- Recommendations: Always quote subprocess arguments (already done); add validation that paths don't contain suspicious patterns; use pathlib.Path for all filesystem operations

## Performance Bottlenecks

**Large File Processing in Woven Maps:**
- Problem: `build_graph_data()` in `IP/woven_maps.py` (lines 150+) scans entire codebase including all files for line-of-code counting; on large projects (10k+ files) this can be slow
- Files: `IP/woven_maps.py` (build_graph_data, lines 150-200), `IP/connection_verifier.py` (verify_imports, lines 300-400)
- Cause: No caching of scan results; full file I/O on every Code City render
- Improvement path: (1) Add `.orchestr8/scan_cache.json` with timestamp, (2) Invalidate cache only on file modification, (3) Cache imports graph for faster connection verification

**Import Graph Verification Always Full-Scan:**
- Problem: `ConnectionVerifier` in `IP/connection_verifier.py` always re-scans all imports; no incremental updates
- Files: `IP/connection_verifier.py` (verify_all_files function, lines 500+)
- Cause: Stateless verification; tracks nothing between calls
- Improvement path: (1) Cache import results per file with file hash, (2) Only re-verify files that changed, (3) Use inotify/watchdog for file change detection

**Marimo Reactivity Overhead:**
- Problem: Every state change in `06_maestro.py` triggers full re-render of panels that read that state
- Files: `IP/plugins/06_maestro.py` (state management pattern, lines 375-423)
- Cause: Marimo's cell re-execution model; no granular update control
- Improvement path: (1) Profile which state updates cause visible lag, (2) Consider splitting large render functions into smaller memoized cells, (3) Document expected behavior in CLAUDE.md

## Fragile Areas

**Plugin Loading System Lacks Error Recovery:**
- Files: `orchestr8.py` (plugin_loader function, lines 88-124)
- Why fragile: If single plugin fails to import, error printed but other plugins still load; plugin ordering (00_, 01_, etc.) creates hidden dependencies not expressed in code
- Safe modification: (1) Before changing plugin names/order, verify no other plugins import them, (2) Add plugin dependency declaration mechanism, (3) Test all plugins load by running `marimo run orchestr8.py`
- Test coverage: No automated tests for plugin loading; manual testing only

**Component Panels Use Direct Class Instantiation:**
- Files: `IP/plugins/06_maestro.py` (lines 403-407 create panel instances), `IP/plugins/components/ticket_panel.py`, `IP/plugins/components/calendar_panel.py`, etc.
- Why fragile: Each panel class has its own initialization and visibility state; no unified panel lifecycle management
- Safe modification: (1) Always call `.set_visible()` when toggling panels, (2) Verify mutual exclusion logic before changing panel toggle handlers, (3) Check that panel .render() method works with both visible and hidden states
- Test coverage: No tests for panel visibility state machine; changes must be manually tested in UI

**State Management Using Marimo's `mo.state()`:**
- Files: All plugins that use `STATE_MANAGERS` pattern
- Why fragile: Distributed state across many cells; no centralized state schema; easy to create stale state if cells don't properly depend on each other
- Safe modification: (1) Always read state at the start of a render function, never cache it, (2) Test that reactive updates actually trigger re-renders, (3) Document which state is "global" vs "local" to each plugin
- Test coverage: No tests for state reactivity; easy to introduce render timing bugs

**Hard-coded Color Values Scattered Across Code:**
- Files: `IP/woven_maps.py` (COLORS dict, lines 30-48), `IP/plugins/06_maestro.py` (constants lines 128-134, CSS lines 139-328)
- Why fragile: Color system is three-state (Gold/Blue/Purple) but exact hex values appear in multiple places; inconsistencies will appear visually
- Safe modification: (1) If you change one color constant, search all files for that hex value and update, (2) Verify the CSS in 06_maestro.py matches the Python constants, (3) Test visual rendering after any color change
- Test coverage: No visual regression tests; changes must be manually verified

**Terminal Spawner Platform Detection:**
- Files: `IP/terminal_spawner.py` (spawn function, lines 69-105)
- Why fragile: Tries terminal emulators in sequence (gnome-terminal, xterm, etc.); each platform has different available tools; silent failure if none found
- Safe modification: Before adding new features that spawn terminals, test on target Linux distribution
- Test coverage: No tests for different terminal availability scenarios

## Scaling Limits

**Single-Process Marimo Application:**
- Current capacity: Single user, single machine
- Limit: App not designed for multi-user concurrent access; all state is in-memory
- Scaling path: (1) Add socket/REST API layer in front of Marimo, (2) Use Redis for shared state, (3) Implement session management, (4) This would require major refactoring

**Combat State File Performance:**
- Current capacity: Can track hundreds of active deployments efficiently (JSON file on disk)
- Limit: If tracking thousands of deployments, JSON file I/O becomes bottleneck
- Scaling path: (1) Move combat_state to database (SQLite already in config), (2) Implement in-memory cache with periodic flush, (3) Use binary format instead of JSON

**Import Graph Verification Memory:**
- Current capacity: Works well on codebases up to ~5k files
- Limit: `ConnectionVerifier` loads all imports into memory; no pagination/streaming
- Scaling path: (1) Implement batched processing in `verify_all_files()`, (2) Stream results instead of returning all at once, (3) Use generator pattern instead of lists

## Dependencies at Risk

**Marimo Version Pinning:**
- Risk: `orchestr8.py` comments reference "marimo >= 0.19.1" but no pyproject.toml or requirements.txt exists
- Impact: Version conflicts if someone installs older/newer marimo; plugin protocol may change in future versions
- Migration plan: (1) Create `requirements.txt` with pinned versions, (2) Add version check in `orchestr8.py` startup, (3) Document breaking changes from marimo upgrades

**Missing Dependency Management:**
- Risk: No requirements.txt or pyproject.toml in root; dependencies only mentioned in CLAUDE.md comments
- Impact: Difficult to set up environment; unclear which versions are required
- Migration plan: Create `requirements.txt` with: `marimo>=0.19.6`, `pandas`, `networkx`, `pyvis`, `jinja2`, and optionally `anthropic`, `toml`

**Anthropic SDK as Optional Dependency:**
- Risk: Chat won't work if not installed, but error only appears at runtime
- Impact: User setup confusion; unclear what needs to be installed for full functionality
- Migration plan: (1) Separate core requirements from optional (chat requires anthropic), (2) Add installer script that offers install options, (3) Add startup checks for optional dependencies

## Missing Critical Features

**No Persistent Configuration Storage:**
- Problem: Project root set in UI but lost on page refresh; plugins have no saved preferences
- Blocks: Can't save user setup across sessions; project root must be re-entered each run
- Fix path: (1) Store in browser localStorage for UI state, (2) Save project root to `~/.orchestr8/orchestr8.conf`, (3) Load on startup

**No Error Recovery / Restart:**
- Problem: If Code City scan fails or import graph becomes stale, no way to force refresh without restarting app
- Blocks: Stuck in broken state; can't fix without killing app
- Fix path: (1) Add "Refresh" button to maestro UI, (2) Add endpoint to reload all scans, (3) Implement proper state invalidation

**No Test Coverage:**
- Problem: Core modules like `connection_verifier.py`, `combat_tracker.py`, `woven_maps.py` have zero tests
- Blocks: Can't safely refactor; easy to introduce bugs
- Fix path: (1) Add pytest configuration, (2) Write unit tests for each core module, (3) Add GitHub Actions CI to run tests on every commit

## Test Coverage Gaps

**Woven Maps Code City (1981 lines, 0 tests):**
- What's not tested: Graph construction, node positioning algorithm, color assignment logic, error handling
- Files: `IP/woven_maps.py`
- Risk: Changes to layout algorithm could break visualization without catching it; invalid file paths silently handled
- Priority: High - this is the central UI feature

**Connection Verifier (902 lines, 0 tests):**
- What's not tested: Import detection regex for Python/JS/TS, relative import resolution, circular dependency detection, broken import classification
- Files: `IP/connection_verifier.py`
- Risk: Import graph could be completely wrong without detection; blue status (broken) may be inaccurate
- Priority: High - determines file health status

**Combat Tracker (100+ lines, 0 tests):**
- What's not tested: State file persistence, stale deployment cleanup, race conditions in concurrent access
- Files: `IP/combat_tracker.py`
- Risk: Combat state could become corrupted; cleanup could fail silently
- Priority: Medium - affects visual accuracy but not core functionality

**Louis File Protection (130+ lines, 0 tests):**
- What's not tested: chmod permission setting/checking, protected files list synchronization, git pre-commit hook integration
- Files: `IP/louis_core.py`
- Risk: Files could fail to lock without detection; false positives on permission checks
- Priority: Medium - affects file safety

**Plugin System (orchestr8.py, 0 tests):**
- What's not tested: Dynamic import of plugins, STATE_MANAGERS injection, plugin ordering, error handling if plugin fails
- Files: `orchestr8.py`
- Risk: Plugin loading could break silently; new plugins could conflict with existing ones
- Priority: Medium - affects app startup

**Marimo UI Rendering (components, ~4k lines total, 0 tests):**
- What's not tested: State reactivity, panel visibility toggling, mutual exclusion logic, event handler chains
- Files: `IP/plugins/06_maestro.py`, `IP/plugins/components/*.py`
- Risk: UI state could become inconsistent; panels could stay visible when they shouldn't
- Priority: Low - visual bugs are noticed by users, but no automated detection

---

*Concerns audit: 2026-01-30*
