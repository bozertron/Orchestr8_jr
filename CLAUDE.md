# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL: Read SOT.md First

**The Source of Truth is `SOT.md`** - read it before making any changes.

## Project Overview

Orchestr8 is a reactive Python dashboard built with Marimo that provides a "God View" of software projects. The UI goal is the stereOS layout implemented in `IP/plugins/06_maestro.py`.

## Running the Application

```bash
marimo run orchestr8.py
```

For development mode with hot reloading:
```bash
marimo edit orchestr8.py
```

## Architecture

- **Entry Point:** `orchestr8.py` (loads plugins from `IP/plugins/`)
- **UI Goal:** `IP/plugins/06_maestro.py` (stereOS layout with Woven Maps Code City)
- **Config:** `pyproject_orchestr8_settings.toml`

### Plugin System

Plugins are loaded from `IP/plugins/` in order (00_, 01_, etc.). Each plugin exports:
- `PLUGIN_NAME` - Display name for tab
- `PLUGIN_ORDER` - Sort order
- `render(STATE_MANAGERS)` - Returns UI content

### Key Modules in IP/

- `woven_maps.py` - Code City visualization (COMPLETE)
- `combat_tracker.py` - LLM deployment tracking
- `connection_verifier.py` - Import graph builder
- `louis_core.py` - File protection system

## Color System

| State | Color | Hex |
|-------|-------|-----|
| Working | Gold | #D4AF37 |
| Broken | Blue | #1fbdea |
| Combat | Purple | #9D4EDD |

## Integration Policy

All future integrations are staged in `one integration at a time/`.

**EVERY integration requires Ben's approval before proceeding.**

See `one integration at a time/INTEGRATION_QUEUE.md` for the queue.

## Dependencies

```bash
pip install marimo pandas networkx pyvis jinja2
```
