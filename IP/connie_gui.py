#!/usr/bin/env python3
"""
CONNIE THE CONVERTER
A Desktop Database Conversion Tool for Linux

"Call Connie Causing Conversion!"

Features:
  - Detects SQLite databases in current folder
  - Beautiful PyQt6 interface
  - One-click conversion to multiple formats
  - Creates "Connie was here" output folder
  - Intelligent file naming (Connied_[name].[format])
  - Double-clickable on Fedora Linux
  - Portable (move anywhere, works everywhere)

Usage:
  1. Move Connie to a folder with .db files
  2. Double-click Connie to launch
  3. Select your database
  4. Click "Call Connie Causing Conversion"
  5. Find converted files in "Connie was here" folder

Installation:
  chmod +x connie.py
  ./connie.py
"""

import sys
import os
import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLabel, QMessageBox,
    QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap

# ============================================================================
# CONSTANTS
# ============================================================================

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
OUTPUT_FOLDER = "Connie was here"

# Color scheme
COLOR_PRIMARY = "#E53935"  # Connie Red
COLOR_ACCENT = "#D32F2F"   # Darker red
COLOR_SUCCESS = "#4CAF50"  # Green
COLOR_TEXT = "#FFFFFF"     # White
COLOR_BG = "#1E1E1E"       # Dark gray
COLOR_PANEL = "#2D2D2D"    # Darker gray

# ============================================================================
# CONVERSION ENGINE
# ============================================================================

class GUIConversionEngine:
    """GUI-specific database conversion engine with output directory management.
    
    Note: This is distinct from IP.connie.ConversionEngine which provides
    headless pandas-based conversion with context manager support.
    """
    
    def __init__(self, db_path: str, output_dir: str):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.db_name = Path(db_path).stem
        self.output_dir.mkdir(exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def get_tables(self) -> List[str]:
        """Get all table names"""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_table_info(self, table_name: str):
        """Get schema for a table"""
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        return self.cursor.fetchall()
    
    def get_foreign_keys(self, table_name: str):
        """Get foreign keys for a table"""
        self.cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        return self.cursor.fetchall()
    
    def get_table_data(self, table_name: str, limit: Optional[int] = None):
        """Get data from a table"""
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_row_count(self, table_name: str) -> int:
        """Get row count for a table"""
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return self.cursor.fetchone()[0]
    
    def export_sql_dump(self) -> str:
        """Export as SQL dump"""
        filename = self.output_dir / f"Connied_{self.db_name}.sql"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"-- SQL Dump: {self.db_name}\n")
            f.write(f"-- Created by Connie the Converter\n")
            f.write(f"-- {datetime.now().isoformat()}\n\n")
            
            for line in self.conn.iterdump():
                f.write(f"{line}\n")
        
        return str(filename)
    
    def export_json(self) -> str:
        """Export as JSON"""
        filename = self.output_dir / f"Connied_{self.db_name}.json"
        tables = self.get_tables()
        
        db_export = {
            "metadata": {
                "database": Path(self.db_path).name,
                "export_date": datetime.now().isoformat(),
                "table_count": len(tables),
                "tables": tables
            },
            "schema": {},
            "data": {}
        }
        
        for table_name in tables:
            schema_info = self.get_table_info(table_name)
            fk_info = self.get_foreign_keys(table_name)
            
            db_export["schema"][table_name] = {
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default_value": col[4],
                        "primary_key": bool(col[5])
                    }
                    for col in schema_info
                ],
                "foreign_keys": [
                    {
                        "column": fk[3],
                        "references_table": fk[2],
                        "references_column": fk[4]
                    }
                    for fk in fk_info
                ] if fk_info else []
            }
            
            rows = self.get_table_data(table_name, limit=100)
            columns = [col[1] for col in schema_info]
            
            db_export["data"][table_name] = {
                "row_count": self.get_row_count(table_name),
                "rows_included": len(rows),
                "data": [dict(zip(columns, row)) for row in rows]
            }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(db_export, f, indent=2, default=str)
        
        return str(filename)
    
    def export_markdown(self) -> str:
        """Export as Markdown"""
        filename = self.output_dir / f"Connied_{self.db_name}.md"
        tables = self.get_tables()
        
        md = []
        md.append(f"# {self.db_name} Database Reference\n")
        md.append(f"**Created by Connie the Converter**  \n")
        md.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        md.append(f"**Tables:** {len(tables)}\n")
        md.append("---\n")
        
        for table_name in tables:
            md.append(f"## Table: `{table_name}`\n")
            
            row_count = self.get_row_count(table_name)
            md.append(f"**Rows:** {row_count}\n")
            
            schema_info = self.get_table_info(table_name)
            
            md.append("### Schema\n")
            md.append("| Column | Type | Nullable | PK |")
            md.append("|--------|------|----------|-----|")
            
            for col in schema_info:
                col_name = col[1]
                col_type = col[2]
                nullable = "YES" if not col[3] else "NO"
                pk = "Y" if col[5] else ""
                md.append(f"| `{col_name}` | {col_type} | {nullable} | {pk} |")
            
            md.append("")
            
            md.append("### Data (Sample)\n")
            rows = self.get_table_data(table_name, limit=10)
            
            if rows:
                columns = [col[1] for col in schema_info]
                md.append("| " + " | ".join(columns) + " |")
                md.append("|" + "|".join(["-" * (len(col) + 2) for col in columns]) + "|")
                
                for row in rows:
                    row_data = [str(val) if val is not None else "NULL" for val in row]
                    row_data = [val[:40] + "..." if len(val) > 40 else val for val in row_data]
                    md.append("| " + " | ".join(row_data) + " |")
                
                if row_count > 10:
                    md.append(f"\n*Showing 10 of {row_count} rows*")
            else:
                md.append("*No data*")
            
            md.append("\n---\n")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md))
        
        return str(filename)
    
    def export_csv(self) -> List[str]:
        """Export as CSV files"""
        csv_dir = self.output_dir / f"Connied_{self.db_name}_CSV"
        csv_dir.mkdir(exist_ok=True)
        
        tables = self.get_tables()
        files = []
        
        for table_name in tables:
            schema_info = self.get_table_info(table_name)
            rows = self.get_table_data(table_name)
            columns = [col[1] for col in schema_info]
            
            csv_filename = csv_dir / f"{table_name}.csv"
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)
                writer.writerows(rows)
            
            files.append(str(csv_filename))
        
        return files
    
    def convert_all(self) -> dict:
        """Convert to all formats"""
        results = {
            "sql": self.export_sql_dump(),
            "json": self.export_json(),
            "markdown": self.export_markdown(),
            "csv": self.export_csv()
        }
        
        self.conn.close()
        return results


# ============================================================================
# CONVERSION THREAD (Non-blocking UI)
# ============================================================================

class ConversionThread(QThread):
    """Run conversion in background thread"""
    
    progress = pyqtSignal(str)  # Progress message
    finished = pyqtSignal(dict)  # Results
    error = pyqtSignal(str)  # Error message
    
    def __init__(self, db_path: str, output_dir: str):
        super().__init__()
        self.db_path = db_path
        self.output_dir = output_dir
    
    def run(self):
        try:
            self.progress.emit("Initializing Connie...")
            engine = GUIConversionEngine(self.db_path, self.output_dir)
            
            self.progress.emit("Converting to SQL...")
            sql_file = engine.export_sql_dump()
            
            self.progress.emit("Converting to JSON...")
            json_file = engine.export_json()
            
            self.progress.emit("Converting to Markdown...")
            md_file = engine.export_markdown()
            
            self.progress.emit("Converting to CSV...")
            csv_files = engine.export_csv()
            
            self.progress.emit("Conversion complete!")
            
            self.finished.emit({
                "sql": sql_file,
                "json": json_file,
                "markdown": md_file,
                "csv": csv_files,
                "output_dir": self.output_dir
            })
        
        except Exception as e:
            self.error.emit(f"Conversion failed: {str(e)}")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

class ConnieTheConverter(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.selected_db = None
        self.is_converting = False
        self.init_ui()
        self.find_databases()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Connie the Converter")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(self.get_stylesheet())
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Call Connie Causing Conversion")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #E53935; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Info label
        info = QLabel("SQLite Databases in this folder:")
        info.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        layout.addWidget(info)
        
        # Database list
        self.db_list = QListWidget()
        self.db_list.setStyleSheet("""
            QListWidget {
                background-color: #2D2D2D;
                border: 1px solid #E53935;
                border-radius: 5px;
                color: #FFFFFF;
            }
            QListWidget::item:selected {
                background-color: #E53935;
                color: #FFFFFF;
            }
            QListWidget::item:hover {
                background-color: #3D3D3D;
            }
        """)
        self.db_list.itemClicked.connect(self.on_db_selected)
        layout.addWidget(self.db_list)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #E53935;
                border-radius: 5px;
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #E53935;
            }
        """)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #BBBBBB; font-size: 11px;")
        layout.addWidget(self.status_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Big red conversion button
        self.convert_btn = QPushButton("CALL CONNIE CAUSING CONVERSION")
        self.convert_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.convert_btn.setMinimumHeight(60)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                padding: 15px;
            }
            QPushButton:hover:!pressed {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #C62828;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """)
        self.convert_btn.clicked.connect(self.on_convert)
        self.convert_btn.setEnabled(False)
        button_layout.addWidget(self.convert_btn)
        
        # Close button
        self.close_btn = QPushButton("X")
        self.close_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.close_btn.setMaximumWidth(50)
        self.close_btn.setMinimumHeight(60)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Info panel
        info_panel = QLabel(
            "Connie is a portable database converter.\n"
            "- Move me to any folder with .db files\n"
            "- Double-click to launch\n"
            "- Select a database and convert\n"
            "- Find results in 'Connie was here' folder"
        )
        info_panel.setStyleSheet("""
            background-color: #2D2D2D;
            border: 1px solid #444444;
            border-radius: 5px;
            padding: 10px;
            color: #CCCCCC;
            font-size: 10px;
            line-height: 1.5;
        """)
        info_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(info_panel)
        
        main_widget.setLayout(layout)
    
    def get_stylesheet(self) -> str:
        """Get application stylesheet"""
        return f"""
            QMainWindow {{
                background-color: {COLOR_BG};
                color: {COLOR_TEXT};
            }}
            QLabel {{
                color: {COLOR_TEXT};
            }}
        """
    
    def find_databases(self):
        """Find SQLite databases in current directory"""
        self.db_list.clear()
        current_dir = Path.cwd()
        
        db_files = list(current_dir.glob("*.db")) + list(current_dir.glob("*.sqlite"))
        
        if db_files:
            for db_file in sorted(db_files):
                item = QListWidgetItem(f"[DB] {db_file.name}")
                item.setData(Qt.ItemDataRole.UserRole, str(db_file))
                self.db_list.addItem(item)

            self.status_label.setText(f"Found {len(db_files)} database(s)")
        else:
            self.db_list.addItem("No .db or .sqlite files found")
            self.status_label.setText("Place Connie in a folder with databases")
    
    def on_db_selected(self, item):
        """Handle database selection"""
        if item.data(Qt.ItemDataRole.UserRole):
            self.selected_db = item.data(Qt.ItemDataRole.UserRole)
            self.convert_btn.setEnabled(True)
            self.status_label.setText(f"Selected: {Path(self.selected_db).name}")
        else:
            self.selected_db = None
            self.convert_btn.setEnabled(False)
    
    def on_convert(self):
        """Handle conversion button click"""
        if not self.selected_db or self.is_converting:
            return
        
        self.is_converting = True
        self.convert_btn.setEnabled(False)
        self.db_list.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create output directory
        output_dir = Path.cwd() / OUTPUT_FOLDER
        
        # Start conversion thread
        self.thread = ConversionThread(self.selected_db, str(output_dir))
        self.thread.progress.connect(self.on_progress)
        self.thread.finished.connect(self.on_conversion_finished)
        self.thread.error.connect(self.on_conversion_error)
        self.thread.start()
    
    def on_progress(self, message: str):
        """Update progress"""
        self.status_label.setText(message)
        self.progress_bar.setValue(min(self.progress_bar.value() + 20, 95))
    
    def on_conversion_finished(self, results: dict):
        """Handle conversion completion"""
        self.progress_bar.setValue(100)
        
        # Show success message
        output_dir = Path(results["output_dir"])

        QMessageBox.information(
            self,
            "Connie Was Here!",
            f"Database converted successfully!\n\n"
            f"Output folder:\n{output_dir}\n\n"
            f"Files created:\n"
            f"  - Connied_{Path(self.selected_db).stem}.sql\n"
            f"  - Connied_{Path(self.selected_db).stem}.json\n"
            f"  - Connied_{Path(self.selected_db).stem}.md\n"
            f"  - Connied_{Path(self.selected_db).stem}_CSV/\n\n"
            f"Ready to use with LLMs or other tools!"
        )
        
        # Reset UI
        self.is_converting = False
        self.convert_btn.setEnabled(True)
        self.db_list.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.selected_db = None
        self.status_label.setText("Ready for next conversion")
        self.db_list.clearSelection()
    
    def on_conversion_error(self, error: str):
        """Handle conversion error"""
        QMessageBox.critical(
            self,
            "Conversion Error",
            f"Connie encountered an error:\n\n{error}"
        )
        
        # Reset UI
        self.is_converting = False
        self.convert_btn.setEnabled(True)
        self.db_list.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Error during conversion")


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

def main():
    """Launch Connie the Converter"""
    app = QApplication(sys.argv)
    window = ConnieTheConverter()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
