import marimo as mo
import os
import sys
import importlib.util
from pathlib import Path

# ==========================================
# 1. GLOBAL STATE (The Backbone)
# ==========================================
get_root, set_root = mo.state(os.getcwd())
get_files, set_files = mo.state(None)
get_selected, set_selected = mo.state(None)
get_logs, set_logs = mo.state([])

# Bundle state for plugins
STATE_MANAGERS = {
    "root": (get_root, set_root),
    "files": (get_files, set_files),
    "selected": (get_selected, set_selected),
    "logs": (get_logs, set_logs)
}

# ==========================================
# 2. DYNAMIC PLUGIN LOADER
# ==========================================
def load_plugins():
    plugin_dir = Path(__file__).parent / "plugins"
    plugins = []
    
    if not plugin_dir.exists():
        os.makedirs(plugin_dir)
        return []

    # Scan for .py files
    for file in sorted(plugin_dir.glob("*.py")):
        if file.name.startswith("__"): continue
        
        try:
            # Dynamic Import Magic
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check Protocol
            if hasattr(module, "render"):
                name = getattr(module, "PLUGIN_NAME", file.stem)
                order = getattr(module, "PLUGIN_ORDER", 999)
                plugins.append({"name": name, "module": module, "order": order})
        except Exception as e:
            print(f"Failed to load plugin {file.name}: {e}")
            
    return sorted(plugins, key=lambda x: x["order"])

# ==========================================
# 3. MAIN RENDER
# ==========================================
plugins = load_plugins()

# Build Tabs Dictionary
tabs_content = {}
for p in plugins:
    # Render the plugin, injecting state
    tabs_content[p["name"]] = p["module"].render(STATE_MANAGERS)

# Add Logs Tab by default
tabs_content["📜 System Logs"] = mo.md(lambda: "\n".join(get_logs()))

# Layout
mo.vstack([
    mo.md("# 🎻 Orchestr8 v2.5: The Fortress"),
    mo.ui.text(value=get_root(), label="Project Root", on_change=set_root),
    mo.ui.tabs(tabs_content)
])
