"""
05_cli_bridge Plugin - TypeScript Plugin Execution Bridge
Orchestr8 v3.0 - The Fortress Factory

Provides dynamic discovery and execution of TypeScript CLI plugins
via the scaffold-cli.ts system. Bridges Python Marimo UI with
TypeScript parser tools.

Features:
    - Dynamic plugin discovery via `npx tsx scaffold-cli.ts list-plugins`
    - Interactive accordion UI for discovered plugins
    - Run button with subprocess execution
    - Timeout handling (30 seconds)
    - Result display for success/error/timeout
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

# Import smart output renderer
from IP.plugins.output_renderer import detect_and_render_output

PLUGIN_NAME = "🔗 CLI Bridge"
PLUGIN_ORDER = 5

# Configuration
DEFAULT_TIMEOUT = 30  # seconds
SCAFFOLD_CLI_PATH = "frontend/tools/scaffold-cli.ts"

def discover_plugins(root_path):
    """Execute list-plugins and parse JSON output."""
    scaffold_cli = Path(root_path) / SCAFFOLD_CLI_PATH
    
    if not scaffold_cli.exists():
        return [], f"Scaffold CLI not found at {SCAFFOLD_CLI_PATH}"
    
    try:
        result = subprocess.run(
            ["npx", "tsx", str(scaffold_cli), "list-plugins"],
            cwd=str(root_path),
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT
        )
        
        if result.returncode != 0:
            return [], f"CLI error: {result.stderr}"
        
        plugins = json.loads(result.stdout)
        return plugins, None
    except subprocess.TimeoutExpired:
        return [], "Plugin discovery timed out"
    except json.JSONDecodeError as e:
        return [], f"Invalid JSON response: {str(e)}"
    except Exception as e:
        return [], f"Discovery failed: {str(e)}"

def execute_plugin(root_path, command_type, target=None, options=None):
    """Execute a specific plugin and return results."""
    scaffold_cli = Path(root_path) / SCAFFOLD_CLI_PATH
    
    if not scaffold_cli.exists():
        return None, f"Scaffold CLI not found"
    
    # Build command
    cmd = ["npx", "tsx", str(scaffold_cli), command_type]
    
    if target:
        cmd.extend(["--target", target])
    
    if options:
        for key, value in options.items():
            if value is True:
                cmd.append(f"--{key}")
            elif value:
                cmd.extend([f"--{key}", str(value)])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(root_path),
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "command": " ".join(cmd)
        }, None
    except subprocess.TimeoutExpired:
        return None, f"Execution timed out after {DEFAULT_TIMEOUT}s"
    except Exception as e:
        return None, str(e)

def render(STATE_MANAGERS):
    """Render the CLI Bridge plugin UI."""
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    # Local state
    get_plugins, set_plugins = mo.state([])
    get_error, set_error = mo.state("")
    get_is_loading, set_is_loading = mo.state(False)
    get_results, set_results = mo.state({})  # {commandType: result}
    get_selected_target, set_selected_target = mo.state("")
    
    root = get_root()
    
    # Discovery function
    def do_discover():
        set_is_loading(True)
        set_error("")
        
        plugins, err = discover_plugins(root)
        
        if err:
            set_error(err)
            set_plugins([])
            logs = get_logs()
            set_logs(logs + [f"[CLI Bridge] Discovery failed: {err}"])
        else:
            set_plugins(plugins)
            logs = get_logs()
            set_logs(logs + [f"[CLI Bridge] Discovered {len(plugins)} plugins"])
        
        set_is_loading(False)
    
    # Discover button
    discover_btn = mo.ui.button(
        label="🔍 Discover Plugins" if not get_is_loading() else "⏳ Loading...",
        on_change=lambda _: do_discover(),
        disabled=get_is_loading()
    )
    
    # Target input
    target_input = mo.ui.text(
        value=get_selected_target() or root,
        label="Target Path",
        placeholder=root,
        on_change=set_selected_target
    )
    
    # Error display
    error = get_error()
    error_display = mo.md(f"⚠️ **Error:** {error}") if error else mo.md("")
    
    # Plugin cards/accordion builder
    plugins = get_plugins()
    results = get_results()
    
    def run_plugin(command_type):
        """Execute a plugin and store results."""
        target = get_selected_target() or root
        
        set_is_loading(True)
        
        result, err = execute_plugin(root, command_type, target)
        
        current_results = get_results()
        
        if err:
            current_results[command_type] = {
                "success": False,
                "error": err,
                "timestamp": datetime.now().isoformat()
            }
            logs = get_logs()
            set_logs(logs + [f"[CLI Bridge] {command_type} failed: {err}"])
        else:
            current_results[command_type] = {
                **result,
                "timestamp": datetime.now().isoformat()
            }
            status = "✅ Success" if result["success"] else "❌ Failed"
            logs = get_logs()
            set_logs(logs + [f"[CLI Bridge] {command_type}: {status}"])
        
        set_results(current_results)
        set_is_loading(False)
    
    def build_plugin_cards():
        """Build accordion items for each plugin."""
        if not plugins:
            return mo.md("*No plugins discovered. Click 'Discover Plugins' to scan.*")
        
        cards = []
        
        for plugin in plugins:
            cmd_type = plugin.get("commandType", "unknown")
            description = plugin.get("description", "No description")
            supports_compare = plugin.get("supportsCompare", False)
            specific_options = plugin.get("specificOptions", [])
            
            # Get result if available
            result = results.get(cmd_type)
            
            # Build result display using smart renderer
            if result:
                if result.get("success"):
                    stdout = result.get("stdout", "")
                    # Use smart JSON/text renderer
                    result_display = mo.vstack([
                        mo.md(f"**Status:** ✅ Success | **Timestamp:** {result.get('timestamp', 'N/A')}"),
                        detect_and_render_output(stdout)
                    ])
                else:
                    error_msg = result.get("error") or result.get("stderr", "Unknown error")
                    result_display = mo.md(f"""
**Status:** ❌ Failed  
**Error:** {error_msg}
                    """)
            else:
                result_display = mo.md("*Not yet executed*")
            
            # Build card content
            card_content = mo.vstack([
                mo.md(f"**Description:** {description}"),
                mo.md(f"**Supports Compare:** {'Yes' if supports_compare else 'No'}"),
                mo.md(f"**Options:** {', '.join(specific_options) if specific_options else 'None'}"),
                mo.ui.button(
                    label=f"▶️ Run {cmd_type}",
                    on_change=lambda _, ct=cmd_type: run_plugin(ct)
                ),
                mo.md("---"),
                mo.md("**Result:**"),
                result_display
            ])
            
            cards.append({
                "title": f"🔌 {cmd_type}",
                "content": card_content
            })
        
        # Build accordion
        accordion_items = {card["title"]: card["content"] for card in cards}
        
        return mo.ui.accordion(accordion_items)
    
    plugin_display = build_plugin_cards()
    
    # Stats
    stats_md = f"**Plugins discovered:** {len(plugins)} | **Target:** `{get_selected_target() or root}`"
    
    # CLI info
    cli_info = mo.md(f"""
**CLI Location:** `{SCAFFOLD_CLI_PATH}`  
**Timeout:** {DEFAULT_TIMEOUT}s per execution
    """)
    
    # Layout
    return mo.vstack([
        mo.md("## 🔗 TypeScript CLI Bridge"),
        cli_info,
        mo.md("---"),
        mo.hstack([discover_btn, target_input], gap="1rem"),
        mo.md(stats_md),
        error_display,
        mo.md("---"),
        plugin_display,
        mo.md("---"),
        mo.md("*Plugins are discovered from `frontend/tools/parsers/*.ts`*")
    ])
