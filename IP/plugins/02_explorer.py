"""
02_explorer Plugin - File Explorer with Carl Integration
Orchestr8 v3.0 - The Fortress Factory

An interactive file explorer that displays project files in a table
with deep scan capabilities using Carl core for context analysis.

Features:
    - File tree visualization in table format
    - Single-row selection for file focus
    - Deep scan using carl_core.run_deep_scan()
    - Context panel for selected file details
    - Status badges for file states
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

PLUGIN_NAME = "Explorer"
PLUGIN_ORDER = 2

# File type icons - text based
FILE_ICONS = {
    'py': '[py]',
    'ts': '[ts]',
    'js': '[js]',
    'json': '[json]',
    'md': '[md]',
    'txt': '[txt]',
    'yaml': '[yaml]',
    'yml': '[yml]',
    'toml': '[toml]',
    'sql': '[sql]',
    'css': '[css]',
    'html': '[html]',
    'vue': '[vue]',
    'svelte': '[svelte]',
    'default': '[file]'
}

# Directories to ignore
IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    'dist', 'build', '.next', '.nuxt', 'coverage', '.pytest_cache',
    '.mypy_cache', 'eggs', '.tox', '.DS_Store'
}

def get_file_icon(filename):
    """Get icon for file based on extension."""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    return FILE_ICONS.get(ext, FILE_ICONS['default'])

def format_size(size_bytes):
    """Format file size for display."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}MB"

def scan_directory(root_path, max_depth=5):
    """Scan directory and return file list."""
    files = []
    root = Path(root_path)
    
    if not root.exists():
        return files
    
    def scan(path, depth=0):
        if depth > max_depth:
            return
        
        try:
            for item in sorted(path.iterdir()):
                if item.name in IGNORE_DIRS or item.name.startswith('.'):
                    continue
                
                rel_path = item.relative_to(root)
                
                if item.is_dir():
                    files.append({
                        'icon': '[dir]',
                        'name': item.name,
                        'path': str(rel_path),
                        'type': 'directory',
                        'size': '-',
                        'modified': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                    })
                    scan(item, depth + 1)
                else:
                    stat = item.stat()
                    files.append({
                        'icon': get_file_icon(item.name),
                        'name': item.name,
                        'path': str(rel_path),
                        'type': 'file',
                        'size': format_size(stat.st_size),
                        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    })
        except PermissionError:
            pass
    
    scan(root)
    return files

def render(STATE_MANAGERS):
    """Render the file explorer with Carl integration."""
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_files, set_files = STATE_MANAGERS["files"]
    get_selected, set_selected = STATE_MANAGERS["selected"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    # Local state for scan results
    get_scan_result, set_scan_result = mo.state(None)
    get_is_scanning, set_is_scanning = mo.state(False)
    
    root = get_root()
    files = get_files()
    selected = get_selected()
    
    # Scan function
    def do_scan():
        set_is_scanning(True)
        try:
            # Basic file scan
            scanned_files = scan_directory(root)
            set_files(scanned_files)
            
            # Log the scan
            logs = get_logs()
            set_logs(logs + [f"[Explorer] Scanned {len(scanned_files)} items in {root}"])
            
            # Try deep scan with Carl if available
            try:
                from carl_core import CarlContextualizer
                carl = CarlContextualizer(root)
                context = carl.run_deep_scan()
                set_scan_result(context)
                logs = get_logs()
                set_logs(logs + [f"[Explorer] Deep scan completed via Carl"])
            except ImportError:
                pass
            except Exception as e:
                logs = get_logs()
                set_logs(logs + [f"[Explorer] Carl deep scan failed: {str(e)}"])
        finally:
            set_is_scanning(False)
    
    # Scan button
    scan_btn = mo.ui.button(
        label="Scan Project" if not get_is_scanning() else "Scanning...",
        on_change=lambda _: do_scan(),
        disabled=get_is_scanning()
    )
    
    # Build table data
    if files:
        # Create selectable table
        table_data = [
            {
                "": f['icon'],
                "Name": f['name'],
                "Path": f['path'],
                "Type": f['type'],
                "Size": f['size'],
                "Modified": f['modified']
            }
            for f in files
        ]
        
        file_table = mo.ui.table(
            data=table_data,
            selection="single",
            label="Project Files",
            on_change=lambda selected_rows: handle_selection(selected_rows)
        )
        
        def handle_selection(selected_rows):
            if selected_rows and len(selected_rows) > 0:
                row = selected_rows[0]
                file_path = row.get('Path', '')
                set_selected(file_path)
                logs = get_logs()
                set_logs(logs + [f"[Explorer] Selected: {file_path}"])
    else:
        file_table = mo.md("*No files scanned yet. Click 'Scan Project' to begin.*")
    
    # Context panel for selected file
    def build_context_panel():
        if not selected:
            return mo.md("*Select a file to view details*")
        
        full_path = Path(root) / selected
        
        if not full_path.exists():
            return mo.md(f"*File not found: {selected}*")
        
        # Get file info
        stat = full_path.stat()
        is_file = full_path.is_file()
        
        # Build context info
        info_lines = [
            f"### {full_path.name}",
            f"",
            f"**Path:** `{selected}`",
            f"**Type:** {'File' if is_file else 'Directory'}",
            f"**Size:** {format_size(stat.st_size) if is_file else 'N/A'}",
            f"**Modified:** {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        
        # Show preview for small text files
        if is_file and stat.st_size < 10000:
            try:
                ext = full_path.suffix.lower()
                if ext in ['.py', '.ts', '.js', '.json', '.md', '.txt', '.yaml', '.yml', '.toml']:
                    content = full_path.read_text()[:2000]
                    info_lines.extend([
                        "",
                        "**Preview:**",
                        f"```{ext[1:]}",
                        content,
                        "```"
                    ])
            except:
                pass
        
        # Show deep scan context if available
        scan_result = get_scan_result()
        if scan_result and isinstance(scan_result, dict):
            if 'context' in scan_result:
                info_lines.extend([
                    "",
                    "**Deep Scan Context:**",
                    f"```json",
                    json.dumps(scan_result.get('context', {}), indent=2)[:1000],
                    "```"
                ])
        
        return mo.md("\n".join(info_lines))
    
    context_panel = build_context_panel()
    
    # Stats bar
    file_count = len([f for f in (files or []) if f['type'] == 'file'])
    dir_count = len([f for f in (files or []) if f['type'] == 'directory'])
    stats = mo.md(f"**Files:** {file_count} | **Directories:** {dir_count} | **Root:** `{root}`")
    
    # Layout
    return mo.vstack([
        mo.md("## Project Explorer"),
        mo.hstack([scan_btn, stats], justify="space-between", align="center"),
        mo.md("---"),
        mo.hstack([
            mo.vstack([file_table], style={"flex": "2"}),
            mo.vstack([context_panel], style={"flex": "1", "padding-left": "1rem"})
        ], gap="1rem"),
    ])
