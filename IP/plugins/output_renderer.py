"""
Output Renderer - Smart JSON/Text Rendering Utility

Orchestr8 v3.0 - The Fortress Factory

Provides intelligent output rendering for CLI command results.
Detects JSON content and renders appropriately:
- JSON arrays → sortable mo.ui.table
- JSON objects → mo.ui.json or formatted text
- Plain text → mo.ui.text_area
- Large arrays (>1000 rows) → paginated view

Usage:
    from IP.plugins.output_renderer import detect_and_render_output
    output_element = detect_and_render_output(stdout_text)

Requires: Python 3.12+, marimo
"""

import json
from json.decoder import JSONDecodeError
from typing import Any, Union

# Pagination threshold for large datasets
PAGINATION_THRESHOLD = 1000
DEFAULT_PAGE_SIZE = 100


def detect_and_render_output(stdout_text: str, page: int = 0) -> Any:
    """
    Detect output type and render appropriately using Marimo UI components.
    
    Args:
        stdout_text: Raw text output from a CLI command (stdout)
        page: Page number for paginated results (0-indexed)
    
    Returns:
        Marimo UI element (mo.ui.table, mo.ui.json, mo.ui.text_area, or mo.vstack)
    
    Rendering Logic:
        1. Try to parse as JSON
        2. If JSON array: render as sortable mo.ui.table (paginated if >1000 rows)
        3. If JSON object: render as mo.ui.json or formatted text_area
        4. If not JSON: render as mo.ui.text_area (plain text fallback)
    
    Example:
        >>> output = detect_and_render_output('[{"name": "test"}]')
        >>> # Returns mo.ui.table with sortable columns
    """
    import marimo as mo
    
    # Handle empty input
    if not stdout_text or not stdout_text.strip():
        return mo.ui.text_area(
            value="(No output)",
            disabled=True,
            full_width=True
        )
    
    # Try to parse as JSON
    try:
        json_data = json.loads(stdout_text)
        return _render_json(json_data, mo, page)
    except JSONDecodeError:
        # Not valid JSON - render as plain text
        return _render_text(stdout_text, mo)


def _render_json(json_data: Any, mo: Any, page: int = 0) -> Any:
    """
    Render parsed JSON data using appropriate Marimo component.
    
    Args:
        json_data: Parsed JSON (list, dict, or primitive)
        mo: Marimo module reference
        page: Current page for pagination
    
    Returns:
        Marimo UI element
    """
    # JSON Array → Table
    if isinstance(json_data, list):
        return _render_json_array(json_data, mo, page)
    
    # JSON Object → JSON viewer or formatted text
    elif isinstance(json_data, dict):
        return _render_json_object(json_data, mo)
    
    # Primitive (string, number, bool, null) → text area
    else:
        return mo.ui.text_area(
            value=json.dumps(json_data, indent=2),
            disabled=True,
            full_width=True
        )


def _render_json_array(data: list, mo: Any, page: int = 0) -> Any:
    """
    Render JSON array as sortable table with pagination for large datasets.
    
    Args:
        data: List of items (typically list of dicts)
        mo: Marimo module reference
        page: Current page number (0-indexed)
    
    Returns:
        mo.ui.table for small arrays, or mo.vstack with pagination for large
    """
    # Empty array
    if not data:
        return mo.ui.text_area(
            value="[]  (empty array)",
            disabled=True,
            full_width=True
        )
    
    # Check if array contains objects (for table rendering)
    if not all(isinstance(item, dict) for item in data):
        # Array of primitives - render as formatted JSON
        return mo.ui.text_area(
            value=json.dumps(data, indent=2),
            disabled=True,
            full_width=True
        )
    
    total_rows = len(data)
    
    # Small dataset - render directly as table
    if total_rows <= PAGINATION_THRESHOLD:
        return mo.ui.table(
            data=data,
            pagination=True,
            page_size=DEFAULT_PAGE_SIZE,
            selection=None
        )
    
    # Large dataset - paginated view with info
    total_pages = (total_rows + PAGINATION_THRESHOLD - 1) // PAGINATION_THRESHOLD
    current_page = min(page, total_pages - 1)
    start_idx = current_page * PAGINATION_THRESHOLD
    end_idx = min(start_idx + PAGINATION_THRESHOLD, total_rows)
    
    page_data = data[start_idx:end_idx]
    
    info_text = f"Showing rows {start_idx + 1}-{end_idx} of {total_rows} (Page {current_page + 1}/{total_pages})"
    
    return mo.vstack([
        mo.md(f"**{info_text}**"),
        mo.ui.table(
            data=page_data,
            pagination=True,
            page_size=DEFAULT_PAGE_SIZE,
            selection=None
        ),
        mo.md(f"*Large dataset: {total_rows} rows total. Use page parameter to navigate.*")
    ])


def _render_json_object(data: dict, mo: Any) -> Any:
    """
    Render JSON object using mo.ui.json or formatted text.
    
    Args:
        data: Dictionary to render
        mo: Marimo module reference
    
    Returns:
        mo.ui.json for small objects, mo.ui.text_area for large
    """
    # Empty object
    if not data:
        return mo.ui.text_area(
            value="{}  (empty object)",
            disabled=True,
            full_width=True
        )
    
    # Check if object is reasonably sized for JSON viewer
    json_str = json.dumps(data, indent=2)
    
    if len(json_str) < 10000:  # ~10KB threshold
        # Use collapsible JSON viewer for smaller objects
        try:
            return mo.accordion({
                "JSON Output": mo.ui.text_area(
                    value=json_str,
                    disabled=True,
                    full_width=True,
                    rows=min(json_str.count('\n') + 1, 30)
                )
            })
        except Exception:
            # Fallback to text area if accordion fails
            pass
    
    # Large object - use text area with scrolling
    return mo.ui.text_area(
        value=json_str,
        disabled=True,
        full_width=True,
        rows=30
    )


def _render_text(text: str, mo: Any) -> Any:
    """
    Render plain text output.
    
    Args:
        text: Plain text content
        mo: Marimo module reference
    
    Returns:
        mo.ui.text_area element
    """
    lines = text.count('\n') + 1
    return mo.ui.text_area(
        value=text,
        disabled=True,
        full_width=True,
        rows=min(lines, 30)  # Cap at 30 visible rows
    )


# Convenience function for rendering with status
def render_command_output(
    stdout: str,
    stderr: str = "",
    exit_code: int = 0,
    command: str = ""
) -> Any:
    """
    Render complete command output with status information.
    
    Args:
        stdout: Standard output text
        stderr: Standard error text
        exit_code: Command exit code
        command: The command that was executed
    
    Returns:
        mo.vstack with status header and rendered output
    """
    import marimo as mo
    
    elements = []
    
    # Status header
    status_icon = "[OK]" if exit_code == 0 else "[ERR]"
    if command:
        elements.append(mo.md(f"{status_icon} `{command}` (exit: {exit_code})"))
    
    # Main output
    if stdout:
        elements.append(mo.md("**stdout:**"))
        elements.append(detect_and_render_output(stdout))
    
    # Error output (if any)
    if stderr:
        elements.append(mo.md("**stderr:**"))
        elements.append(mo.ui.text_area(
            value=stderr,
            disabled=True,
            full_width=True
        ))
    
    return mo.vstack(elements) if elements else mo.md("*(no output)*")
