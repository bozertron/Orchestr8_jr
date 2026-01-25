# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Orchestr8 is a reactive Python dashboard built with Marimo that provides a "God View" of software projects. It consolidates file exploration, dependency analysis, connection visualization, and PRD generation into a single interface.

## Running the Application

```bash
marimo run orchestr8.py
```

For development mode with hot reloading:
```bash
marimo edit orchestr8.py
```

## Dependencies

- marimo (reactive notebook runtime)
- pandas (DataFrames for file/edge data)
- networkx (graph topology)
- pyvis (interactive graph visualization)
- jinja2 (PRD templating)

Install with:
```bash
pip install marimo pandas networkx pyvis jinja2
```

## Architecture

### State Management
The app uses Marimo's `mo.state()` hooks to manage global reactive state:
- `project_root` - target directory path
- `files_df` - DataFrame of scanned files with metadata and status badges
- `edges_df` - DataFrame of import dependencies (source -> target)
- `selected_file` - currently selected file in UI
- `agent_logs` - command log entries

### Core Components

**Data Layer (Harvesters)**
- `scan_project()` - walks directory tree, builds files DataFrame (excludes node_modules, .git, __pycache__)
- `verify_connections()` - parses imports via regex, assigns status badges (NORMAL/WARNING/COMPLEX), builds edges DataFrame

**UI Layer (Tabs)**
- Explorer: interactive table with status badges, single-row selection updates `selected_file`
- Connections: PyVis force-directed graph of import dependencies
- PRD Generator: Jinja2 template renders context for selected file
- Emperor: mission input + agent deployment logging

### Status Badge System
Files are classified by heuristics:
- NORMAL (green): default
- WARNING (orange): contains TODO/FIXME
- COMPLEX (purple): >10 imports
