"""Orchestr8 v3.0

Canonical entrypoint for Orchestr8, rendering IP/plugins/06_maestro.py directly.

Usage:
    marimo run orchestr8.py
    marimo edit orchestr8.py
"""

import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


# ============================================================================
# Cell 1: Core Imports
# ============================================================================
@app.cell
def imports():
    """Core imports for direct Maestro loading."""
    import marimo as mo
    import os
    import sys
    from pathlib import Path

    # Force Uvicorn off legacy websockets protocol to avoid Python 3.14
    # close-race crashes (AttributeError: transfer_data_task) in this stack.
    try:
        import uvicorn

        original_config_init = uvicorn.Config.__init__

        def orchestr8_uvicorn_config_init(self, *args, **kwargs):
            kwargs.setdefault("ws", "websockets-sansio")
            return original_config_init(self, *args, **kwargs)

        if uvicorn.Config.__init__.__name__ != "orchestr8_uvicorn_config_init":
            uvicorn.Config.__init__ = orchestr8_uvicorn_config_init
    except Exception:
        pass

    # Add IP to path for local imports used by plugin internals.
    _ip_root = Path(os.getcwd()) / "IP"
    if str(_ip_root) not in sys.path:
        sys.path.insert(0, str(_ip_root))

    return Path, mo, os


# ============================================================================
# Cell 2: State Management
# ============================================================================
@app.cell
def state_management(mo, os):
    """Initialize STATE_MANAGERS expected by 06_maestro.py."""
    _ip_root = os.path.join(os.getcwd(), "IP")
    default_root = _ip_root if os.path.isdir(_ip_root) else os.getcwd()

    get_root, set_root = mo.state(default_root)
    get_files, set_files = mo.state(None)
    get_selected, set_selected = mo.state(None)
    get_logs, set_logs = mo.state([])
    get_health, set_health = mo.state({})
    get_health_status, set_health_status = mo.state("idle")

    STATE_MANAGERS = {
        "root": (get_root, set_root),
        "files": (get_files, set_files),
        "selected": (get_selected, set_selected),
        "logs": (get_logs, set_logs),
        "health": (get_health, set_health),
        "health_status": (get_health_status, set_health_status),
    }

    return (STATE_MANAGERS,)


# ============================================================================
# Cell 3: Direct Maestro Render
# ============================================================================
@app.cell
def load_maestro_direct(STATE_MANAGERS, Path, mo):
    """Load and render 06_maestro.py directly (no plugin wrapper)."""
    import importlib.util

    plugin_file = Path(__file__).parent / "IP" / "plugins" / "06_maestro.py"

    try:
        spec = importlib.util.spec_from_file_location("maestro_direct", plugin_file)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load module spec for {plugin_file}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.render(STATE_MANAGERS)

    except Exception as e:
        import traceback

        error_detail = traceback.format_exc()
        result = mo.md(
            f"""
## Error Loading Maestro

**File:** `{plugin_file}`

**Error:** `{e}`

<details>
<summary>Full Traceback</summary>

```
{error_detail}
```

</details>
            """
        )

    return (result,)


# ============================================================================
# Cell 4: App Entry Point
# ============================================================================
@app.cell
def display(result):
    result
    return


# ============================================================================
# Run
# ============================================================================
if __name__ == "__main__":
    app.run()
