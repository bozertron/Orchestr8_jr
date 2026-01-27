# IP/plugins/components/file_explorer_panel.py
"""
FileExplorer panel for Marimo.
Provides inline file browsing within maestro, inspired by FileExplorer.vue.
"""
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional
import os
import marimo as mo

# Import Maestro colors for consistency
BLUE_DOMINANT = "#1fbdea"
GOLD_METALLIC = "#D4AF37"
GOLD_DARK = "#B8860B"
GOLD_SAFFRON = "#F4C430"
BG_ELEVATED = "#121214"

# File Explorer CSS - slides from RIGHT (like ticket panel)
FILE_EXPLORER_CSS = f"""
<style>
.file-explorer-overlay {{
    position: fixed;
    top: 0;
    right: 0;
    width: 500px;
    height: 100vh;
    background: {BG_ELEVATED};
    border-left: 1px solid rgba(31, 189, 234, 0.3);
    z-index: 1000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.file-explorer-header {{
    padding: 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.file-explorer-title {{
    color: {GOLD_METALLIC};
    font-family: monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
}}

.file-explorer-close {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.3);
    color: {BLUE_DOMINANT};
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
}}

.file-explorer-close:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}

.file-explorer-breadcrumb {{
    padding: 8px 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.1);
    font-family: monospace;
    font-size: 10px;
    color: {GOLD_DARK};
    overflow-x: auto;
    white-space: nowrap;
}}

.file-explorer-body {{
    flex: 1;
    overflow-y: auto;
    padding: 0;
}}

.file-list {{
    display: flex;
    flex-direction: column;
}}

.file-item {{
    display: flex;
    align-items: center;
    padding: 10px 16px;
    cursor: pointer;
    transition: all 150ms ease-out;
    border-bottom: 1px solid rgba(31, 189, 234, 0.05);
}}

.file-item:hover {{
    background: rgba(212, 175, 55, 0.05);
}}

.file-item.selected {{
    background: rgba(212, 175, 55, 0.1);
    border-left: 2px solid {GOLD_METALLIC};
}}

.file-item.directory {{
    color: {GOLD_METALLIC};
}}

.file-icon {{
    width: 24px;
    font-size: 14px;
    margin-right: 8px;
}}

.file-name {{
    flex: 1;
    font-size: 11px;
    color: #e8e8e8;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.file-item.directory .file-name {{
    color: {GOLD_METALLIC};
}}

.file-size {{
    font-family: monospace;
    font-size: 9px;
    color: #666;
    margin-left: 8px;
}}

.file-date {{
    font-family: monospace;
    font-size: 9px;
    color: #666;
    margin-left: 12px;
    min-width: 80px;
}}

.file-explorer-footer {{
    padding: 12px 16px;
    border-top: 1px solid rgba(31, 189, 234, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(18, 18, 20, 0.95);
}}

.selection-info {{
    font-family: monospace;
    font-size: 10px;
    color: {GOLD_DARK};
}}

.explorer-btn {{
    background: rgba(212, 175, 55, 0.1);
    border: 1px solid {GOLD_METALLIC};
    color: {GOLD_METALLIC};
    padding: 6px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    transition: all 150ms ease-out;
}}

.explorer-btn:hover {{
    background: rgba(212, 175, 55, 0.2);
}}

.explorer-btn:disabled {{
    opacity: 0.5;
    cursor: not-allowed;
}}

.empty-dir {{
    padding: 40px;
    text-align: center;
    color: #666;
    font-style: italic;
}}

.quick-nav {{
    display: flex;
    gap: 8px;
    padding: 8px 16px;
    border-bottom: 1px solid rgba(31, 189, 234, 0.1);
}}

.quick-nav-btn {{
    background: transparent;
    border: 1px solid rgba(31, 189, 234, 0.2);
    color: #999;
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-family: monospace;
    font-size: 9px;
}}

.quick-nav-btn:hover {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
}}

.quick-nav-btn.active {{
    color: {GOLD_METALLIC};
    border-color: {GOLD_METALLIC};
    background: rgba(212, 175, 55, 0.1);
}}
</style>
"""


class FileExplorerPanel:
    """File Explorer panel for Marimo, inspired by FileExplorer.vue."""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self._is_visible = False
        self._current_path = self.project_root
        self._selected_paths: List[str] = []

        # Quick navigation locations
        self.locations = [
            ("HOME", Path.home()),
            ("PROJECT", self.project_root),
            ("DOCS", Path.home() / "Documents"),
            ("DOWN", Path.home() / "Downloads"),
        ]

    def toggle_visibility(self) -> None:
        """Toggle panel visibility."""
        self._is_visible = not self._is_visible

    def set_visible(self, visible: bool) -> None:
        """Set panel visibility."""
        self._is_visible = visible

    def is_visible(self) -> bool:
        """Check if panel is visible."""
        return self._is_visible

    def navigate_to(self, path: str) -> None:
        """Navigate to a directory."""
        new_path = Path(path).resolve()
        if new_path.is_dir():
            self._current_path = new_path
            self._selected_paths = []

    def navigate_up(self) -> None:
        """Navigate to parent directory."""
        parent = self._current_path.parent
        if parent != self._current_path:
            self._current_path = parent
            self._selected_paths = []

    def select_path(self, path: str) -> None:
        """Toggle selection of a path."""
        if path in self._selected_paths:
            self._selected_paths.remove(path)
        else:
            self._selected_paths.append(path)

    def clear_selection(self) -> None:
        """Clear all selections."""
        self._selected_paths = []

    def get_selected_paths(self) -> List[str]:
        """Get list of selected paths."""
        return self._selected_paths

    def get_entries(self) -> List[dict]:
        """Get directory entries for current path."""
        entries = []
        try:
            for item in sorted(self._current_path.iterdir()):
                # Skip hidden files and common ignored dirs
                if item.name.startswith("."):
                    continue
                if item.name in ["node_modules", "__pycache__", ".git", "target"]:
                    continue

                try:
                    stat = item.stat()
                    entries.append({
                        "name": item.name,
                        "path": str(item),
                        "is_directory": item.is_dir(),
                        "size": stat.st_size if item.is_file() else None,
                        "modified_at": datetime.fromtimestamp(stat.st_mtime),
                    })
                except (PermissionError, OSError):
                    continue

            # Sort: directories first, then files
            entries.sort(key=lambda e: (not e["is_directory"], e["name"].lower()))

        except PermissionError:
            pass

        return entries

    def render(self) -> Any:
        """Render the file explorer panel."""
        if not self._is_visible:
            return mo.md("")

        entries = self.get_entries()

        # Build HTML
        panel_html = f"""
        <div class="file-explorer-overlay">
            <div class="file-explorer-header">
                <span class="file-explorer-title">FILE EXPLORER</span>
                <button class="file-explorer-close" onclick="window.location.reload()">X</button>
            </div>
            {self._build_quick_nav()}
            <div class="file-explorer-breadcrumb">
                {self._build_breadcrumb()}
            </div>
            <div class="file-explorer-body">
                {self._build_file_list(entries)}
            </div>
            <div class="file-explorer-footer">
                {self._build_footer()}
            </div>
        </div>
        """

        return mo.Html(FILE_EXPLORER_CSS + panel_html)

    def _build_quick_nav(self) -> str:
        """Build quick navigation bar."""
        buttons = ""
        for name, path in self.locations:
            is_active = self._current_path == path
            buttons += f"""
            <button class="quick-nav-btn {'active' if is_active else ''}"
                    title="{path}">
                {name}
            </button>
            """
        return f'<div class="quick-nav">{buttons}</div>'

    def _build_breadcrumb(self) -> str:
        """Build breadcrumb navigation."""
        parts = []
        path = self._current_path

        # Build path parts
        while path != path.parent:
            parts.append(path.name)
            path = path.parent

        # Add root
        if str(self._current_path).startswith("/"):
            parts.append("/")

        parts.reverse()
        return " > ".join(parts[-5:])  # Show last 5 parts

    def _build_file_list(self, entries: List[dict]) -> str:
        """Build file list HTML."""
        if not entries:
            return '<div class="empty-dir">DIRECTORY IS EMPTY</div>'

        items = ""
        for entry in entries:
            is_selected = entry["path"] in self._selected_paths
            is_dir = entry["is_directory"]

            icon = self._get_icon(entry)
            size = self._format_size(entry.get("size"))
            date = self._format_date(entry.get("modified_at"))

            items += f"""
            <div class="file-item {'selected' if is_selected else ''} {'directory' if is_dir else ''}"
                 data-path="{entry['path']}">
                <span class="file-icon">{icon}</span>
                <span class="file-name">{entry['name']}</span>
                <span class="file-size">{size}</span>
                <span class="file-date">{date}</span>
            </div>
            """

        return f'<div class="file-list">{items}</div>'

    def _build_footer(self) -> str:
        """Build footer with selection info and actions."""
        count = len(self._selected_paths)
        selection_text = f"{count} ITEM{'S' if count != 1 else ''} SELECTED" if count else ""

        return f"""
        <span class="selection-info">{selection_text}</span>
        <button class="explorer-btn" {'disabled' if count == 0 else ''}>
            ADD TO CHAT
        </button>
        """

    def _get_icon(self, entry: dict) -> str:
        """Get icon for file entry."""
        if entry["is_directory"]:
            return "\U0001F4C1"  # folder

        name = entry["name"].lower()
        ext = name.split(".")[-1] if "." in name else ""

        icons = {
            "md": "\U0001F4C4",  # document
            "txt": "\U0001F4C4",
            "py": "\U0001F40D",  # snake
            "js": "\U0001F4DC",  # scroll
            "ts": "\U0001F4DC",
            "vue": "\U0001F4DC",
            "rs": "\U00002699",  # gear
            "toml": "\U00002699",
            "json": "\U00002699",
            "png": "\U0001F5BC",  # picture
            "jpg": "\U0001F5BC",
            "svg": "\U0001F5BC",
        }

        return icons.get(ext, "\U000025C7")  # diamond

    def _format_size(self, size: Optional[int]) -> str:
        """Format file size."""
        if size is None:
            return "--"
        if size == 0:
            return "0 B"

        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024

        return f"{size:.1f} TB"

    def _format_date(self, dt: Optional[datetime]) -> str:
        """Format modification date."""
        if dt is None:
            return "--"
        return dt.strftime("%m/%d %H:%M")
