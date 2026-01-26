import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def imports():
    """Core imports for Orchestr8"""
    import marimo as mo
    import pandas as pd
    import networkx as nx
    from pyvis.network import Network
    import os
    import re
    import json
    import datetime
    from jinja2 import Template
    return Network, Template, datetime, json, mo, nx, os, pd, re


@app.cell
def state_management(mo, pd):
    """Global state management - The Data Core"""
    # Project state using Marimo's reactive state
    get_project_root, set_project_root = mo.state(".")
    get_files_df, set_files_df = mo.state(pd.DataFrame())
    get_edges_df, set_edges_df = mo.state(pd.DataFrame())
    get_selected_file, set_selected_file = mo.state(None)
    get_agent_logs, set_agent_logs = mo.state([])
    return (
        get_agent_logs,
        get_edges_df,
        get_files_df,
        get_project_root,
        get_selected_file,
        set_agent_logs,
        set_edges_df,
        set_files_df,
        set_project_root,
        set_selected_file,
    )


@app.cell
def scanner_function(os, pd):
    """Project Scanner - The Harvester"""
    EXCLUSIONS = {'node_modules', '.git', '__pycache__', '.venv', 'venv', '.env'}
    
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
                
                file_list.append({
                    "path": rel_path,
                    "name": file,
                    "type": ext,
                    "size": size,
                    "status": "NORMAL",
                    "issues": 0
                })
                
        return pd.DataFrame(file_list)
    return EXCLUSIONS, scan_project


@app.cell
def verifier_function(os, pd, re):
    """Connection Verifier - Parses imports and checks file health"""
    # Regex patterns for various import styles
    IMPORT_PATTERNS = [
        re.compile(r"(?:from|import)\s+['\"]([^'\"]+)['\"]"),  # JS/TS style
        re.compile(r"^import\s+(\w+)", re.MULTILINE),          # Python: import module
        re.compile(r"^from\s+([\w.]+)\s+import", re.MULTILINE), # Python: from x import y
    ]
    
    def verify_connections(root_path, files_df):
        """
        Analyzes files for imports and health status.
        Returns: Updated files_df with badges, edges_df with connections
        """
        edges = []
        
        for index, row in files_df.iterrows():
            full_path = os.path.join(root_path, row['path'])
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Extract all imports using multiple patterns
                    all_imports = set()
                    for pattern in IMPORT_PATTERNS:
                        matches = pattern.findall(content)
                        all_imports.update(matches)
                    
                    # Create edges for each import
                    for target in all_imports:
                        edge = {
                            "source": row['path'],
                            "target": target,
                            "type": "import"
                        }
                        edges.append(edge)
                    
                    # Status badge logic
                    issues = 0
                    status = "NORMAL"
                    
                    if "TODO" in content or "FIXME" in content:
                        status = "WARNING"
                        issues += content.count("TODO") + content.count("FIXME")
                    
                    if len(all_imports) > 10:
                        status = "COMPLEX"
                    
                    files_df.at[index, 'status'] = status
                    files_df.at[index, 'issues'] = issues
                    
            except Exception:
                pass  # Skip binary/unreadable files
        
        return files_df, pd.DataFrame(edges)
    return IMPORT_PATTERNS, verify_connections


@app.cell
def badge_renderer():
    """Status Badge Renderer - Visual indicators"""
    def render_badge(status):
        colors = {
            "NORMAL": "#22c55e",   # green
            "WARNING": "#f97316",  # orange
            "COMPLEX": "#a855f7",  # purple
            "ERROR": "#ef4444"     # red
        }
        color = colors.get(status, "#6b7280")
        return f"<span style='background-color:{color}; color:white; padding:2px 8px; border-radius:4px; font-size:0.85em; font-weight:500'>{status}</span>"
    return (render_badge,)


@app.cell
def app_header(mo):
    """App Title and Header"""
    app_title = mo.md("# 🎻 Orchestr8: The Command Center")
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
):
    """Control Panel - Path input and scan button"""
    path_input = mo.ui.text(
        value=".", 
        label="Project Root", 
        full_width=True
    )
    
    def run_scan():
        root = path_input.value
        set_project_root(root)
        df = scan_project(root)
        df, edges = verify_connections(root, df)
        set_files_df(df)
        set_edges_df(edges)
    
    scan_button = mo.ui.button(
        label="🔍 Scan & Verify Codebase", 
        on_change=lambda _: run_scan()
    )
    
    control_row = mo.hstack([path_input, scan_button], justify="start", gap=1)
    return control_row, path_input, run_scan, scan_button


@app.cell
def explorer_view_cell(mo, get_files_df, get_selected_file, set_selected_file, render_badge):
    """Explorer Tab - File system table with selection"""
    def build_explorer_view():
        df = get_files_df()
        if df.empty:
            return mo.md("*No project loaded. Enter a path and click Scan.*")
        
        # Add visual badges
        display_df = df.copy()
        display_df['status_badge'] = display_df['status'].apply(render_badge)
        
        # Create interactive table
        table = mo.ui.table(
            display_df[['status_badge', 'path', 'type', 'size', 'issues']],
            selection='single',
            label="📂 File System"
        )
        
        return mo.vstack([
            table,
            mo.md(f"**Selected:** `{get_selected_file() or 'None'}`")
        ])
    
    explorer_content = build_explorer_view()
    return (explorer_content,)


@app.cell
def connection_graph_cell(mo, nx, Network, get_edges_df, get_files_df):
    """Connections Tab - NetworkX/PyVis graph visualization"""
    def build_connection_graph():
        edges = get_edges_df()
        
        if edges.empty:
            return mo.md("*No connections found. Scan a project first.*")
        
        # Build NetworkX directed graph
        G = nx.from_pandas_edgelist(edges, source='source', target='target', create_using=nx.DiGraph())
        
        # Configure PyVis
        net = Network(
            height="500px", 
            width="100%", 
            bgcolor="#1a1a2e", 
            font_color="white",
            directed=True
        )
        net.from_nx(G)
        
        # Physics settings for force-directed layout
        net.barnes_hut(
            gravity=-2000,
            central_gravity=0.3,
            spring_length=100,
            spring_strength=0.01,
            damping=0.09
        )
        
        try:
            html_str = net.generate_html()
            return mo.Html(html_str)
        except Exception as e:
            return mo.md(f"Graph generation error: {str(e)}")
    
    graph_content = build_connection_graph()
    return (graph_content,)


@app.cell
def prd_generator_cell(mo, Template, datetime, get_selected_file, get_files_df, get_edges_df):
    """PRD Generator Tab - Jinja2 templated documentation"""
    def build_prd_view():
        selected = get_selected_file()
        if not selected:
            return mo.md("👈 *Select a file in the Explorer tab to generate a PRD.*")
        
        df = get_files_df()
        edges = get_edges_df()
        
        if df.empty:
            return mo.md("*No project loaded.*")
        
        # Find file data
        file_matches = df[df['path'] == selected]
        if file_matches.empty:
            return mo.md(f"*File `{selected}` not found in scan results.*")
        
        file_data = file_matches.iloc[0]
        
        # Get connections
        outgoing = edges[edges['source'] == selected].to_dict('records') if not edges.empty else []
        incoming = edges[edges['target'] == selected].to_dict('records') if not edges.empty else []
        
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
            status=file_data['status'],
            extension=file_data['type'],
            size=file_data['size'],
            outgoing=outgoing,
            incoming=incoming
        )
        
        return mo.md(markdown_out)
    
    prd_content = build_prd_view()
    return (prd_content,)


@app.cell
def emperor_view_cell(mo, datetime, get_selected_file, get_agent_logs, set_agent_logs):
    """Emperor Tab - Command interface and logging"""
    selected = get_selected_file()
    
    mission_input = mo.ui.text_area(
        label="Mission Briefing", 
        placeholder="e.g., Refactor the login logic to use OAuth...",
        full_width=True
    )
    
    def deploy_agent():
        if not selected:
            return
        current_logs = get_agent_logs()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        new_log = f"[{timestamp}] 🚀 DEPLOYING to '{selected}': {mission_input.value}"
        set_agent_logs(current_logs + [new_log])
    
    deploy_btn = mo.ui.button(
        label="🎯 Deploy Agent", 
        on_change=lambda _: deploy_agent()
    )
    
    # Build log display
    logs = get_agent_logs()
    if logs:
        log_items = "\n".join([f"- {log}" for log in logs])
        log_display = mo.md(log_items)
    else:
        log_display = mo.md("*No deployments yet.*")
    
    emperor_content = mo.vstack([
        mo.md(f"### 🎯 Target: `{selected or 'None selected'}`"),
        mission_input,
        deploy_btn,
        mo.md("---"),
        mo.md("### 📡 Command Center Logs"),
        log_display
    ])
    return deploy_btn, emperor_content, mission_input


@app.cell
def main_layout(mo, app_title, control_row, explorer_content, graph_content, prd_content, emperor_content):
    """Main Application Layout with Tabs"""
    tabs = mo.ui.tabs({
        "📁 Explorer": explorer_content,
        "🕸️ Connections": graph_content,
        "📄 PRD Generator": prd_content,
        "👑 Emperor": emperor_content
    })
    
    # Final layout
    mo.vstack([
        app_title,
        control_row,
        tabs
    ])
    return (tabs,)


if __name__ == "__main__":
    app.run()
