import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def imports():
    """Core imports for Orchestr8 - THE LIGHT SWITCH
    
    When this cell runs, the entire building turns on.
    All IP modules are imported here, activating the full library chain.
    """
    import marimo as mo
    import pandas as pd
    import networkx as nx
    from pyvis.network import Network
    import os
    import re
    import json
    import datetime
    from jinja2 import Template

    # =========================================================================
    # THE BUILDING - All IP modules activated on startup
    # =========================================================================
    
    # Code City visualization - The Skyscape
    from IP.woven_maps import create_code_city, build_graph_data

    # Combat tracking for LLM deployments
    from IP.combat_tracker import CombatTracker
    
    # Connection verification - import graph analysis
    from IP.connection_verifier import ConnectionVerifier
    
    # Health monitoring
    from IP.health_checker import HealthChecker
    
    # Mermaid diagram generation
    from IP.mermaid_generator import Fiefdom, FiefdomStatus, generate_empire_mermaid
    
    # Terminal spawning for agent deployment
    from IP.terminal_spawner import TerminalSpawner
    
    # Briefing generation for context
    from IP.briefing_generator import BriefingGenerator
    
    # Ticket management
    from IP.ticket_manager import TicketManager
    
    # Carl - TypeScript context bridge
    from IP.carl_core import CarlContextualizer
    
    # Louis - The Warden (validation)
    from IP.louis_core import LouisWarden, LouisConfig
    
    # Connie - Database conversion engine
    from IP.connie import ConversionEngine
    
    # Log successful activation
    print("⚡ THE BUILDING IS ON - All IP modules activated")
    print(f"   ├── woven_maps (Code City)")
    print(f"   ├── combat_tracker (Deployments)")
    print(f"   ├── connection_verifier (Import Graph)")
    print(f"   ├── health_checker (System Health)")
    print(f"   ├── mermaid_generator (Diagrams)")
    print(f"   ├── terminal_spawner (Terminals)")
    print(f"   ├── briefing_generator (Context)")
    print(f"   ├── ticket_manager (Tickets)")
    print(f"   ├── carl_core (TypeScript Bridge)")
    print(f"   ├── louis_core (Validation)")
    print(f"   └── connie (DB Conversion)")

    return (
        BriefingGenerator,
        CarlContextualizer,
        CombatTracker,
        ConnectionVerifier,
        ConversionEngine,
        Fiefdom,
        FiefdomStatus,
        HealthChecker,
        LouisConfig,
        LouisWarden,
        Network,
        Template,
        TerminalSpawner,
        TicketManager,
        build_graph_data,
        create_code_city,
        datetime,
        generate_empire_mermaid,
        json,
        mo,
        nx,
        os,
        pd,
        re,
    )


@app.cell
def state_management(mo, pd):
    """Global state management - The Data Core"""
    # Project state using Marimo's reactive state
    get_project_root, set_project_root = mo.state(".")
    get_files_df, set_files_df = mo.state(pd.DataFrame())
    get_edges_df, set_edges_df = mo.state(pd.DataFrame())
    get_selected_file, set_selected_file = mo.state(None)
    get_agent_logs, set_agent_logs = mo.state([])

    # Combat state - version counter triggers UI refresh on deploy/withdraw
    get_combat_version, set_combat_version = mo.state(0)

    return (
        get_agent_logs,
        get_combat_version,
        get_edges_df,
        get_files_df,
        get_project_root,
        get_selected_file,
        set_agent_logs,
        set_combat_version,
        set_edges_df,
        set_files_df,
        set_project_root,
        set_selected_file,
    )


@app.cell
def scanner_function(os, pd):
    """Project Scanner - The Harvester"""
    EXCLUSIONS = {"node_modules", ".git", "__pycache__", ".venv", "venv", ".env"}

    def scan_project(root_path):
        """
        Scans directory and builds Files DataFrame.
        Excludes common non-source directories.
        """
        file_list = []

        for root, dirs, files in os.walk(root_path):
            # Filter out excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUSIONS]

            # Skip if we're inside an excluded path
            if any(excl in root for excl in EXCLUSIONS):
                continue

            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_path)
                ext = os.path.splitext(file)[1]

                try:
                    size = os.path.getsize(full_path)
                except OSError:
                    size = 0

                file_list.append(
                    {
                        "path": rel_path,
                        "name": file,
                        "type": ext,
                        "size": size,
                        "status": "NORMAL",
                        "issues": 0,
                    }
                )

        return pd.DataFrame(file_list)

    return EXCLUSIONS, scan_project


@app.cell
def verifier_function(os, pd, re, ConnectionVerifier):
    """Connection Verifier - Uses IP/connection_verifier.py for real import resolution"""
    # ConnectionVerifier is now passed from imports() - always available
    HAS_VERIFIER = True
    
    # Fallback regex patterns if connection_verifier not available
    IMPORT_PATTERNS = [
        re.compile(r"(?:from|import)\s+['\"]([^'\"]+)['\"]"),  # JS/TS style
        re.compile(r"^import\s+(\w+)", re.MULTILINE),  # Python: import module
        re.compile(
            r"^from\s+([\w.]+)\s+import", re.MULTILINE
        ),  # Python: from x import y
    ]

    def verify_connections(root_path, files_df):
        """
        Analyzes files for imports and health status.
        Uses IP/connection_verifier.py to ACTUALLY resolve imports.
        Returns: Updated files_df with badges, edges_df with connections
        """
        edges = []
        
        # Use real verifier if available
        if HAS_VERIFIER:
            verifier = ConnectionVerifier(root_path)
            
            for index, row in files_df.iterrows():
                result = verifier.verify_file(row["path"])
                
                # Status based on ACTUAL import resolution
                if result.broken_imports:
                    files_df.at[index, "status"] = "ERROR"  # Blue - broken imports
                    files_df.at[index, "issues"] = len(result.broken_imports)
                elif result.total_imports > 10:
                    files_df.at[index, "status"] = "COMPLEX"  # Purple - high complexity
                else:
                    files_df.at[index, "status"] = "NORMAL"  # Gold - working
                
                # Create edges for all imports (with resolution status)
                for imp in result.broken_imports:
                    edges.append({
                        "source": row["path"],
                        "target": imp.target_module,
                        "type": "import",
                        "resolved": False,
                        "line": imp.line_number
                    })

                # Add resolved local imports (THE ACTUAL CONNECTIONS!)
                for imp in result.local_imports:
                    edges.append({
                        "source": row["path"],
                        "target": imp.resolved_path,
                        "type": "import",
                        "resolved": True,
                        "line": imp.line_number
                    })

                # External imports with resolved paths (rare, usually None)
                for imp in result.external_imports:
                    if imp.resolved_path:
                        edges.append({
                            "source": row["path"],
                            "target": imp.resolved_path,
                            "type": "import",
                            "resolved": True,
                            "line": imp.line_number
                        })
            
            return files_df, pd.DataFrame(edges) if edges else pd.DataFrame()
        
        # Fallback: original regex-only approach
        for index, row in files_df.iterrows():
            full_path = os.path.join(root_path, row["path"])

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    # Extract all imports using multiple patterns
                    all_imports = set()
                    for pattern in IMPORT_PATTERNS:
                        matches = pattern.findall(content)
                        all_imports.update(matches)

                    # Create edges for each import
                    for target in all_imports:
                        edge = {
                            "source": row["path"],
                            "target": target,
                            "type": "import",
                            "resolved": None,  # Unknown
                            "line": 0
                        }
                        edges.append(edge)

                    # Status badge logic (fallback - no resolution check)
                    issues = 0
                    status = "NORMAL"

                    if "TODO" in content or "FIXME" in content:
                        status = "WARNING"
                        issues += content.count("TODO") + content.count("FIXME")

                    if len(all_imports) > 10:
                        status = "COMPLEX"

                    files_df.at[index, "status"] = status
                    files_df.at[index, "issues"] = issues

            except Exception:
                pass  # Skip binary/unreadable files

        return files_df, pd.DataFrame(edges)

    return IMPORT_PATTERNS, verify_connections


@app.cell
def badge_renderer():
    """Status Badge Renderer - Visual indicators"""

    def render_badge(status):
        colors = {
            "NORMAL": "#D4AF37",   # Gold - working (matches Woven Maps)
            "WARNING": "#f97316",  # Orange
            "COMPLEX": "#a855f7",  # Purple - high complexity
            "ERROR": "#1fbdea",    # Teal/Blue - broken (matches Woven Maps)
            "COMBAT": "#9D4EDD",   # Purple - LLM deployed (matches Woven Maps)
        }
        color = colors.get(status, "#6b7280")
        return f"<span style='background-color:{color}; color:white; padding:2px 8px; border-radius:4px; font-size:0.85em; font-weight:500'>{status}</span>"

    return (render_badge,)


@app.cell
def app_header(mo):
    """App Title and Header"""
    app_title = mo.md("# Orchestr8: The Command Center")
    return (app_title,)


@app.cell
def control_panel(
    mo,
    get_project_root,
    set_project_root,
    set_files_df,
    set_edges_df,
    scan_project,
    verify_connections,
    CombatTracker,
):
    """Control Panel - Path input and scan button"""
    path_input = mo.ui.text(value=".", label="Project Root", full_width=True)

    def run_scan():
        root = path_input.value
        set_project_root(root)
        df = scan_project(root)
        df, edges = verify_connections(root, df)

        # Apply COMBAT status for files with active deployments
        combat_tracker = CombatTracker(root)
        combat_files = combat_tracker.get_combat_files()
        for combat_file in combat_files:
            mask = df["path"] == combat_file
            if mask.any():
                df.loc[mask, "status"] = "COMBAT"

        set_files_df(df)
        set_edges_df(edges)

    scan_button = mo.ui.button(
        label="Scan & Verify Codebase", on_change=lambda _: run_scan()
    )

    control_row = mo.hstack([path_input, scan_button], justify="start", gap=1)
    return control_row, path_input, run_scan, scan_button


@app.cell
def explorer_table_cell(mo, get_files_df, render_badge):
    """Explorer Tab - File system table with selection"""
    df = get_files_df()

    if df.empty:
        explorer_table = None
        explorer_content = mo.md("*No project loaded. Enter a path and click Scan.*")
    else:
        # Add visual badges
        display_df = df.copy()
        display_df["status_badge"] = display_df["status"].apply(render_badge)

        # Create interactive table - returned so selection can be accessed
        explorer_table = mo.ui.table(
            display_df[["status_badge", "path", "type", "size", "issues"]],
            selection="single",
            label="File System",
        )
        explorer_content = explorer_table

    return explorer_content, explorer_table


@app.cell
def explorer_selection_cell(mo, explorer_table, set_selected_file, get_selected_file):
    """Handle explorer table selection and update state"""
    selected_path = None

    if explorer_table is not None and hasattr(explorer_table, 'value') and explorer_table.value is not None:
        # table.value returns DataFrame of selected rows
        selected_rows = explorer_table.value
        if not selected_rows.empty and len(selected_rows) > 0:
            selected_path = selected_rows.iloc[0].get("path")
            set_selected_file(selected_path)

    # Display current selection
    current = get_selected_file()
    selection_display = mo.md(f"**Selected:** `{current or 'None'}`")
    return (selection_display,)


@app.cell
def explorer_view_cell(mo, explorer_content, selection_display):
    """Combine explorer table and selection display"""
    if hasattr(explorer_content, '_mime_'):
        # It's a UI element (table)
        combined = mo.vstack([explorer_content, selection_display])
    else:
        # It's the empty state markdown
        combined = explorer_content
    return (combined,)


@app.cell
def connection_graph_cell(mo, nx, Network, get_edges_df, get_files_df):
    """Connections Tab - NetworkX/PyVis graph visualization"""

    def build_connection_graph():
        edges = get_edges_df()

        if edges.empty:
            return mo.md("*No connections found. Scan a project first.*")

        # Build NetworkX directed graph
        G = nx.from_pandas_edgelist(
            edges, source="source", target="target", create_using=nx.DiGraph()
        )

        # Configure PyVis
        net = Network(
            height="500px",
            width="100%",
            bgcolor="#1a1a2e",
            font_color="white",
            directed=True,
        )
        net.from_nx(G)

        # Physics settings for force-directed layout
        net.barnes_hut(
            gravity=-2000,
            central_gravity=0.3,
            spring_length=100,
            spring_strength=0.01,
            damping=0.09,
        )

        try:
            html_str = net.generate_html()
            return mo.Html(html_str)
        except Exception as e:
            return mo.md(f"Graph generation error: {str(e)}")

    graph_content = build_connection_graph()
    return (graph_content,)


@app.cell
def code_city_cell(mo, get_project_root, get_files_df, create_code_city):
    """Code City Tab - Woven Maps visualization with emergence animations"""

    def build_code_city_view():
        df = get_files_df()
        root = get_project_root()

        if df.empty:
            return mo.md("*No project loaded. Scan a project to see the Code City.*")

        # Pass the project root to create_code_city - it handles scanning internally
        # with its own Code City node analysis (LOC, TODO detection, etc.)
        try:
            return create_code_city(root, width=900, height=650)
        except Exception as e:
            return mo.md(f"Code City generation error: {str(e)}")

    code_city_content = build_code_city_view()
    return (code_city_content,)


@app.cell
def prd_generator_cell(
    mo, Template, datetime, get_selected_file, get_files_df, get_edges_df
):
    """PRD Generator Tab - Jinja2 templated documentation"""

    def build_prd_view():
        selected = get_selected_file()
        if not selected:
            return mo.md("*Select a file in the Explorer tab to generate a PRD.*")

        df = get_files_df()
        edges = get_edges_df()

        if df.empty:
            return mo.md("*No project loaded.*")

        # Find file data
        file_matches = df[df["path"] == selected]
        if file_matches.empty:
            return mo.md(f"*File `{selected}` not found in scan results.*")

        file_data = file_matches.iloc[0]

        # Get connections
        outgoing = (
            edges[edges["source"] == selected].to_dict("records")
            if not edges.empty
            else []
        )
        incoming = (
            edges[edges["target"] == selected].to_dict("records")
            if not edges.empty
            else []
        )

        # Jinja2 Template
        template_str = """
# PRD: {{ filename }}

**Generated:** {{ timestamp }}  
**Status:** {{ status }}  
**Type:** {{ extension }}  
**Size:** {{ size }} bytes

---

## 1. Overview

This document describes the functionality of `{{ filename }}`.

## 2. Dependencies (Outgoing)

{% if outgoing %}
This file imports:
{% for edge in outgoing %}
- `{{ edge.target }}` ({{ edge.type }})
{% endfor %}
{% else %}
*No outgoing dependencies detected.*
{% endif %}

## 3. Consumers (Incoming)

{% if incoming %}
This file is imported by:
{% for edge in incoming %}
- `{{ edge.source }}` ({{ edge.type }})
{% endfor %}
{% else %}
*No incoming references detected.*
{% endif %}

## 4. Implementation Notes

[TODO: Add implementation details based on file analysis]

---
*Generated by Orchestr8 PRD Generator*
"""

        t = Template(template_str)
        markdown_out = t.render(
            filename=selected,
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            status=file_data["status"],
            extension=file_data["type"],
            size=file_data["size"],
            outgoing=outgoing,
            incoming=incoming,
        )

        return mo.md(markdown_out)

    prd_content = build_prd_view()
    return (prd_content,)


@app.cell
def model_loader_cell():
    """Load available models from settings."""
    def get_available_models():
        """Load available models from orchestr8_settings.toml."""
        try:
            import toml
            from pathlib import Path
            settings_file = Path("orchestr8_settings.toml")
            if settings_file.exists():
                settings = toml.load(settings_file)
                # Get from communic8.multi_llm.default_models
                models = settings.get("tools", {}).get("communic8", {}).get("multi_llm", {}).get("default_models", [])
                if models:
                    return models
        except Exception:
            pass
        # Fallback - user should configure in settings
        return ["claude", "gpt-4", "gemini", "local"]

    return (get_available_models,)


@app.cell
def emperor_view_cell(
    mo,
    datetime,
    get_selected_file,
    get_agent_logs,
    set_agent_logs,
    get_project_root,
    CombatTracker,
    get_combat_version,
    set_combat_version,
    set_files_df,
    get_files_df,
    get_available_models,
):
    """Emperor Tab - Command interface with COMBAT deployment tracking"""
    selected = get_selected_file()
    root = get_project_root()

    # Initialize combat tracker
    combat_tracker = CombatTracker(root)

    # Get available models from settings
    available_models = get_available_models()
    get_selected_model, set_selected_model = mo.state(available_models[0] if available_models else "claude")

    # Force reactivity on combat_version changes
    _ = get_combat_version()

    mission_input = mo.ui.text_area(
        label="Mission Briefing",
        placeholder="e.g., Refactor the login logic to use OAuth...",
        full_width=True,
    )

    # Model selector dropdown - populated from settings
    model_selector = mo.ui.dropdown(
        options=available_models,
        value=get_selected_model(),
        label="Deploy Model",
        on_change=set_selected_model,
    )

    def deploy_agent():
        if not selected:
            return

        # Deploy via CombatTracker - file goes PURPLE
        terminal_id = f"emperor-{datetime.datetime.now().strftime('%H%M%S')}"
        selected_model = get_selected_model()
        combat_tracker.deploy(selected, terminal_id, model=selected_model)

        # Update files_df to show COMBAT status
        df = get_files_df()
        if not df.empty:
            mask = df["path"] == selected
            df.loc[mask, "status"] = "COMBAT"
            set_files_df(df.copy())

        # Log the deployment
        current_logs = get_agent_logs()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        new_log = f"[{timestamp}] DEPLOYED to '{selected}': {mission_input.value}"
        set_agent_logs(current_logs + [new_log])

        # Trigger UI refresh
        set_combat_version(get_combat_version() + 1)

    def withdraw_agent():
        if not selected:
            return

        # Withdraw via CombatTracker - file returns to normal status
        combat_tracker.withdraw(selected)

        # Update files_df - set back to NORMAL (will be rechecked on next scan)
        df = get_files_df()
        if not df.empty:
            mask = df["path"] == selected
            df.loc[mask, "status"] = "NORMAL"
            set_files_df(df.copy())

        # Log the withdrawal
        current_logs = get_agent_logs()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        new_log = f"[{timestamp}] WITHDRAWN from '{selected}'"
        set_agent_logs(current_logs + [new_log])

        # Trigger UI refresh
        set_combat_version(get_combat_version() + 1)

    deploy_btn = mo.ui.button(
        label="Deploy Agent",
        on_change=lambda _: deploy_agent()
    )

    withdraw_btn = mo.ui.button(
        label="Withdraw",
        on_change=lambda _: withdraw_agent()
    )

    # Check if selected file is in combat
    is_in_combat = combat_tracker.is_in_combat(selected) if selected else False

    # Get all active deployments
    active_deployments = combat_tracker.get_active_deployments()

    # Build combat status display
    if active_deployments:
        combat_list = "\n".join([
            f"- `{path}` (deployed {info.get('deployed_at', 'unknown')[:19]})"
            for path, info in active_deployments.items()
        ])
        combat_display = mo.md(f"**Active Deployments ({len(active_deployments)}):**\n{combat_list}")
    else:
        combat_display = mo.md("*No active deployments.*")

    # Build log display
    logs = get_agent_logs()
    if logs:
        log_items = "\n".join([f"- {log}" for log in logs[-10:]])  # Last 10 logs
        log_display = mo.md(log_items)
    else:
        log_display = mo.md("*No deployments yet.*")

    # Target status indicator
    if selected:
        status_text = "**IN COMBAT**" if is_in_combat else "Ready for deployment"
    else:
        status_text = "No target selected"

    emperor_content = mo.vstack(
        [
            mo.md(f"### Target: `{selected or 'None selected'}`"),
            mo.md(status_text),
            mission_input,
            mo.hstack([model_selector, deploy_btn, withdraw_btn], justify="start", gap="1rem"),
            mo.md("---"),
            mo.md("### Active Combat Zones"),
            combat_display,
            mo.md("---"),
            mo.md("### Command Center Logs"),
            log_display,
        ]
    )
    return deploy_btn, emperor_content, mission_input, model_selector, withdraw_btn


@app.cell
def main_layout(
    mo,
    app_title,
    control_row,
    combined,
    graph_content,
    code_city_content,
    prd_content,
    emperor_content,
):
    """Main Application Layout - MAESTRO STYLE
    
    Implements MaestroView.vue spatial UI pattern:
    - Top row navigation with brand
    - Central void for content emergence
    - Bottom control surface
    
    Colors (EXACT - NO EXCEPTIONS):
    --blue-dominant: #1fbdea (UI default, Broken state)
    --gold-metallic: #D4AF37 (UI highlight, Working state)
    --gold-dark: #B8860B (Maestro default)
    --gold-saffron: #F4C430 (Maestro highlight)
    --bg-primary: #0A0A0B (The Void)
    --bg-elevated: #121214 (Surface)
    --purple-combat: #9D4EDD (Combat state - General deployed)
    """
    
    # Color constants
    BLUE_DOMINANT = "#1fbdea"
    GOLD_METALLIC = "#D4AF37"
    GOLD_DARK = "#B8860B"
    GOLD_SAFFRON = "#F4C430"
    BG_PRIMARY = "#0A0A0B"
    BG_ELEVATED = "#121214"
    PURPLE_COMBAT = "#9D4EDD"
    
    # Maestro CSS - The styling that makes it look like MaestroView.vue
    MAESTRO_CSS = f"""
    <style>
    /* =========================================================
       EMERGENCE ANIMATIONS - Things EMERGE, they don't breathe
       ========================================================= */
    
    @keyframes emergence {{
        0% {{
            opacity: 0;
            transform: translateY(12px);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes emergence-fade {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}
    
    @keyframes emergence-scale {{
        0% {{
            opacity: 0;
            transform: scale(0.95);
        }}
        100% {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    /* Apply emergence to key elements with staggered delays */
    .maestro-container {{
        min-height: 70vh;
        display: flex;
        flex-direction: column;
        animation: emergence-fade 0.3s ease-out forwards;
        background: {BG_PRIMARY};
        padding: 16px;
        border-radius: 8px;
    }}
    
    .maestro-top-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid rgba(31, 189, 234, 0.2);
        animation: emergence 0.4s ease-out 0.1s both;
    }}
    
    .stereos-brand {{
        font-family: monospace;
        font-size: 18px;
        letter-spacing: 0.08em;
    }}
    
    .stereos-prefix {{
        color: {BLUE_DOMINANT};
    }}
    
    .stereos-suffix {{
        color: {GOLD_METALLIC};
    }}
    
    .void-center {{
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 20px;
        min-height: 400px;
        animation: emergence-scale 0.5s ease-out 0.2s both;
    }}
    
    .control-surface {{
        border-top: 1px solid rgba(31, 189, 234, 0.2);
        padding: 12px 0;
        animation: emergence 0.4s ease-out 0.3s both;
    }}
    
    .maestro-btn {{
        padding: 8px 16px;
        background: transparent;
        border: 1px solid rgba(31, 189, 234, 0.3);
        border-radius: 4px;
        color: {BLUE_DOMINANT};
        font-family: monospace;
        font-size: 11px;
        letter-spacing: 0.08em;
        cursor: pointer;
        transition: all 150ms ease-out;
    }}
    
    .maestro-btn:hover {{
        color: {GOLD_METALLIC};
        border-color: {GOLD_METALLIC};
        background: rgba(212, 175, 55, 0.1);
    }}
    
    .maestro-btn.active {{
        color: {GOLD_METALLIC};
        border-color: {GOLD_METALLIC};
    }}
    
    .maestro-center-btn {{
        padding: 12px 40px;
        background: none;
        border: 1px solid rgba(184, 134, 11, 0.3);
        border-radius: 4px;
        color: {GOLD_DARK};
        font-family: monospace;
        font-size: 14px;
        letter-spacing: 0.1em;
        cursor: pointer;
    }}
    
    .maestro-center-btn:hover {{
        color: {GOLD_SAFFRON};
        border-color: rgba(244, 196, 48, 0.4);
        background: rgba(184, 134, 11, 0.1);
    }}
    
    .panel-overlay {{
        background: rgba(18, 18, 20, 0.95);
        border: 1px solid rgba(31, 189, 234, 0.3);
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
        animation: emergence-scale 0.35s ease-out both;
    }}
    
    .panel-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(31, 189, 234, 0.2);
    }}
    
    .panel-title {{
        color: {GOLD_METALLIC};
        font-family: monospace;
        font-size: 12px;
        letter-spacing: 0.1em;
    }}
    
    .maestro-tabs {{
        display: flex;
        gap: 8px;
        margin: 12px 0;
    }}
    
    .void-title {{
        color: {GOLD_METALLIC};
        font-family: monospace;
        font-size: 24px;
        letter-spacing: 0.15em;
        margin-bottom: 4px;
    }}
    
    .void-subtitle {{
        color: rgba(255, 255, 255, 0.4);
        font-style: italic;
        font-size: 12px;
        margin-bottom: 16px;
    }}
    </style>
    """
    
    # Inject CSS
    css_injection = mo.Html(MAESTRO_CSS)
    
    # Brand header
    brand = mo.Html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
        <div class="stereos-brand">
            <span class="stereos-prefix">Orchestr</span><span class="stereos-suffix">8</span>
        </div>
        <div style="color: {GOLD_DARK}; font-family: monospace; font-size: 11px;">
            THE VOID
        </div>
    </div>
    """)
    
    # Title
    void_header = mo.Html(f"""
    <div style="text-align: center; padding: 8px 0;">
        <div class="void-title">The Command Center</div>
        <div class="void-subtitle">maestro overlooks the abyss</div>
    </div>
    """)
    
    # Build tabs with Maestro styling
    tabs = mo.ui.tabs(
        {
            "Code City": code_city_content,
            "Explorer": combined,
            "Connections": graph_content,
            "PRD Generator": prd_content,
            "Emperor": emperor_content,
        }
    )

    # Final Maestro-style layout
    layout = mo.Html(f"""
    <div class="maestro-container">
    </div>
    """)
    
    # Assemble with emergence pattern
    mo.vstack([
        css_injection,
        brand,
        mo.Html(f'<div style="border-bottom: 1px solid rgba(31, 189, 234, 0.2); margin: 8px 0;"></div>'),
        void_header,
        control_row,
        mo.Html(f'<div style="border-bottom: 1px solid rgba(31, 189, 234, 0.2); margin: 8px 0;"></div>'),
        tabs,
    ])
    
    return (tabs,)


if __name__ == "__main__":
    app.run()
