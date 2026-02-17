"""
05_universal_bridge Plugin - Dynamic Registry-Based Tool Bridge
Orchestr8 v3.0

Universal Bridge dynamically scans the registry directory for tool manifests
and generates interactive UI components for each discovered tool.

Features:
    - Dynamic registry scanning (frontend/tools/registry/*.json)
    - Manifest validation (required: name, base_command)
    - Auto-discovery of tool commands via discovery.command
    - Static command support via static_commands array
    - Smart output rendering using detect_and_render_output()
    - Timeout handling and error display
    - Command validation via shutil.which()

Manifest Schema:
    {
        "name": "Tool Name",
        "description": "Optional description",
        "icon": "Optional icon (e.g., 'TS', 'RS')",
        "base_command": ["npx", "tsx", "path/to/cli.ts"],
        "discovery": {
            "enabled": true,
            "command": "list-plugins"
        },
        "static_commands": [
            {"name": "Overview", "command": "overview"},
            {"name": "Routes", "command": "routes"}
        ]
    }

Requires: Python 3.12+, marimo
"""

import json
import shutil
import subprocess
from datetime import datetime
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any, Optional

# Import smart output renderer
from IP.plugins.output_renderer import detect_and_render_output

PLUGIN_NAME = "Universal Bridge"
PLUGIN_ORDER = 5

# Configuration
DEFAULT_TIMEOUT = 30  # seconds
REGISTRY_PATH = "frontend/tools/registry"
REQUIRED_FIELDS = ["name", "base_command"]
OPTIONAL_FIELDS = ["description", "icon", "discovery", "static_commands"]


def scan_registry(root_path: Path) -> tuple[list[dict], list[str]]:
    """
    Scan registry directory for valid tool manifests.
    
    Args:
        root_path: Project root directory
        
    Returns:
        Tuple of (valid_manifests, errors)
    """
    registry_dir = root_path / REGISTRY_PATH
    manifests = []
    errors = []
    
    if not registry_dir.exists():
        return [], [f"Registry directory not found: {REGISTRY_PATH}"]
    
    # Scan for JSON files (exclude .template files)
    for json_file in registry_dir.glob("*.json"):
        # Skip template files
        if ".template" in json_file.name:
            continue
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            
            # Validate required fields
            missing = [field for field in REQUIRED_FIELDS if field not in manifest]
            if missing:
                errors.append(f"{json_file.name}: Missing required fields: {missing}")
                continue
            
            # Add metadata
            manifest["_source_file"] = json_file.name
            manifest["_file_path"] = str(json_file)
            manifests.append(manifest)
            
        except JSONDecodeError as e:
            errors.append(f"{json_file.name}: Invalid JSON - {str(e)}")
        except Exception as e:
            errors.append(f"{json_file.name}: Load error - {str(e)}")
    
    # Sort by filename for consistent ordering
    manifests.sort(key=lambda m: m.get("_source_file", ""))
    
    return manifests, errors


def validate_command(base_command: list[str]) -> tuple[bool, str]:
    """
    Validate that the base command is executable.
    
    Args:
        base_command: Command list (e.g., ["npx", "tsx", "..."])
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not base_command:
        return False, "Empty command"
    
    # For npx/npm commands, check if npm is available
    if base_command[0] in ("npx", "npm"):
        if shutil.which("npm"):
            return True, "npm available"
        return False, "npm not found in PATH"
    
    # For other commands, check directly
    if shutil.which(base_command[0]):
        return True, f"{base_command[0]} available"
    
    return False, f"{base_command[0]} not found in PATH"


def run_discovery(
    root_path: Path,
    manifest: dict
) -> tuple[list[dict], Optional[str]]:
    """
    Execute discovery command and parse results.
    
    Args:
        root_path: Project root directory
        manifest: Tool manifest with discovery config
        
    Returns:
        Tuple of (discovered_commands, error_message)
    """
    discovery = manifest.get("discovery", {})
    if not discovery.get("enabled"):
        return [], None
    
    base_cmd = manifest.get("base_command", [])
    discovery_cmd = discovery.get("command")
    
    if not discovery_cmd:
        return [], "No discovery command specified"
    
    # Build full command
    full_cmd = base_cmd + [discovery_cmd, "--json"]
    
    try:
        result = subprocess.run(
            full_cmd,
            cwd=str(root_path),
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT
        )
        
        if result.returncode != 0:
            return [], f"Discovery failed: {result.stderr or 'Unknown error'}"
        
        # Parse JSON output
        commands = json.loads(result.stdout)
        
        if isinstance(commands, list):
            return commands, None
        else:
            return [commands], None
            
    except subprocess.TimeoutExpired:
        return [], f"Discovery timed out after {DEFAULT_TIMEOUT}s"
    except JSONDecodeError as e:
        return [], f"Invalid JSON from discovery: {str(e)}"
    except Exception as e:
        return [], f"Discovery error: {str(e)}"


def execute_command(
    root_path: Path,
    base_command: list[str],
    command: str,
    target: Optional[str] = None,
    extra_args: Optional[list[str]] = None
) -> dict:
    """
    Execute a tool command and return results.
    
    Args:
        root_path: Project root directory
        base_command: Base command list
        command: Command to execute
        target: Optional target path
        extra_args: Optional additional arguments
        
    Returns:
        Result dictionary with success, stdout, stderr, etc.
    """
    # Build full command
    full_cmd = list(base_command) + [command]
    
    if target:
        full_cmd.extend(["--target", target])
    
    if extra_args:
        full_cmd.extend(extra_args)
    
    try:
        result = subprocess.run(
            full_cmd,
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
            "command": " ".join(full_cmd),
            "timestamp": datetime.now().isoformat()
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Timeout after {DEFAULT_TIMEOUT}s",
            "command": " ".join(full_cmd),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": " ".join(full_cmd),
            "timestamp": datetime.now().isoformat()
        }


def render(STATE_MANAGERS: dict) -> Any:
    """
    Render the Universal Bridge plugin UI.
    
    Args:
        STATE_MANAGERS: Dictionary of state getters/setters
        
    Returns:
        Marimo UI element
    """
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    root = Path(get_root())
    
    # Local state for each tool's discovered commands and results
    get_tool_states, set_tool_states = mo.state({})
    get_scan_errors, set_scan_errors = mo.state([])
    get_is_scanning, set_is_scanning = mo.state(False)
    get_selected_target, set_selected_target = mo.state("")
    
    # Scan registry
    manifests, scan_errors = scan_registry(root)
    
    if scan_errors:
        set_scan_errors(scan_errors)
    
    def log_message(msg: str) -> None:
        """Add message to logs."""
        logs = get_logs()
        set_logs(logs + [f"[Universal Bridge] {msg}"])
    
    def do_discovery(manifest_name: str, manifest: dict) -> None:
        """Run discovery for a specific tool."""
        states = get_tool_states()
        if manifest_name not in states:
            states[manifest_name] = {"commands": [], "results": {}, "error": None}
        
        states[manifest_name]["error"] = None
        set_tool_states(states)
        
        commands, error = run_discovery(root, manifest)
        
        states = get_tool_states()
        if error:
            states[manifest_name]["error"] = error
            log_message(f"{manifest_name} discovery failed: {error}")
        else:
            states[manifest_name]["commands"] = commands
            log_message(f"{manifest_name}: Discovered {len(commands)} commands")
        
        set_tool_states(states)
    
    def run_command(
        manifest_name: str,
        base_command: list[str],
        command: str,
        command_id: str
    ) -> None:
        """Execute a command for a tool."""
        target = get_selected_target() or str(root)
        
        result = execute_command(root, base_command, command, target)
        
        states = get_tool_states()
        if manifest_name not in states:
            states[manifest_name] = {"commands": [], "results": {}, "error": None}
        
        states[manifest_name]["results"][command_id] = result
        set_tool_states(states)
        
        status = "Success" if result.get("success") else "Failed"
        log_message(f"{manifest_name}.{command}: {status}")
    
    def build_tool_accordion(manifest: dict) -> Any:
        """Build accordion content for a single tool."""
        name = manifest.get("name", "Unknown Tool")
        description = manifest.get("description", "No description")
        icon = manifest.get("icon", "[T]")
        base_command = manifest.get("base_command", [])
        static_commands = manifest.get("static_commands", [])
        discovery = manifest.get("discovery", {})
        
        # Get tool state
        states = get_tool_states()
        tool_state = states.get(name, {"commands": [], "results": {}, "error": None})
        discovered_commands = tool_state.get("commands", [])
        results = tool_state.get("results", {})
        discovery_error = tool_state.get("error")
        
        # Validate command
        cmd_valid, cmd_msg = validate_command(base_command)
        
        # Header info
        header_elements = [
            mo.md(f"**Description:** {description}"),
            mo.md(f"**Base Command:** `{' '.join(base_command)}`"),
            mo.md(f"**Command Status:** {'[OK]' if cmd_valid else '[ERR]'} {cmd_msg}"),
        ]
        
        # Discovery section
        if discovery.get("enabled"):
            discover_btn = mo.ui.button(
                label="Run Discovery",
                on_change=lambda _, m=manifest, n=name: do_discovery(n, m),
                disabled=not cmd_valid
            )
            header_elements.append(
                mo.hstack([discover_btn], justify="start")
            )

            if discovery_error:
                header_elements.append(
                    mo.md(f"**Discovery Error:** {discovery_error}")
                )
        
        header_elements.append(mo.md("---"))
        
        # Build command buttons section
        command_elements = []
        
        # Static commands
        if static_commands:
            command_elements.append(mo.md("### Static Commands"))
            for static_cmd in static_commands:
                cmd_name = static_cmd.get("name", "Unknown")
                cmd_value = static_cmd.get("command", "")
                cmd_id = f"static_{cmd_value}"
                
                # Button for this command
                btn = mo.ui.button(
                    label=f"Run {cmd_name}",
                    on_change=lambda _, bc=base_command, c=cmd_value, n=name, cid=cmd_id: run_command(n, bc, c, cid),
                    disabled=not cmd_valid
                )

                # Result display
                result = results.get(cmd_id)
                if result:
                    if result.get("success"):
                        result_ui = mo.vstack([
                            mo.md(f"**Success** | `{result.get('command', '')}`"),
                            detect_and_render_output(result.get("stdout", ""))
                        ])
                    else:
                        error_msg = result.get("error") or result.get("stderr", "Unknown error")
                        result_ui = mo.md(f"**Failed:** {error_msg}")
                else:
                    result_ui = mo.md("*Not executed*")
                
                command_elements.append(mo.vstack([btn, result_ui]))
        
        # Discovered commands
        if discovered_commands:
            command_elements.append(mo.md("### Discovered Commands"))
            for cmd_info in discovered_commands:
                # Handle both dict format and simple string
                if isinstance(cmd_info, dict):
                    cmd_type = cmd_info.get("commandType", cmd_info.get("name", "unknown"))
                    cmd_desc = cmd_info.get("description", "")
                else:
                    cmd_type = str(cmd_info)
                    cmd_desc = ""
                
                cmd_id = f"discovered_{cmd_type}"

                btn_label = f"Run {cmd_type}"
                if cmd_desc:
                    btn_label += f" - {cmd_desc[:40]}..."

                btn = mo.ui.button(
                    label=btn_label,
                    on_change=lambda _, bc=base_command, c=cmd_type, n=name, cid=cmd_id: run_command(n, bc, c, cid),
                    disabled=not cmd_valid
                )

                # Result display
                result = results.get(cmd_id)
                if result:
                    if result.get("success"):
                        result_ui = mo.vstack([
                            mo.md(f"**Success** | `{result.get('command', '')}`"),
                            detect_and_render_output(result.get("stdout", ""))
                        ])
                    else:
                        error_msg = result.get("error") or result.get("stderr", "Unknown error")
                        result_ui = mo.md(f"**Failed:** {error_msg}")
                else:
                    result_ui = mo.md("*Not executed*")
                
                command_elements.append(mo.vstack([btn, result_ui]))
        
        # No commands message
        if not static_commands and not discovered_commands:
            if discovery.get("enabled"):
                command_elements.append(
                    mo.md("*Click 'Run Discovery' to find available commands.*")
                )
            else:
                command_elements.append(
                    mo.md("*No commands configured for this tool.*")
                )
        
        # Combine all elements
        return mo.vstack(header_elements + command_elements)
    
    # Target path input
    target_input = mo.ui.text(
        value=get_selected_target() or str(root),
        label="Target Path",
        placeholder=str(root),
        on_change=set_selected_target,
        full_width=True
    )
    
    # Build main accordion with all tools
    if manifests:
        accordion_items = {}
        for manifest in manifests:
            name = manifest.get("name", "Unknown")
            icon = manifest.get("icon", "[T]")
            accordion_items[f"{icon} {name}"] = build_tool_accordion(manifest)
        
        tools_accordion = mo.accordion(accordion_items)  # mo.accordion, not mo.ui.accordion
    else:
        tools_accordion = mo.md("*No tool manifests found in registry.*")
    
    # Scan errors display
    errors = get_scan_errors()
    if errors or scan_errors:
        all_errors = list(set(errors + scan_errors))
        error_display = mo.accordion({  # mo.accordion, not mo.ui.accordion
            "Registry Warnings": mo.vstack([
                mo.md(f"- {err}") for err in all_errors
            ])
        })
    else:
        error_display = mo.md("")
    
    # Stats
    stats_text = f"**Tools loaded:** {len(manifests)} | **Registry:** `{REGISTRY_PATH}`"
    
    # Layout
    return mo.vstack([
        mo.md("## Universal Bridge"),
        mo.md("*Dynamically discovers and executes tools from the registry.*"),
        mo.md("---"),
        mo.hstack([target_input], gap="1rem"),
        mo.md(stats_text),
        error_display,
        mo.md("---"),
        tools_accordion,
        mo.md("---"),
        mo.md(f"*Timeout: {DEFAULT_TIMEOUT}s per command | Manifests: `{REGISTRY_PATH}/*.json`*")
    ])
