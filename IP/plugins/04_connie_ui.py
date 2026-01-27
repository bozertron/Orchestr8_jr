"""
04_connie_ui Plugin - Database Conversion UI
Orchestr8 v3.0 - The Fortress Factory

Provides a UI interface for Connie database conversion engine.
Allows users to browse, preview, and export SQLite database tables
in multiple formats.

Features:
    - Database file picker (*.db)
    - Table dropdown selection
    - Format selection (CSV, JSON, Markdown, SQL)
    - Preview with pd.head(10)
    - Export functionality
"""

import os
import json
from pathlib import Path
from datetime import datetime

PLUGIN_NAME = "Connie"
PLUGIN_ORDER = 4

def find_db_files(root_path, max_depth=3):
    """Find SQLite database files in project."""
    db_files = []
    root = Path(root_path)
    
    def scan(path, depth=0):
        if depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', 'venv', '.venv']:
                    continue
                
                if item.is_file() and item.suffix in ['.db', '.sqlite', '.sqlite3']:
                    db_files.append(str(item.relative_to(root)))
                elif item.is_dir():
                    scan(item, depth + 1)
        except PermissionError:
            pass
    
    scan(root)
    return sorted(db_files)

def render(STATE_MANAGERS):
    """Render the Connie database conversion UI."""
    import marimo as mo
    
    get_root, set_root = STATE_MANAGERS["root"]
    get_logs, set_logs = STATE_MANAGERS["logs"]
    
    # Local state
    get_selected_db, set_selected_db = mo.state("")
    get_selected_table, set_selected_table = mo.state("")
    get_export_format, set_export_format = mo.state("csv")
    get_tables, set_tables = mo.state([])
    get_preview, set_preview = mo.state(None)
    get_export_result, set_export_result = mo.state("")
    
    root = get_root()
    
    # Find database files
    db_files = find_db_files(root)
    
    # Database picker
    if db_files:
        db_options = {f: f for f in db_files}
        db_picker = mo.ui.dropdown(
            options=db_options,
            value=get_selected_db() or (db_files[0] if db_files else ""),
            label="Select Database",
            on_change=lambda v: handle_db_select(v)
        )
    else:
        db_picker = mo.md("*No SQLite databases found in project. Files with .db, .sqlite, or .sqlite3 extensions will appear here.*")
    
    def handle_db_select(db_path):
        """Handle database selection and load tables."""
        set_selected_db(db_path)
        set_selected_table("")
        set_preview(None)
        
        if not db_path:
            set_tables([])
            return
        
        full_path = Path(root) / db_path
        
        try:
            # Try to use ConversionEngine from connie.py
            try:
                import sys
                sys.path.insert(0, str(Path(__file__).parent.parent))
                from connie import ConversionEngine
                
                with ConversionEngine(str(full_path)) as engine:
                    tables_df = engine.list_tables()
                    table_list = tables_df['name'].tolist() if not tables_df.empty else []
                    set_tables(table_list)
                    
                    logs = get_logs()
                    set_logs(logs + [f"[Connie] Loaded {len(table_list)} tables from {db_path}"])
            except ImportError:
                # Fallback to direct sqlite3 access
                import sqlite3
                conn = sqlite3.connect(str(full_path))
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                table_list = [row[0] for row in cursor.fetchall()]
                conn.close()
                set_tables(table_list)
                
                logs = get_logs()
                set_logs(logs + [f"[Connie] Loaded {len(table_list)} tables (fallback mode)"])
        except Exception as e:
            logs = get_logs()
            set_logs(logs + [f"[Connie] Error loading database: {str(e)}"])
            set_tables([])
    
    # Table dropdown
    tables = get_tables()
    if tables:
        table_dropdown = mo.ui.dropdown(
            options={t: t for t in tables},
            value=get_selected_table() or (tables[0] if tables else ""),
            label="Select Table",
            on_change=lambda v: handle_table_select(v)
        )
    else:
        table_dropdown = mo.md("*Select a database to view tables*")
    
    def handle_table_select(table_name):
        """Handle table selection and load preview."""
        set_selected_table(table_name)
        
        if not table_name or not get_selected_db():
            set_preview(None)
            return
        
        full_path = Path(root) / get_selected_db()
        
        try:
            import pandas as pd
            import sqlite3
            
            conn = sqlite3.connect(str(full_path))
            df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 10", conn)
            conn.close()
            
            set_preview(df)
            
            logs = get_logs()
            set_logs(logs + [f"[Connie] Previewing {table_name}"])
        except Exception as e:
            logs = get_logs()
            set_logs(logs + [f"[Connie] Preview error: {str(e)}"])
            set_preview(None)
    
    # Format selector
    format_radio = mo.ui.radio(
        options={"csv": "CSV", "json": "JSON", "markdown": "Markdown", "sql": "SQL Dump"},
        value=get_export_format(),
        label="Export Format",
        on_change=set_export_format
    )
    
    # Preview display
    preview_df = get_preview()
    if preview_df is not None:
        try:
            preview_md = preview_df.to_markdown(index=False)
            preview_display = mo.md(f"""
### Preview (First 10 Rows)

{preview_md}

*{len(preview_df)} rows shown*
            """)
        except:
            preview_display = mo.md(f"```\n{preview_df.to_string()}\n```")
    else:
        preview_display = mo.md("*Select a table to preview data*")
    
    # Export function
    def do_export():
        selected_db = get_selected_db()
        selected_table = get_selected_table()
        export_format = get_export_format()
        
        if not selected_db or not selected_table:
            set_export_result("Please select a database and table first")
            return
        
        full_path = Path(root) / selected_db
        output_dir = Path(root) / "exports"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Try to use ConversionEngine
            try:
                import sys
                sys.path.insert(0, str(Path(__file__).parent.parent))
                from connie import ConversionEngine
                
                with ConversionEngine(str(full_path)) as engine:
                    if export_format == "csv":
                        output_file = engine.export_to_csv(selected_table, str(output_dir / f"{selected_table}_{timestamp}.csv"))
                    elif export_format == "json":
                        output_file = engine.export_to_json(selected_table, str(output_dir / f"{selected_table}_{timestamp}.json"))
                    elif export_format == "markdown":
                        output_file = engine.export_to_markdown(selected_table, str(output_dir / f"{selected_table}_{timestamp}.md"))
                    elif export_format == "sql":
                        output_file = engine.export_to_sql_dump(str(output_dir / f"{Path(selected_db).stem}_{timestamp}.sql"))
                    
                    set_export_result(f"Exported to: `{output_file}`")
                    logs = get_logs()
                    set_logs(logs + [f"[Connie] Exported {selected_table} to {export_format.upper()}"])
            except ImportError:
                # Fallback export
                import pandas as pd
                import sqlite3
                
                conn = sqlite3.connect(str(full_path))
                df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
                conn.close()
                
                if export_format == "csv":
                    output_file = output_dir / f"{selected_table}_{timestamp}.csv"
                    df.to_csv(output_file, index=False)
                elif export_format == "json":
                    output_file = output_dir / f"{selected_table}_{timestamp}.json"
                    df.to_json(output_file, orient="records", indent=2)
                elif export_format == "markdown":
                    output_file = output_dir / f"{selected_table}_{timestamp}.md"
                    with open(output_file, 'w') as f:
                        f.write(f"# {selected_table}\n\n")
                        f.write(df.to_markdown(index=False))
                elif export_format == "sql":
                    output_file = output_dir / f"{Path(selected_db).stem}_{timestamp}.sql"
                    conn = sqlite3.connect(str(full_path))
                    with open(output_file, 'w') as f:
                        for line in conn.iterdump():
                            f.write(f"{line}\n")
                    conn.close()
                
                set_export_result(f"Exported to: `{output_file}`")
                logs = get_logs()
                set_logs(logs + [f"[Connie] Exported {selected_table} (fallback mode)"])
        except Exception as e:
            set_export_result(f"Export failed: {str(e)}")
            logs = get_logs()
            set_logs(logs + [f"[Connie] Export error: {str(e)}"])
    
    # Export button
    export_btn = mo.ui.button(
        label="Export Table",
        on_change=lambda _: do_export(),
        disabled=not get_selected_table()
    )
    
    # Export all button
    def do_export_all():
        selected_db = get_selected_db()
        
        if not selected_db:
            set_export_result("Please select a database first")
            return
        
        full_path = Path(root) / selected_db
        output_dir = Path(root) / "exports"
        output_dir.mkdir(exist_ok=True)
        
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from connie import ConversionEngine
            
            with ConversionEngine(str(full_path)) as engine:
                results = engine.convert_all(str(output_dir))
                set_export_result(f"Exported all tables: {results}")
                logs = get_logs()
                set_logs(logs + [f"[Connie] Batch export completed"])
        except Exception as e:
            set_export_result(f"Batch export failed: {str(e)}")
    
    export_all_btn = mo.ui.button(
        label="Export All Tables",
        on_change=lambda _: do_export_all(),
        disabled=not get_selected_db()
    )
    
    # Export result display
    export_result = get_export_result()
    result_display = mo.md(export_result) if export_result else mo.md("")
    
    # Stats
    stats_md = f"**Databases found:** {len(db_files)} | **Tables loaded:** {len(tables)}"
    
    # Layout
    return mo.vstack([
        mo.md("## Connie Database Converter"),
        mo.md(stats_md),
        mo.md("---"),
        mo.hstack([db_picker, table_dropdown], gap="1rem"),
        mo.md("---"),
        preview_display,
        mo.md("---"),
        mo.hstack([format_radio, export_btn, export_all_btn], gap="1rem"),
        result_display,
        mo.md("---"),
        mo.md("*Exports saved to `exports/` directory in project root*")
    ])
