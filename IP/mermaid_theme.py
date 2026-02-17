"""Generate Mermaid diagrams with MaestroView.vue colors for Orchestr8."""

MERMAID_CLASSDEFS = """
    classDef working fill:#D4AF37,stroke:#B8860B,color:#050505
    classDef broken fill:#1fbdea,stroke:#1fbdea,color:#050505
    classDef combat fill:#9D4EDD,stroke:#9D4EDD,color:#fff
    classDef normal fill:#D4AF37,stroke:#B8860B,color:#050505
    classDef warning fill:#D4AF37,stroke:#B8860B,color:#050505
    classDef complex fill:#9D4EDD,stroke:#9D4EDD,color:#fff
    classDef error fill:#1fbdea,stroke:#1fbdea,color:#050505
    classDef default fill:#121214,stroke:#B8860B,color:#e8e8e8
"""


def generate_status_graph(fiefdoms: dict) -> str:
    """Generate Mermaid graph with proper status colors."""
    lines = ["graph TB"]

    # Add nodes with status classes
    for name, info in fiefdoms.items():
        status = info.get("status", "broken").lower()
        # Map various statuses to our three-state system
        if status in ["normal", "working", "warning"]:
            mermaid_class = "working"
        elif status in ["combat", "complex"]:
            mermaid_class = "combat"
        else:  # broken, error, unknown
            mermaid_class = "broken"

        lines.append(f"    {name}[{name}]:::{mermaid_class}")

    # Add relationships
    for name, info in fiefdoms.items():
        for dep in info.get("depends_on", []):
            lines.append(f"    {dep} --> {name}")

    lines.append(MERMAID_CLASSDEFS)
    return "\n".join(lines)


def generate_file_dependency_graph(edges_df, files_df):
    """Generate Mermaid graph from file dependency data."""
    if edges_df.empty:
        return "graph TB\n    A[No Dependencies Found]"

    lines = ["graph TB"]
    nodes = set()

    # Process edges and create nodes
    for _, edge in edges_df.iterrows():
        source = edge["source"].replace("/", "_").replace(".", "_").replace("-", "_")
        target = edge["target"].replace("/", "_").replace(".", "_").replace("-", "_")

        nodes.add(source)
        nodes.add(target)
        lines.append(f"    {source} --> {target}")

    # Add node definitions with status from files_df
    for node in nodes:
        # Try to find the original file path
        original_path = node.replace("_", "/").replace("-", "/")
        file_status = "default"

        if not files_df.empty:
            matching_files = files_df[
                files_df["path"].str.contains(original_path, case=False, na=False)
            ]
            if not matching_files.empty:
                status = matching_files.iloc[0]["status"].lower()
                if status in ["normal", "working", "warning"]:
                    file_status = "working"
                elif status in ["combat", "complex"]:
                    file_status = "combat"
                else:
                    file_status = "broken"

        # Clean up node name for display
        display_name = (
            original_path.split("/")[-1] if "/" in original_path else original_path
        )
        lines.append(f"    {node}[{display_name}]:::{file_status}")

    lines.append(MERMAID_CLASSDEFS)
    return "\n".join(lines)


def generate_system_architecture(components: dict) -> str:
    """Generate system architecture diagram with status."""
    lines = ["graph TD"]

    for component_name, component_info in components.items():
        status = component_info.get("status", "default").lower()
        component_type = component_info.get("type", "component")

        # Map status
        if status in ["normal", "working", "warning"]:
            mermaid_class = "working"
        elif status in ["combat", "complex"]:
            mermaid_class = "combat"
        else:
            mermaid_class = "broken"

        lines.append(
            f"    {component_name}({component_name} [{component_type}]):::{mermaid_class}"
        )

        # Add connections
        for connection in component_info.get("connections", []):
            lines.append(f"    {component_name} --> {connection}")

    lines.append(MERMAID_CLASSDEFS)
    return "\n".join(lines)


def generate_workflow_steps(steps: list) -> str:
    """Generate workflow diagram with status for each step."""
    lines = ["graph LR"]

    for i, step in enumerate(steps):
        step_name = step.get("name", f"Step_{i}")
        status = step.get("status", "working").lower()

        # Map status
        if status in ["normal", "working", "warning"]:
            mermaid_class = "working"
        elif status in ["combat", "complex"]:
            mermaid_class = "combat"
        else:
            mermaid_class = "broken"

        node_id = f"step_{i}"
        lines.append(f"    {node_id}[{step_name}]:::{mermaid_class}")

        # Connect to next step
        if i < len(steps) - 1:
            next_id = f"step_{i + 1}"
            lines.append(f"    {node_id} --> {next_id}")

    lines.append(MERMAID_CLASSDEFS)
    return "\n".join(lines)
