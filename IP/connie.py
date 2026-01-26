"""
Connie Headless - Database Conversion Engine
Orchestr8 v3.0 - The Fortress Factory

A headless SQLite database conversion tool supporting multiple export formats.
No GUI dependencies - designed for programmatic use.

Usage:
    with ConversionEngine("path/to/database.db") as engine:
        tables = engine.list_tables()
        engine.export_to_json("table_name", "output.json")
        engine.export_to_csv("table_name", "output.csv")
        engine.export_to_markdown("table_name", "output.md")
        engine.export_to_sql_dump("output.sql")
"""

import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
import pandas as pd


class ConversionEngine:
    """
    Headless SQLite database conversion engine.
    
    Supports context manager pattern for automatic resource cleanup.
    
    Example:
        with ConversionEngine("my_database.db") as engine:
            print(engine.list_tables())
            engine.export_to_json("users", "users.json")
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the conversion engine.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_name = self.db_path.stem
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {db_path}")
    
    def __enter__(self) -> 'ConversionEngine':
        """Context manager entry - open database connection."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.cursor = None
        self.conn = None
    
    def _ensure_connected(self) -> None:
        """Ensure database connection is open."""
        if self.conn is None:
            raise RuntimeError(
                "Database not connected. Use 'with ConversionEngine(path) as engine:'"
            )
    
    def list_tables(self) -> pd.DataFrame:
        """
        Get all table names in the database.
        
        Returns:
            DataFrame with table names and row counts
        """
        self._ensure_connected()
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in self.cursor.fetchall()]
        
        # Get row counts
        table_info = []
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
            count = self.cursor.fetchone()[0]
            table_info.append({"name": table, "row_count": count})
        
        return pd.DataFrame(table_info)
    
    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """
        Get schema information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            DataFrame with column information
        """
        self._ensure_connected()
        self.cursor.execute(f"PRAGMA table_info([{table_name}])")
        columns = self.cursor.fetchall()
        
        schema_data = []
        for col in columns:
            schema_data.append({
                "column_id": col[0],
                "name": col[1],
                "type": col[2],
                "not_null": bool(col[3]),
                "default_value": col[4],
                "primary_key": bool(col[5])
            })
        
        return pd.DataFrame(schema_data)
    
    def get_table_data(self, table_name: str, limit: Optional[int] = None) -> pd.DataFrame:
        """
        Get data from a table as a DataFrame.
        
        Args:
            table_name: Name of the table
            limit: Optional row limit
            
        Returns:
            DataFrame with table data
        """
        self._ensure_connected()
        query = f"SELECT * FROM [{table_name}]"
        if limit:
            query += f" LIMIT {limit}"
        
        return pd.read_sql_query(query, self.conn)
    
    def export_to_json(self, table_name: Optional[str] = None, output_path: str = None) -> str:
        """
        Export table(s) to JSON format.
        
        Args:
            table_name: Specific table to export (None for all tables)
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to the created JSON file
        """
        self._ensure_connected()
        
        if output_path is None:
            suffix = f"_{table_name}" if table_name else ""
            output_path = f"{self.db_name}{suffix}.json"
        
        output_file = Path(output_path)
        
        if table_name:
            # Export single table
            df = self.get_table_data(table_name)
            export_data = {
                "metadata": {
                    "database": self.db_name,
                    "table": table_name,
                    "export_date": datetime.now().isoformat(),
                    "row_count": len(df)
                },
                "data": df.to_dict(orient="records")
            }
        else:
            # Export all tables
            tables_df = self.list_tables()
            export_data = {
                "metadata": {
                    "database": self.db_name,
                    "export_date": datetime.now().isoformat(),
                    "table_count": len(tables_df)
                },
                "tables": {}
            }
            
            for _, row in tables_df.iterrows():
                tbl = row["name"]
                df = self.get_table_data(tbl)
                export_data["tables"][tbl] = {
                    "row_count": len(df),
                    "data": df.to_dict(orient="records")
                }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return str(output_file)
    
    def export_to_csv(self, table_name: str, output_path: str = None) -> str:
        """
        Export a table to CSV format.
        
        Args:
            table_name: Name of the table to export
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to the created CSV file
        """
        self._ensure_connected()
        
        if output_path is None:
            output_path = f"{self.db_name}_{table_name}.csv"
        
        output_file = Path(output_path)
        df = self.get_table_data(table_name)
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        return str(output_file)
    
    def export_to_markdown(self, table_name: Optional[str] = None, output_path: str = None) -> str:
        """
        Export table(s) to Markdown format.
        
        Args:
            table_name: Specific table to export (None for all tables)
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to the created Markdown file
        """
        self._ensure_connected()
        
        if output_path is None:
            suffix = f"_{table_name}" if table_name else ""
            output_path = f"{self.db_name}{suffix}.md"
        
        output_file = Path(output_path)
        
        md_lines = [
            f"# Database: {self.db_name}",
            f"",
            f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            "---",
            ""
        ]
        
        if table_name:
            tables = [table_name]
        else:
            tables_df = self.list_tables()
            tables = tables_df["name"].tolist()
            md_lines.append(f"**Tables:** {len(tables)}")
            md_lines.append("")
        
        for tbl in tables:
            df = self.get_table_data(tbl, limit=10)
            schema_df = self.get_table_schema(tbl)
            
            md_lines.append(f"## Table: `{tbl}`")
            md_lines.append("")
            md_lines.append(f"**Rows:** {len(self.get_table_data(tbl))}")
            md_lines.append("")
            
            # Schema
            md_lines.append("### Schema")
            md_lines.append("")
            md_lines.append("| Column | Type | Nullable | PK |")
            md_lines.append("|--------|------|----------|-----|")
            
            for _, col in schema_df.iterrows():
                nullable = "YES" if not col["not_null"] else "NO"
                pk = "✓" if col["primary_key"] else ""
                md_lines.append(f"| `{col['name']}` | {col['type']} | {nullable} | {pk} |")
            
            md_lines.append("")
            
            # Sample data
            md_lines.append("### Sample Data (first 10 rows)")
            md_lines.append("")
            
            if not df.empty:
                md_lines.append(df.to_markdown(index=False))
            else:
                md_lines.append("*No data*")
            
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))
        
        return str(output_file)
    
    def export_to_sql_dump(self, output_path: str = None) -> str:
        """
        Export entire database as SQL dump.
        
        Args:
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to the created SQL file
        """
        self._ensure_connected()
        
        if output_path is None:
            output_path = f"{self.db_name}.sql"
        
        output_file = Path(output_path)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"-- SQL Dump: {self.db_name}\n")
            f.write(f"-- Exported by Connie Headless\n")
            f.write(f"-- {datetime.now().isoformat()}\n\n")
            
            for line in self.conn.iterdump():
                f.write(f"{line}\n")
        
        return str(output_file)
    
    def convert_all(self, output_dir: str = ".") -> Dict[str, Any]:
        """
        Convert database to all supported formats.
        
        Args:
            output_dir: Directory for output files
            
        Returns:
            Dictionary with paths to all created files
        """
        self._ensure_connected()
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {
            "sql": self.export_to_sql_dump(str(output_path / f"{self.db_name}.sql")),
            "json": self.export_to_json(output_path=str(output_path / f"{self.db_name}.json")),
            "markdown": self.export_to_markdown(output_path=str(output_path / f"{self.db_name}.md")),
            "csv": []
        }
        
        # Export each table to CSV
        tables_df = self.list_tables()
        csv_dir = output_path / f"{self.db_name}_csv"
        csv_dir.mkdir(exist_ok=True)
        
        for _, row in tables_df.iterrows():
            csv_path = self.export_to_csv(
                row["name"], 
                str(csv_dir / f"{row['name']}.csv")
            )
            results["csv"].append(csv_path)
        
        return results


# Convenience function for quick operations
def quick_export(db_path: str, output_format: str = "json", table: str = None) -> str:
    """
    Quick export helper function.
    
    Args:
        db_path: Path to SQLite database
        output_format: One of 'json', 'csv', 'markdown', 'sql'
        table: Specific table (required for csv)
        
    Returns:
        Path to created file
    """
    with ConversionEngine(db_path) as engine:
        if output_format == "json":
            return engine.export_to_json(table)
        elif output_format == "csv":
            if not table:
                raise ValueError("Table name required for CSV export")
            return engine.export_to_csv(table)
        elif output_format == "markdown":
            return engine.export_to_markdown(table)
        elif output_format == "sql":
            return engine.export_to_sql_dump()
        else:
            raise ValueError(f"Unknown format: {output_format}")
