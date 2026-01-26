"""
03_gatekeeper Plugin - Louis File Protection UI
Orchestr8 v3.0 - The Fortress Factory

Provides a UI interface for Louis file protection system.
Allows users to manage protected paths, install git hooks,
and monitor protection status.

Features:
    - Protection status badge display
    - Lock/Unlock path management
    - Git hook installation
    - Protection log viewer
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

PLUGIN_NAME = "🛡️ Gatekeeper"
PLUGIN_ORDER = 3

# Default Louis config location
LOUIS_CONFIG_DIR = ".louis-control"
LOUIS_CONFIG_FILE = "louis-config.json"

def load_louis_config(root_path):
    """Load Louis configuration from project root."""
    config_path = Path(root_path) / LOUIS_CONFIG_DIR / LOUIS_CONFIG_FILE
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Return default config
    return {
        "protected_paths": [],
        "protected_folders": [],
        "ignore_patterns": ["node_modules", ".git", "__pycache__", "dist"]
    }

def save_louis_config(root_path, config):
    """Save Louis configuration to project root."""
    config_dir = Path(root_path) / LOUIS_CONFIG_DIR
    config_path = config_dir / LOUIS_CONFIG_FILE
    
    config_dir.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def get_protection_status(root_path):
    """Get current protection status."""
    config = load_louis_config(root_path)
    
    total_protected = len(config.get("protected_paths", [])) + len(config.get("protected_folders", []))
    
    if total_protected == 0:
        return "⚪ Unprotected", "No paths or folders protected"
    elif total_protected < 5:
        return "🟡 Partial", f"{total_protected} items protected"
    else:
        return "🟢 Active", f"{total_protected} items protected"

def check_git_hook_installed(root_path):
    """Check if Louis git hook is installed."""
    hook_path = Path(root_path) / ".git" / "hooks" / "pre-commit"
    
    if hook_path.exists():
        try:
            content = hook_path.read_text()
            return "louis" in content.lower() or "gatekeeper" in content.lower()
        except:
            pass
    
    return False

def install_git_hook(root_path):
    """Install Louis protection git hook."""
    git_dir = Path(root_path) / ".git"
    
    if not git_dir.exists():
        return False, "Not a git repository"
    
    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    
    hook_path = hooks_dir / "pre-commit"
    
    hook_script = '''#!/bin/bash
# Louis Gatekeeper - Pre-commit protection hook
# Orchestr8 v3.0

echo "🛡️ Louis Gatekeeper: Checking protected files..."

# Load config
CONFIG_FILE=".louis-control/louis-config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "No Louis config found, allowing commit."
    exit 0
fi

# Check if any protected files are being modified
PROTECTED_PATHS=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; config = json.load(sys.stdin); print('\\n'.join(config.get('protected_paths', []) + config.get('protected_folders', [])))")

STAGED_FILES=$(git diff --cached --name-only)

for protected in $PROTECTED_PATHS; do
    for staged in $STAGED_FILES; do
        if [[ "$staged" == "$protected"* ]]; then
            echo "❌ BLOCKED: Attempting to modify protected path: $staged"
            echo "   To override, use: git commit --no-verify"
            exit 1
        fi
    done
done

echo "✅ Louis Gatekeeper: All clear."
exit 0
'''
    
    try:
        hook_path.write_text(hook_script)
        hook_path.chmod(0o755)
        return True, "Git hook installed successfully"
    except Exception as e:
        return False, str(e)

def render(STATE_MANAGERS):
    """Render the Gatekeeper protection UI."""
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    # Local state
    get_config, set_config = mo.state(None)
    get_new_path, set_new_path = mo.state("")
    
    root = get_root()
    
    # Load config on first render
    if get_config() is None:
        set_config(load_louis_config(root))
    
    config = get_config() or load_louis_config(root)
    
    # Status badge
    status_label, status_detail = get_protection_status(root)
    hook_installed = check_git_hook_installed(root)
    
    status_badge = mo.md(f"""
### Protection Status: {status_label}

{status_detail}

**Git Hook:** {'✅ Installed' if hook_installed else '❌ Not Installed'}
    """)
    
    # Protected paths list
    protected_paths = config.get("protected_paths", [])
    protected_folders = config.get("protected_folders", [])
    
    paths_md = "**Protected Paths:**\n"
    if protected_paths:
        paths_md += "\n".join([f"- 📄 `{p}`" for p in protected_paths])
    else:
        paths_md += "*No paths protected*"
    
    paths_md += "\n\n**Protected Folders:**\n"
    if protected_folders:
        paths_md += "\n".join([f"- 📁 `{f}`" for f in protected_folders])
    else:
        paths_md += "*No folders protected*"
    
    protected_list = mo.md(paths_md)
    
    # Add path input
    new_path_input = mo.ui.text(
        value=get_new_path(),
        label="Path to Protect",
        placeholder="src/core/critical.py or config/",
        on_change=set_new_path
    )
    
    # Protection type selector
    path_type_select = mo.ui.dropdown(
        options=["File Path", "Folder"],
        value="File Path",
        label="Protection Type"
    )
    
    # Action handlers
    def add_protection():
        path = get_new_path()
        if not path:
            return
        
        current_config = get_config() or load_louis_config(root)
        
        # Determine if it's a file or folder
        is_folder = path.endswith('/') or (Path(root) / path).is_dir()
        
        if is_folder:
            path = path.rstrip('/')
            if path not in current_config.get("protected_folders", []):
                current_config.setdefault("protected_folders", []).append(path)
        else:
            if path not in current_config.get("protected_paths", []):
                current_config.setdefault("protected_paths", []).append(path)
        
        save_louis_config(root, current_config)
        set_config(current_config)
        set_new_path("")
        
        logs = get_logs()
        set_logs(logs + [f"[Gatekeeper] Protected: {path}"])
    
    def clear_all_protection():
        current_config = get_config() or load_louis_config(root)
        current_config["protected_paths"] = []
        current_config["protected_folders"] = []
        save_louis_config(root, current_config)
        set_config(current_config)
        
        logs = get_logs()
        set_logs(logs + [f"[Gatekeeper] Cleared all protection"])
    
    def do_install_hook():
        success, message = install_git_hook(root)
        logs = get_logs()
        if success:
            set_logs(logs + [f"[Gatekeeper] {message}"])
        else:
            set_logs(logs + [f"[Gatekeeper] Hook install failed: {message}"])
    
    def scan_and_protect():
        """Scan project and suggest protection for critical files."""
        critical_patterns = [
            "config/", "secrets/", ".env", "credentials",
            "core/", "auth/", "security/"
        ]
        
        current_config = get_config() or load_louis_config(root)
        added = []
        
        root_path = Path(root)
        for pattern in critical_patterns:
            search_path = root_path / pattern.rstrip('/')
            if search_path.exists():
                if search_path.is_dir():
                    if pattern not in current_config.get("protected_folders", []):
                        current_config.setdefault("protected_folders", []).append(pattern.rstrip('/'))
                        added.append(pattern)
                else:
                    if pattern not in current_config.get("protected_paths", []):
                        current_config.setdefault("protected_paths", []).append(pattern)
                        added.append(pattern)
        
        if added:
            save_louis_config(root, current_config)
            set_config(current_config)
            logs = get_logs()
            set_logs(logs + [f"[Gatekeeper] Auto-protected {len(added)} critical paths"])
    
    # Buttons
    add_btn = mo.ui.button(
        label="🔒 Lock Path",
        on_change=lambda _: add_protection()
    )
    
    clear_btn = mo.ui.button(
        label="🔓 Clear All",
        on_change=lambda _: clear_all_protection()
    )
    
    install_hook_btn = mo.ui.button(
        label="📥 Install Git Hook",
        on_change=lambda _: do_install_hook(),
        disabled=hook_installed
    )
    
    auto_scan_btn = mo.ui.button(
        label="🔍 Auto-Protect Critical",
        on_change=lambda _: scan_and_protect()
    )
    
    # Layout
    return mo.vstack([
        mo.md("## 🛡️ Louis Gatekeeper"),
        status_badge,
        mo.md("---"),
        mo.hstack([new_path_input, add_btn], gap="0.5rem"),
        mo.hstack([auto_scan_btn, install_hook_btn, clear_btn], gap="0.5rem"),
        mo.md("---"),
        protected_list,
        mo.md("---"),
        mo.md(f"*Config location: `{LOUIS_CONFIG_DIR}/{LOUIS_CONFIG_FILE}`*")
    ])
