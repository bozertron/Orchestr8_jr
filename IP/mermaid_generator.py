# IP/mermaid_generator.py
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class FiefdomStatus(Enum):
    WORKING = "working"  # Gold - healthy
    BROKEN = "broken"  # Blue - has errors
    COMBAT = "combat"  # Purple - general deployed


@dataclass
class Fiefdom:
    path: str
    status: FiefdomStatus
    connections: List[str]
    error_count: int = 0
    last_check: Optional[str] = None


# Color constants from MaestroView.vue
COLORS = {
    "working": {"fill": "#D4AF37", "stroke": "#B8860B", "text": "#000"},
    "broken": {"fill": "#1fbdea", "stroke": "#0891b2", "text": "#000"},
    "combat": {"fill": "#9D4EDD", "stroke": "#7c3aed", "text": "#fff"},
}


def generate_empire_mermaid(fiefdoms: List[Fiefdom]) -> str:
    """
    Generate Mermaid flowchart with gold/blue/purple coloring.

    Args:
        fiefdoms: List of Fiefdom objects

    Returns:
        Mermaid markdown string ready for mo.mermaid()
    """
    lines = ["graph TD"]

    # Create node ID mapping
    path_to_id = {f.path: f"N{i}" for i, f in enumerate(fiefdoms)}

    # Add nodes with labels
    for i, f in enumerate(fiefdoms):
        node_id = f"N{i}"
        label = Path(f.path).name
        # Add error count to broken nodes
        if f.status == FiefdomStatus.BROKEN and f.error_count > 0:
            label = f"{label} ({f.error_count})"
        lines.append(f'    {node_id}["{label}"]')

    # Add edges based on connections
    for f in fiefdoms:
        source_id = path_to_id[f.path]
        for conn in f.connections:
            if conn in path_to_id:
                target_id = path_to_id[conn]
                lines.append(f"    {source_id} --> {target_id}")

    # Add styles based on status
    lines.append("")
    for i, f in enumerate(fiefdoms):
        node_id = f"N{i}"
        colors = COLORS[f.status.value]
        lines.append(
            f"    style {node_id} fill:{colors['fill']},"
            f"stroke:{colors['stroke']},color:{colors['text']}"
        )

    return "\n".join(lines)


def render_in_marimo(fiefdoms: List[Fiefdom]):
    """Render Mermaid graph in Marimo."""
    import marimo as mo

    mermaid_str = generate_empire_mermaid(fiefdoms)
    return mo.mermaid(mermaid_str)
