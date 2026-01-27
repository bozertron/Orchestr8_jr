import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def core_setup():
    """Core Library Imports"""
    import marimo as mo
    import os
    import sys
    import importlib.util
    from pathlib import Path
    return mo, os, sys, importlib, Path


@app.cell
def state_manager(mo, os):
    """Global State Hub - The Data Core"""
    get_root, set_root = mo.state(os.getcwd())
    get_files, set_files = mo.state(None)   # Stores DataFrame
    get_edges, set_edges = mo.state(None)   # Stores DataFrame
    get_selected, set_selected = mo.state(None)
    get_logs, set_logs = mo.state([])
    
    # The Protocol Object passed to all plugins
    # This is the "API" your plugins interact with
    STATE_MANAGERS = {
        "root": (get_root, set_root),
        "files": (get_files, set_files),
        "edges": (get_edges, set_edges),
        "selected": (get_selected, set_selected),
        "logs": (get_logs, set_logs)
    }
    return STATE_MANAGERS, get_root, set_root


@app.cell
def plugin_loader(mo, Path, importlib, sys, STATE_MANAGERS):
    """
    Dynamic Plugin Loader - Self-Locating
    Scans the 'plugins' folder next to this script.
    """
    # 1. FIND OURSELVES (The Fix)
    # If running as script, use __file__. If in notebook mode, fallback to cwd.
    try:
        current_file = Path(__file__)
        app_dir = current_file.parent
    except NameError:
        app_dir = Path.cwd()

    # 2. LOCATE PLUGINS
    plugin_dir = app_dir / "plugins"
    
    # 3. FIX PYTHON PATH
    # Ensure plugins can import sibling modules (like IP.woven_maps)
    if str(app_dir.parent) not in sys.path:
        sys.path.insert(0, str(app_dir.parent))
    
    plugins = []
    
    # Debug info for the console
    print(f"🔌 Orchestr8 Host located at: {app_dir}")
    print(f"🔌 Scanning for plugins in: {plugin_dir}")
    
    if plugin_dir.exists():
        for file in sorted(plugin_dir.glob("*.py")):
            if file.name.startswith("__") or not file.name.endswith(".py"): 
                continue
            
            try:
                # Import module dynamically
                spec = importlib.util.spec_from_file_location(file.stem, file)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                
                # Verify Protocol (Must have render function)
                if hasattr(mod, "render"):
                    plugins.append({
                        "name": getattr(mod, "PLUGIN_NAME", file.stem),
                        "order": getattr(mod, "PLUGIN_ORDER", 999),
                        "render": mod.render
                    })
                    print(f"   ✅ Loaded: {file.name}")
                else:
                    print(f"   ⚠️ Skipped {file.name}: Missing 'render' function")
                    
            except Exception as e:
                print(f"   ❌ Error loading {file.name}: {e}")
    else:
        print(f"❌ Plugin directory not found at {plugin_dir}")
        print("   Did you create the 'plugins' folder?")

    # Sort plugins by order and execute render()
    tabs = {}
    for p in sorted(plugins, key=lambda x: x["order"]):
        try:
            # Dependency Injection: Pass STATE_MANAGERS to the plugin
            tabs[p["name"]] = p["render"](STATE_MANAGERS)
        except Exception as e:
            tabs[p["name"]] = mo.md(f"**Error rendering {p['name']}:** {str(e)}")
            
    return (tabs,)


@app.cell
def ui_render(mo, get_root, set_root, tabs):
    """Main UI Layout Renderer"""
    header = mo.md("# Orchestr8: The Command Center")
    path_input = mo.ui.text(
        value=get_root(), 
        label="Project Root", 
        on_change=set_root, 
        full_width=True
    )
    
    if not tabs:
        content = mo.md("""
        ### No Plugins Found
        
        The Host is running, but no plugins were loaded.
        
        **Action Required:**
        1. Ensure you have created the `IP/plugins/` directory.
        2. Ensure you have added the plugin files (Explorer, Graph, etc.) into that directory.
        """)
    else:
        content = mo.ui.tabs(tabs)
        
    return mo.vstack([header, path_input, content])


if __name__ == "__main__":
    app.run()
