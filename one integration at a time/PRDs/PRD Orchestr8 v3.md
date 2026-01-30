📜 PRD: Orchestr8 v3.0 - The Fortress Factory
**Philosophy:** "The Mainframe." A modular, reactive Command Center that orchestrates Python logic and TypeScript tools through a unified Plugin Architecture.
**Core Stack:** Marimo (UI/State), Python (Glue), TypeScript (Analysis), SQLite (Data).

## 1. The Directory Structure (The "IP" Protocol)
The system relies on a rigid directory layout. The Agent must verify this structure exists.

```text
project_root/
├── IP/
│   ├── __init__.py         # (Empty) Makes IP importable
│   ├── orchestr8_app.py    # (Host) The Main Marimo Application
│   ├── louis_core.py       # (Logic) The File Warden
│   ├── carl_core.py        # (Logic) The Context Bridge
│   ├── connie.py           # (Logic) The Database Converter
│   └── plugins/            # (Python UI Plugins)
│       ├── 01_generator.py # The 7-Phase Wizard
│       ├── 02_explorer.py  # The Carl UI
│       ├── 03_gatekeeper.py# The Louis UI
│       ├── 04_connie_ui.py # The Connie UI
│       └── 05_cli_bridge.py# (New) The TypeScript Scaffold Bridge
├── frontend/tools/
│   ├── scaffold-cli.ts     # (The TS Protocol Source)
│   ├── unified-context-system.ts
│   └── parsers/            # (Future TS Plugins live here)
└── .louis-control/         # Configuration storage
```

---

## 2. The Host Application (`orchestr8_app.py`)
**Role:** The Chassis. It manages global state and loads the UI plugins.

### 2.1 State Management (The Bus)
The Host must initialize a `STATE_MANAGERS` dictionary passed to every plugin.
*   `root`: The Project Root path (getter/setter).
*   `files`: The DataFrame of project files (getter/setter).
*   `selected`: The currently selected file path (getter/setter).
*   `logs`: A list of system events (getter/setter).

### 2.2 The Plugin Loader
*   **Logic:**
    1.  Scan `IP/plugins/*.py`.
    2.  Dynamically import modules using `importlib`.
    3.  Read metadata: `PLUGIN_NAME` and `PLUGIN_ORDER`.
    4.  Execute `module.render(STATE_MANAGERS)`.
    5.  Construct the `mo.ui.tabs` dictionary.

---

## 3. The Core Logic Modules (No Mocks)

### 3.1 Louis v2.1 (The Warden)
*   **Source:** `IP/louis_core.py`
*   **Capabilities:**
    *   `scan_and_protect()`: Scans folders defined in `.louis-control/louis-config.json`.
    *   `install_git_hook()`: Writes the pre-commit hook to `.git/hooks/`.
    *   `lock_file() / unlock_file()`: Uses `os.chmod` to enforce read-only status.

### 3.2 Connie (The Converter)
*   **Source:** `IP/connie.py` (Migrated from legacy input)
*   **Capabilities:**
    *   `ConversionEngine`: Connects to SQLite, exports to JSON/MD/CSV.
    *   **Requirement:** Must run headless (no PyQt).

### 3.3 Carl v2.0 (The Context Bridge)
*   **Source:** `IP/carl_core.py`
*   **Capabilities:**
    *   Wrapper around `frontend/tools/unified-context-system.ts`.
    *   Executes: `subprocess.run(["npx", "tsx", "frontend/tools/unified-context-system.ts"])`.
    *   Ingests the resulting JSON map into the `files` DataFrame.

---

## 4. The UI Plugins (The Interface)

### 4.1 Plugin 01: The Generator (`01_generator.py`)
*   **Function:** The "New Project" Wizard.
*   **Logic:** Implements the 7-Phase Build Spec.
*   **Output:** Writes to `BUILD_SPEC.json`.
*   **Interaction:** Text Input + "Lock Phase" button.

### 4.2 Plugin 02: The Explorer (`02_explorer.py`)
*   **Function:** The File Tree & Context Viewer.
*   **Integration:** Calls **Carl** to get file data.
*   **UI:** `mo.ui.table` (Interactive). Selecting a row updates global `selected` state.

### 4.3 Plugin 03: The Gatekeeper (`03_gatekeeper.py`)
*   **Function:** Louis's Dashboard.
*   **UI:**
    *   Status Indicator (Secure/Vulnerable).
    *   "Lock All" Button.
    *   "Install Git Hook" Button.
    *   Per-file Toggle (Lock/Unlock) for the `selected` file.

### 4.4 Plugin 04: Connie UI (`04_connie_ui.py`)
*   **Function:** Database tools.
*   **UI:** Dropdown of found `.db` files + "Convert" button.

---

## 5. The Scaffold Bridge (`05_cli_bridge.py`)
**The New Architecture:** This plugin allows Orchestr8 to consume your TypeScript CLI tools.

### 5.1 The Protocol
It relies on `frontend/tools/scaffold-cli.ts` (The User's Input).
*   **Discovery:** The Python plugin executes:
    `npx tsx frontend/tools/scaffold-cli.ts list-plugins`
*   **Ingestion:** It parses the JSON output to find available TS plugins (e.g., 'stores', 'routes').

### 5.2 Dynamic UI Generation
For every plugin returned by the CLI:
1.  Orchestr8 creates a sub-tab (or section).
2.  It renders the plugin's `description`.
3.  It provides a "Run Analysis" button.
4.  **Action:** When clicked, it runs:
    `npx tsx frontend/tools/scaffold-cli.ts [commandType] --target [root]`
5.  **Output:** It captures the JSON result and renders it as a Data Grid.

---

## 6. Execution Instructions for the Agent
1.  **Setup:** Verify `IP/` exists. Create `IP/plugins/`.
2.  **Migration:**
    *   Move `louis_core.py` logic to `IP/louis_core.py`.
    *   Move `connie.py` logic (ConversionEngine only) to `IP/connie.py`.
    *   Create `IP/carl_core.py` wrapper.
3.  **Host Creation:** Write `IP/orchestr8_app.py` with the dynamic loader.
4.  **Plugin Creation:** Write the 5 plugin files in `IP/plugins/`.
5.  **Bridge Implementation:** Ensure `05_cli_bridge.py` correctly calls the `list-plugins` command defined in `scaffold-cli.ts`.

---
**Final Note:** This architecture ensures that when you add a new TypeScript parser to `frontend/tools/parsers/`, Orchestr8 *automatically* discovers it and builds a GUI for it. No Python code changes required.

**Build it.**
