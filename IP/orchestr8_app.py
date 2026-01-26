"""Orchestr8 v3.0 - The Fortress Factory

A reactive Marimo notebook for codebase orchestration with dynamic plugin loading.
This is the main application entry point using the IP Protocol directory structure.

Usage:
    marimo run IP/orchestr8_app.py
    marimo edit IP/orchestr8_app.py

Requirements:
    - Python 3.12+
    - marimo >= 0.19.1
    - pandas
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


# ============================================================================
# Cell 1: Core Imports
# ============================================================================
@app.cell
def imports():
    """Core imports for Orchestr8 v3.0"""
    import marimo as mo
    import os
    import sys
    import importlib.util
    from pathlib import Path
    import json
    return Path, importlib, json, mo, os, sys


# ============================================================================
# Cell 2: State Management - The Backbone
# ============================================================================
@app.cell
def state_management(mo, os):
    """Global state using Marimo's reactive state hooks.
    
    STATE_MANAGERS Pattern:
        Each state is a tuple of (getter, setter) functions.
        Plugins receive STATE_MANAGERS dict and can read/write state reactively.
    """
    # Core state definitions
    get_root, set_root = mo.state(os.getcwd())
    get_files, set_files = mo.state(None)
    get_selected, set_selected = mo.state(None)
    get_logs, set_logs = mo.state([])
    
    # Bundle state for plugin injection
    STATE_MANAGERS = {
        "root": (get_root, set_root),
        "files": (get_files, set_files),
        "selected": (get_selected, set_selected),
        "logs": (get_logs, set_logs)
    }
    
    return (
        STATE_MANAGERS,
        get_files,
        get_logs,
        get_root,
        get_selected,
        set_files,
        set_logs,
        set_root,
        set_selected,
    )


# ============================================================================
# Cell 3: Dynamic Plugin Loader
# ============================================================================
@app.cell
def plugin_loader(Path, importlib, os):
    """Dynamic plugin discovery and loading.
    
    Scans IP/plugins/*.py for valid plugins.
    Valid plugins must have:
        - PLUGIN_NAME: str (display name)
        - PLUGIN_ORDER: int (tab order, lower = first)
        - render(STATE_MANAGERS): function returning mo.Html or mo.md
    """
    def load_plugins():
        # Get the IP directory (parent of this file)
        ip_dir = Path(__file__).parent if "__file__" in dir() else Path.cwd() / "IP"
        plugin_dir = ip_dir / "plugins"
        plugins = []
        
        if not plugin_dir.exists():
            os.makedirs(plugin_dir, exist_ok=True)
            return []
        
        # Scan for .py files, sorted by name (prefix ordering)
        for file in sorted(plugin_dir.glob("*.py")):
            if file.name.startswith("__"):
                continue
            
            try:
                # Dynamic import using importlib
                spec = importlib.util.spec_from_file_location(file.stem, file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Validate plugin protocol
                    if hasattr(module, "render"):
                        name = getattr(module, "PLUGIN_NAME", file.stem)
                        order = getattr(module, "PLUGIN_ORDER", 999)
                        plugins.append({
                            "name": name,
                            "module": module,
                            "order": order,
                            "file": file.name
                        })
            except Exception as e:
                print(f"[Plugin Loader] Failed to load {file.name}: {e}")
        
        # Sort by PLUGIN_ORDER
        return sorted(plugins, key=lambda x: x["order"])
    
    return (load_plugins,)


# ============================================================================
# Cell 4: Plugin Rendering
# ============================================================================
@app.cell
def plugin_renderer(STATE_MANAGERS, load_plugins, mo):
    """Load plugins and build tabs content dictionary."""
    # Load all discovered plugins
    plugins = load_plugins()
    
    # Build tabs content from plugins
    tabs_content = {}
    plugin_errors = []
    
    for p in plugins:
        try:
            # Render plugin, injecting STATE_MANAGERS
            rendered = p["module"].render(STATE_MANAGERS)
            tabs_content[p["name"]] = rendered
        except Exception as e:
            plugin_errors.append(f"Error rendering {p['name']}: {e}")
    
    # Report any plugin errors
    if plugin_errors:
        for err in plugin_errors:
            print(f"[Plugin Error] {err}")
    
    return plugins, plugin_errors, tabs_content


# ============================================================================
# Cell 5: System Logs Tab
# ============================================================================
@app.cell
def logs_tab(get_logs, mo):
    """System logs display - always available."""
    def render_logs():
        logs = get_logs()
        if not logs:
            return mo.md("*No logs yet. Actions will be recorded here.*")
        return mo.md("\n".join([f"- {log}" for log in logs]))
    
    logs_content = render_logs()
    return (logs_content,)


# ============================================================================
# Cell 6: Main UI Layout
# ============================================================================
@app.cell
def main_layout(mo, get_root, set_root, tabs_content, logs_content, plugins):
    """Main application layout with header, controls, and tabs."""
    # Header
    header = mo.md("# 🎻 Orchestr8 v3.0: The Fortress Factory")
    
    # Project root input
    root_input = mo.ui.text(
        value=get_root(),
        label="Project Root",
        on_change=set_root,
        full_width=True
    )
    
    # Plugin status
    plugin_count = len(plugins)
    status_badge = mo.md(f"**Plugins Loaded:** {plugin_count}")
    
    # Build final tabs (plugins + system logs)
    final_tabs = {**tabs_content, "📜 System Logs": logs_content}
    
    # Show empty state if no plugins
    if not tabs_content:
        final_tabs["🔌 Getting Started"] = mo.md("""
## No Plugins Found

Create plugins in `IP/plugins/` directory. Each plugin needs:

```python
PLUGIN_NAME = "My Plugin"
PLUGIN_ORDER = 1  # Lower = appears first

def render(STATE_MANAGERS):
    import marimo as mo
    get_root, set_root = STATE_MANAGERS["root"]
    return mo.md(f"Current root: {get_root()}")
```
        """)
    
    # Main layout
    layout = mo.vstack([
        header,
        mo.hstack([root_input, status_badge], justify="space-between", align="center"),
        mo.ui.tabs(final_tabs)
    ])
    
    return (layout,)


# ============================================================================
# Cell 7: App Entry Point
# ============================================================================
@app.cell
def display(layout):
    """Display the main layout."""
    return layout


# ============================================================================
# Run
# ============================================================================
if __name__ == "__main__":
    app.run()
