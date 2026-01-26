"""
03_gatekeeper Plugin - Louis File Protection UI
Orchestr8 v3.0 - The Fortress Factory

Provides a UI interface for Louis file protection system using
LouisWarden and LouisConfig from louis_core.py.

Features:
    - Protection status badge display
    - Lock/Unlock All Protected buttons
    - Per-file toggle checkboxes
    - Git hook installation
    - Protection log viewer

Permissions:
    - Locked: 0o444 (read-only)
    - Unlocked: 0o644 (read-write)

Uses: LouisWarden, LouisConfig from IP/louis_core.py
"""

from pathlib import Path
from typing import Any

# Import Louis Core components
from IP.louis_core import LouisWarden, LouisConfig

PLUGIN_NAME = "🛡️ Gatekeeper"
PLUGIN_ORDER = 3


def render(STATE_MANAGERS: dict) -> Any:
    """
    Render the Gatekeeper protection UI.
    
    Args:
        STATE_MANAGERS: Dictionary of state getters/setters
        
    Returns:
        Marimo UI element
    """
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    # Initialize LouisConfig with project root
    root = get_root()
    config = LouisConfig(root)
    warden = LouisWarden(config)
    
    # Local state
    get_new_path, set_new_path = mo.state("")
    get_refresh_trigger, set_refresh_trigger = mo.state(0)
    get_selected_files, set_selected_files = mo.state(set())
    
    def log_message(msg: str) -> None:
        """Add message to logs."""
        logs = get_logs()
        set_logs(logs + [f"[Gatekeeper] {msg}"])
    
    def trigger_refresh() -> None:
        """Force UI refresh."""
        set_refresh_trigger(get_refresh_trigger() + 1)
    
    # Get current protection status
    protection_status = warden.get_protection_status()
    total_protected = len(protection_status)
    locked_count = sum(1 for s in protection_status.values() if s.get("locked"))
    unlocked_count = total_protected - locked_count
    
    # Status badge
    if total_protected == 0:
        status_label = "⚪ Unprotected"
        status_detail = "No files in protection list"
    elif locked_count == total_protected:
        status_label = "🟢 Fully Locked"
        status_detail = f"All {total_protected} files locked (0o444)"
    elif locked_count > 0:
        status_label = "🟡 Partial"
        status_detail = f"{locked_count} locked, {unlocked_count} unlocked"
    else:
        status_label = "🔓 Unlocked"
        status_detail = f"{total_protected} files tracked but unlocked"
    
    # Check git hook
    hook_path = Path(root) / ".git" / "hooks" / "pre-commit"
    hook_installed = hook_path.exists() and "louis" in hook_path.read_text().lower() if hook_path.exists() else False
    
    status_badge = mo.md(f"""
### Protection Status: {status_label}

{status_detail}

**Protected Folders:** {len(config.protected_folders)}  
**Git Hook:** {'✅ Installed' if hook_installed else '❌ Not Installed'}
    """)
    
    # === Action Handlers ===
    
    def lock_all_protected() -> None:
        """Lock all files in the protection list."""
        count = 0
        for rel_path in protection_status.keys():
            success, msg = warden.lock_file(rel_path)
            if success:
                count += 1
        log_message(f"Locked {count} files (0o444)")
        trigger_refresh()
    
    def unlock_all_protected() -> None:
        """Unlock all files in the protection list."""
        count = 0
        for rel_path in protection_status.keys():
            success, msg = warden.unlock_file(rel_path)
            if success:
                count += 1
        log_message(f"Unlocked {count} files (0o644)")
        trigger_refresh()
    
    def lock_selected() -> None:
        """Lock only selected files."""
        selected = get_selected_files()
        count = 0
        for rel_path in selected:
            success, msg = warden.lock_file(rel_path)
            if success:
                count += 1
        log_message(f"Locked {count} selected files")
        trigger_refresh()
    
    def unlock_selected() -> None:
        """Unlock only selected files."""
        selected = get_selected_files()
        count = 0
        for rel_path in selected:
            success, msg = warden.unlock_file(rel_path)
            if success:
                count += 1
        log_message(f"Unlocked {count} selected files")
        trigger_refresh()
    
    def add_protected_folder() -> None:
        """Add a folder to protection list."""
        folder = get_new_path().strip().rstrip('/')
        if not folder:
            return
        
        if folder not in config.protected_folders:
            config.protected_folders.append(folder)
            config.save()
            # Rescan to update protected files list
            file_count = warden.scan_and_protect()
            log_message(f"Added '{folder}' - {file_count} files now tracked")
        else:
            log_message(f"'{folder}' already protected")
        
        set_new_path("")
        trigger_refresh()
    
    def remove_folder(folder: str) -> None:
        """Remove a folder from protection list."""
        if folder in config.protected_folders:
            config.protected_folders.remove(folder)
            config.save()
            warden.scan_and_protect()
            log_message(f"Removed '{folder}' from protection")
        trigger_refresh()
    
    def rescan_files() -> None:
        """Rescan protected folders and update file list."""
        count = warden.scan_and_protect()
        log_message(f"Rescanned: {count} files now tracked")
        trigger_refresh()
    
    def install_hook() -> None:
        """Install Louis git pre-commit hook."""
        success, msg = warden.install_git_hook()
        log_message(msg)
        trigger_refresh()
    
    def toggle_file_selection(rel_path: str, checked: bool) -> None:
        """Toggle file selection state."""
        selected = get_selected_files().copy()
        if checked:
            selected.add(rel_path)
        else:
            selected.discard(rel_path)
        set_selected_files(selected)
    
    # === UI Components ===
    
    # Add folder input
    folder_input = mo.ui.text(
        value=get_new_path(),
        label="Folder to Protect",
        placeholder="src/core or config/secrets",
        on_change=set_new_path,
        full_width=True
    )
    
    add_folder_btn = mo.ui.button(
        label="📁 Add Folder",
        on_change=lambda _: add_protected_folder()
    )
    
    # Bulk action buttons
    lock_all_btn = mo.ui.button(
        label="🔒 Lock All Protected",
        on_change=lambda _: lock_all_protected(),
        disabled=total_protected == 0
    )
    
    unlock_all_btn = mo.ui.button(
        label="🔓 Unlock All",
        on_change=lambda _: unlock_all_protected(),
        disabled=total_protected == 0
    )
    
    rescan_btn = mo.ui.button(
        label="🔄 Rescan Files",
        on_change=lambda _: rescan_files()
    )
    
    install_hook_btn = mo.ui.button(
        label="📥 Install Git Hook",
        on_change=lambda _: install_hook(),
        disabled=hook_installed
    )
    
    # Selected file actions
    selected = get_selected_files()
    selected_count = len(selected)
    
    lock_selected_btn = mo.ui.button(
        label=f"🔒 Lock Selected ({selected_count})",
        on_change=lambda _: lock_selected(),
        disabled=selected_count == 0
    )
    
    unlock_selected_btn = mo.ui.button(
        label=f"🔓 Unlock Selected ({selected_count})",
        on_change=lambda _: unlock_selected(),
        disabled=selected_count == 0
    )
    
    # Protected folders display
    folders_md = "### Protected Folders\n\n"
    if config.protected_folders:
        for folder in config.protected_folders:
            folders_md += f"- 📁 `{folder}` "
            # Note: Can't easily add remove buttons inline in MD
        folders_md += "\n\n*Use the input above to add folders.*"
    else:
        folders_md += "*No folders protected. Add folders above.*"
    
    folders_display = mo.md(folders_md)
    
    # File list with checkboxes
    def build_file_checkboxes() -> Any:
        """Build checkbox list for protected files."""
        if not protection_status:
            return mo.md("*No files tracked. Add folders and click 'Rescan Files'.*")
        
        file_elements = []
        sorted_files = sorted(protection_status.items())
        
        for rel_path, status in sorted_files:
            is_locked = status.get("locked", False)
            lock_icon = "🔒" if is_locked else "🔓"
            is_selected = rel_path in selected
            
            # Create checkbox for selection
            checkbox = mo.ui.checkbox(
                value=is_selected,
                label=f"{lock_icon} `{rel_path}`",
                on_change=lambda checked, path=rel_path: toggle_file_selection(path, checked)
            )
            file_elements.append(checkbox)
        
        return mo.vstack(file_elements)
    
    file_list = build_file_checkboxes()
    
    # Layout
    return mo.vstack([
        mo.md("## 🛡️ Louis Gatekeeper"),
        status_badge,
        mo.md("---"),
        
        # Add folder section
        mo.hstack([folder_input, add_folder_btn], gap="0.5rem"),
        
        # Bulk actions
        mo.md("**Bulk Actions:**"),
        mo.hstack([lock_all_btn, unlock_all_btn, rescan_btn, install_hook_btn], gap="0.5rem"),
        
        # Selected actions
        mo.md("**Selected File Actions:**"),
        mo.hstack([lock_selected_btn, unlock_selected_btn], gap="0.5rem"),
        
        mo.md("---"),
        folders_display,
        
        mo.md("---"),
        mo.md("### Protected Files"),
        file_list,
        
        mo.md("---"),
        mo.md(f"*Config: `~/.louis-control/` | Locked: 0o444 | Unlocked: 0o644*")
    ])
