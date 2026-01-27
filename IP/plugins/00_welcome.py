"""
00_welcome Plugin - Welcome Tab
Orchestr8 v3.0 - The Fortress Factory

A simple welcome plugin that displays the getting started guide.
This plugin demonstrates the plugin protocol.

Plugin Protocol:
    PLUGIN_NAME: str - Display name in tab
    PLUGIN_ORDER: int - Tab order (lower = first)
    render(STATE_MANAGERS) - Returns mo.Html or mo.md element

STATE_MANAGERS Pattern:
    {
        "root": (get_root, set_root),
        "files": (get_files, set_files),
        "selected": (get_selected, set_selected),
        "logs": (get_logs, set_logs)
    }
"""

PLUGIN_NAME = "Welcome"
PLUGIN_ORDER = 0

def render(STATE_MANAGERS):
    """Render the welcome tab content."""
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    # Welcome content
    welcome_md = mo.md("""
## Welcome to Orchestr8 v3.0

**The Fortress Factory** - A modular, reactive Command Center for codebase orchestration.

### Quick Start

1. **Set Project Root** - Enter the path to your project above
2. **Explore Tabs** - Use the tabs to access different tools
3. **Check Logs** - System activity is recorded in the Logs tab

### Available Plugins

| Plugin | Purpose |
|--------|---------|
| Welcome | Getting started guide (this tab) |
| Explorer | Browse and select files |
| Generator | 7-phase project wizard |
| Gatekeeper | File protection with Louis |
| Connie | Database conversion tools |
| CLI Bridge | Execute TypeScript parsers |

### Architecture

```
IP/
├── orchestr8_app.py    # Main Marimo app
├── plugins/            # Dynamic plugin directory
│   ├── 00_welcome.py   # This plugin
│   ├── 01_generator.py # Generator wizard
│   └── ...
├── carl_core.py        # TypeScript bridge
├── louis_core.py       # File protection
└── connie.py           # DB conversion engine
```

### STATE_MANAGERS

Access reactive state through the STATE_MANAGERS dictionary:

```python
get_root, set_root = STATE_MANAGERS["root"]
current_root = get_root()
set_root("/new/path")
```
    """)
    
    # Log that welcome was rendered
    def log_visit():
        logs = get_logs()
        if not any("Welcome tab" in log for log in logs[-5:]):
            set_logs(logs + [f"[Welcome] Tab visited"])
    
    # Trigger log on render (only if not recently logged)
    log_visit()
    
    # Current project info
    root = get_root()
    project_info = mo.md(f"""
---
**Current Project Root:** `{root}`
    """)
    
    return mo.vstack([welcome_md, project_info])
